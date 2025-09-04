<template>
  <div class="home-container">
    <div class="search-box">
      <h2>IP Information Lookup</h2>
      <p>Enter an IP address or hostname to get detailed information</p>
      
      <div class="input-group">
        <input 
          type="text" 
          v-model="ipInput" 
          placeholder="IP address or hostname (e.g., 8.8.8.8 or google.com)"
          @keyup.enter="lookupIP"
        />
        <button @click="lookupIP" :disabled="isLoading">
          {{ isLoading ? 'Loading...' : 'Lookup' }}
        </button>
      </div>
      
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>
    </div>
    
    <div v-if="ipInfo" class="results-box">
      <h3>Information for {{ ipInfo.ip }}</h3>
      
      <div class="info-grid">
        <div class="info-item">
          <strong>IP Address:</strong> {{ ipInfo.ip }}
        </div>
        <div class="info-item">
          <strong>Hostname:</strong> {{ ipInfo.hostname || 'N/A' }}
        </div>
        <div class="info-item">
          <strong>Country:</strong> {{ ipInfo.country || 'N/A' }}
        </div>
        <div class="info-item">
          <strong>Region:</strong> {{ ipInfo.region || 'N/A' }}
        </div>
        <div class="info-item">
          <strong>City:</strong> {{ ipInfo.city || 'N/A' }}
        </div>
        <div class="info-item">
          <strong>Postal:</strong> {{ ipInfo.postal || 'N/A' }}
        </div>
        <div class="info-item">
          <strong>Location:</strong> {{ ipInfo.loc || 'N/A' }}
        </div>
        <div class="info-item">
          <strong>Timezone:</strong> {{ ipInfo.timezone || 'N/A' }}
        </div>
        <div class="info-item">
          <strong>Organization:</strong> {{ ipInfo.org || 'N/A' }}
        </div>
        <div class="info-item">
          <strong>ASN:</strong> {{ ipInfo.asn || 'N/A' }}
        </div>
      </div>
      
      <div class="map-container" v-if="ipInfo.loc">
        <h4>Map Location</h4>
        <div id="ip-map" ref="mapContainer"></div>
      </div>
      
      <div class="action-buttons">
        <router-link :to="'/ip/' + ipInfo.ip" class="button">View Detailed Information</router-link>
        <button @click="copyToClipboard()" class="button secondary">Copy JSON</button>
      </div>
    </div>
    
    <div class="features-section">
      <h3>Features of Self-Hosted IP Info</h3>
      <div class="features-grid">
        <div class="feature-card">
          <h4>Geolocation Data</h4>
          <p>Get accurate location information including country, region, city, and geographic coordinates.</p>
        </div>
        <div class="feature-card">
          <h4>Network Information</h4>
          <p>View ASN details, organization, and network provider information.</p>
        </div>
        <div class="feature-card">
          <h4>Self-Hosted Solution</h4>
          <p>Keep your data private and secure with this self-hosted alternative to third-party services.</p>
        </div>
        <div class="feature-card">
          <h4>API Access</h4>
          <p>Integrate with your own applications using our simple and fast API.</p>
        </div>
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
  name: 'Home',
  setup() {
    const ipInput = ref('');
    const ipInfo = ref(null);
    const errorMessage = ref('');
    const isLoading = ref(false);
    const mapContainer = ref(null);
    let map = null;
    
    // Get client IP on component mount
    onMounted(async () => {
      try {
        const response = await axios.get('/api');
        ipInfo.value = response.data;
        
        // Initialize map after data is loaded
        nextTick(() => {
          if (ipInfo.value && ipInfo.value.loc) {
            initMap();
          }
        });
      } catch (error) {
        console.error('Error fetching client IP info:', error);
      }
    });
    
    // Initialize Leaflet map
    const initMap = () => {
      if (!ipInfo.value.loc || !mapContainer.value) return;
      
      if (map) {
        map.remove();
      }
      
      const [lat, lng] = ipInfo.value.loc.split(',').map(Number);
      
      map = L.map(mapContainer.value).setView([lat, lng], 10);
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map);
      
      L.marker([lat, lng]).addTo(map)
        .bindPopup(`<b>${ipInfo.value.ip}</b><br>${ipInfo.value.city || ''}, ${ipInfo.value.country || ''}`)
        .openPopup();
    };
    
    // Lookup IP function
    const lookupIP = async () => {
      if (!ipInput.value.trim()) {
        errorMessage.value = 'Please enter an IP address or hostname';
        return;
      }
      
      errorMessage.value = '';
      isLoading.value = true;
      
      try {
        const response = await axios.get(`/api/${ipInput.value}`);
        ipInfo.value = response.data;
        
        // Initialize map after data is loaded
        nextTick(() => {
          if (ipInfo.value && ipInfo.value.loc) {
            initMap();
          }
        });
      } catch (error) {
        console.error('Error looking up IP:', error);
        errorMessage.value = error.response?.data?.detail || 'Error looking up IP information';
      } finally {
        isLoading.value = false;
      }
    };
    
    // Copy JSON to clipboard
    const copyToClipboard = () => {
      if (!ipInfo.value) return;
      
      const jsonText = JSON.stringify(ipInfo.value, null, 2);
      
      // Create a temporary textarea element to copy from
      const textarea = document.createElement('textarea');
      textarea.value = jsonText;
      document.body.appendChild(textarea);
      textarea.select();
      
      try {
        // Use the older document.execCommand API which has better compatibility
        const success = document.execCommand('copy');
        if (success) {
          alert('IP information copied to clipboard!');
        } else {
          throw new Error('Copy operation failed');
        }
      } catch (err) {
        console.error('Failed to copy:', err);
        
        // Try the newer navigator.clipboard API as fallback
        try {
          navigator.clipboard.writeText(jsonText)
            .then(() => {
              alert('IP information copied to clipboard!');
            })
            .catch(clipErr => {
              console.error('Clipboard API failed:', clipErr);
              alert('Failed to copy to clipboard. Please copy manually:\n\n' + jsonText);
            });
        } catch (finalErr) {
          console.error('All copy methods failed:', finalErr);
          alert('Failed to copy to clipboard. Please copy manually:\n\n' + jsonText);
        }
      } finally {
        // Clean up the temporary element
        document.body.removeChild(textarea);
      }
    };
    
    return {
      ipInput,
      ipInfo,
      errorMessage,
      isLoading,
      mapContainer,
      lookupIP,
      copyToClipboard
    };
  }
}
</script>

<style scoped>
.home-container {
  max-width: 900px;
  margin: 0 auto;
}

.search-box {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
  text-align: center;
}

.input-group {
  display: flex;
  margin: 1.5rem 0;
}

.input-group input {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 1rem;
}

.input-group button {
  padding: 0.75rem 1.5rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 0 4px 4px 0;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.input-group button:hover {
  background-color: #2980b9;
}

.input-group button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.error-message {
  color: #e74c3c;
  margin-top: 1rem;
}

.results-box {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
  margin: 1.5rem 0;
}

.info-item {
  padding: 0.5rem;
  border-bottom: 1px solid #eee;
}

.map-container {
  margin: 1.5rem 0;
}

#ip-map {
  height: 300px;
  border-radius: 8px;
  margin-top: 1rem;
}

.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
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
  text-align: center;
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

.features-section {
  margin-top: 3rem;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.feature-card {
  background-color: white;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h4 {
  color: #3498db;
  margin-top: 0;
}
</style>