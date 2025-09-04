<template>
  <div class="ip-details-container">
    <div v-if="isLoading" class="loading">
      <p>Loading IP information...</p>
    </div>
    
    <div v-else-if="errorMessage" class="error-container">
      <h2>Error</h2>
      <p>{{ errorMessage }}</p>
      <router-link to="/" class="button">Back to Home</router-link>
    </div>
    
    <div v-else-if="ipInfo" class="details-content">
      <div class="details-header">
        <h2>Details for {{ ipInfo.ip }}</h2>
        <div class="actions">
          <button @click="copyToClipboard()" class="button secondary">Copy JSON</button>
          <router-link to="/" class="button">New Lookup</router-link>
        </div>
      </div>
      
      <div class="details-grid">
        <div class="detail-section">
          <h3>Basic Information</h3>
          <div class="detail-item">
            <div class="label">IP Address</div>
            <div class="value">{{ ipInfo.ip }}</div>
          </div>
          <div class="detail-item">
            <div class="label">Hostname</div>
            <div class="value">{{ ipInfo.hostname || 'Not available' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">Type</div>
            <div class="value">{{ getIPType() }}</div>
          </div>
        </div>
        
        <div class="detail-section">
          <h3>Location</h3>
          <div class="detail-item">
            <div class="label">Country</div>
            <div class="value">{{ ipInfo.country || 'Not available' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">Region</div>
            <div class="value">{{ ipInfo.region || 'Not available' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">City</div>
            <div class="value">{{ ipInfo.city || 'Not available' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">Postal Code</div>
            <div class="value">{{ ipInfo.postal || 'Not available' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">Coordinates</div>
            <div class="value">{{ ipInfo.loc || 'Not available' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">Timezone</div>
            <div class="value">{{ ipInfo.timezone || 'Not available' }}</div>
          </div>
        </div>
        
        <div class="detail-section">
          <h3>Network</h3>
          <div class="detail-item">
            <div class="label">Organization</div>
            <div class="value">{{ ipInfo.org || 'Not available' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">ASN</div>
            <div class="value">{{ ipInfo.asn || 'Not available' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">ASN Organization</div>
            <div class="value">{{ ipInfo.asn_org || 'Not available' }}</div>
          </div>
        </div>
        
        <div class="detail-section">
          <h3>Security</h3>
          <div class="detail-item">
            <div class="label">VPN</div>
            <div class="value">{{ ipInfo.is_vpn ? 'Yes' : 'No' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">Proxy</div>
            <div class="value">{{ ipInfo.is_proxy ? 'Yes' : 'No' }}</div>
          </div>
          <div class="detail-item">
            <div class="label">Hosting</div>
            <div class="value">{{ ipInfo.is_hosting ? 'Yes' : 'No' }}</div>
          </div>
        </div>
      </div>
      
      <div class="map-section" v-if="ipInfo.loc">
        <h3>Map Location</h3>
        <div id="detail-map" ref="mapContainer"></div>
      </div>
      
      <div class="json-section">
        <h3>Raw JSON</h3>
        <pre>{{ JSON.stringify(ipInfo, null, 2) }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { onMounted, ref, nextTick } from 'vue';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default {
  name: 'IPDetails',
  props: {
    ip: {
      type: String,
      required: true
    }
  },
  setup(props) {
    const ipInfo = ref(null);
    const isLoading = ref(true);
    const errorMessage = ref('');
    const mapContainer = ref(null);
    let map = null;
    
    // Get IP details on component mount
    onMounted(async () => {
      try {
        const response = await axios.get(`/api/${props.ip}`);
        ipInfo.value = response.data;
        isLoading.value = false;
        
        // Initialize map after data is loaded
        nextTick(() => {
          if (ipInfo.value && ipInfo.value.loc) {
            initMap();
          }
        });
      } catch (error) {
        console.error('Error fetching IP details:', error);
        errorMessage.value = error.response?.data?.detail || 'Error looking up IP information';
        isLoading.value = false;
      }
    });
    
    // Initialize Leaflet map
    const initMap = () => {
      if (!ipInfo.value.loc || !mapContainer.value) return;
      
      const [lat, lng] = ipInfo.value.loc.split(',').map(Number);
      
      map = L.map(mapContainer.value).setView([lat, lng], 10);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      
      L.marker([lat, lng]).addTo(map)
        .bindPopup(`<b>${ipInfo.value.ip}</b><br>${ipInfo.value.city || ''}, ${ipInfo.value.country || ''}`)
        .openPopup();
    };
    
    // Determine IP type (IPv4 or IPv6)
    const getIPType = () => {
      if (!ipInfo.value || !ipInfo.value.ip) return 'Unknown';
      
      return ipInfo.value.ip.includes(':') ? 'IPv6' : 'IPv4';
    };
    
    // Copy JSON to clipboard
    const copyToClipboard = () => {
      if (!ipInfo.value) return;
      
      const jsonText = JSON.stringify(ipInfo.value, null, 2);
      navigator.clipboard.writeText(jsonText)
        .then(() => {
          alert('IP information copied to clipboard!');
        })
        .catch(err => {
          console.error('Failed to copy:', err);
          alert('Failed to copy to clipboard');
        });
    };
    
    return {
      ipInfo,
      isLoading,
      errorMessage,
      mapContainer,
      getIPType,
      copyToClipboard
    };
  }
}
</script>

<style scoped>
.ip-details-container {
  max-width: 1000px;
  margin: 0 auto;
}

.loading {
  text-align: center;
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.error-container {
  padding: 2rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.error-container h2 {
  color: #e74c3c;
}

.details-content {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.actions {
  display: flex;
  gap: 1rem;
}

.button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.button:hover {
  background-color: #2980b9;
}

.button.secondary {
  background-color: #2c3e50;
}

.button.secondary:hover {
  background-color: #1a252f;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.detail-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
}

.detail-section h3 {
  margin-top: 0;
  color: #3498db;
  border-bottom: 1px solid #ddd;
  padding-bottom: 0.5rem;
  margin-bottom: 1rem;
}

.detail-item {
  display: flex;
  margin-bottom: 0.75rem;
}

.label {
  font-weight: bold;
  width: 40%;
  color: #7f8c8d;
}

.value {
  width: 60%;
  word-break: break-word;
}

.map-section {
  margin: 2rem 0;
}

.map-section h3 {
  color: #3498db;
  margin-bottom: 1rem;
}

#detail-map {
  height: 400px;
  border-radius: 8px;
}

.json-section {
  margin-top: 2rem;
}

.json-section h3 {
  color: #3498db;
  margin-bottom: 1rem;
}

.json-section pre {
  background-color: #f5f5f5;
  padding: 1rem;
  border-radius: 4px;
  overflow-x: auto;
  font-family: monospace;
}

@media (max-width: 768px) {
  .details-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .detail-item {
    flex-direction: column;
  }
  
  .label, .value {
    width: 100%;
  }
  
  .label {
    margin-bottom: 0.25rem;
  }
}
</style>