<template>
  <div class="about-container">
    <div class="about-content">
      <h2>About Self-Hosted IP Info</h2>
      
      <p class="intro">
        Self-Hosted IP Info is a Docker-based alternative to services like ipinfo.io, 
        allowing you to host your own IP information service with full control over your data.
      </p>
      
      <div class="section">
        <h3>Why Self-Host?</h3>
        <div class="feature-grid">
          <div class="feature-card">
            <h4>Privacy</h4>
            <p>Keep your IP lookup data private and secure. No third-party has access to your query patterns or data.</p>
          </div>
          <div class="feature-card">
            <h4>Control</h4>
            <p>Full control over the infrastructure, allowing you to customize and extend functionality as needed.</p>
          </div>
          <div class="feature-card">
            <h4>Cost Efficiency</h4>
            <p>Avoid subscription fees for high-volume API usage, especially for internal or development environments.</p>
          </div>
          <div class="feature-card">
            <h4>Reliability</h4>
            <p>No dependency on external services. Your IP lookup service works even if your internet connection is limited.</p>
          </div>
        </div>
      </div>
      
      <div class="section">
        <h3>Key Features</h3>
        <ul class="feature-list">
          <li>
            <strong>Comprehensive IP Information:</strong> Access detailed IP data including geolocation, ASN, organization, and more.
          </li>
          <li>
            <strong>Simple API:</strong> Easy-to-use REST API with JSON responses.
          </li>
          <li>
            <strong>Fast Response Times:</strong> Redis caching ensures fast response times for repeated queries.
          </li>
          <li>
            <strong>Bulk Lookup:</strong> Look up multiple IP addresses in a single API call.
          </li>
          <li>
            <strong>IPv4 and IPv6 Support:</strong> Full support for both IPv4 and IPv6 addresses.
          </li>
          <li>
            <strong>Visual Interface:</strong> User-friendly web interface for looking up IP information.
          </li>
          <li>
            <strong>Self-Updating:</strong> Automatic database updates to ensure accuracy.
          </li>
          <li>
            <strong>Docker-Based:</strong> Easy deployment using Docker and Docker Compose.
          </li>
        </ul>
      </div>
      
      <div class="section">
        <h3>Architecture</h3>
        <p>
          Self-Hosted IP Info is built using a modern, containerized architecture:
        </p>
        <div class="architecture-diagram">
          <div class="component api">
            <h4>API Service</h4>
            <p>FastAPI-based RESTful API for IP lookups</p>
          </div>
          <div class="component db">
            <h4>Database</h4>
            <p>PostgreSQL for storing IP metadata</p>
          </div>
          <div class="component cache">
            <h4>Cache</h4>
            <p>Redis for caching frequent lookups</p>
          </div>
          <div class="component updater">
            <h4>Updater</h4>
            <p>Service for keeping IP databases current</p>
          </div>
          <div class="component ui">
            <h4>Web UI</h4>
            <p>Vue.js frontend for user interaction</p>
          </div>
        </div>
      </div>
      
      <div class="section">
        <h3>Data Sources</h3>
        <p>
          Self-Hosted IP Info uses a combination of data sources to provide accurate IP information:
        </p>
        <ul class="data-sources-list">
          <li>
            <strong>MaxMind GeoLite2:</strong> For geolocation and ASN data (city, country, coordinates, etc.)
          </li>
          <li>
            <strong>Curated Lists:</strong> For VPN, proxy, and hosting detection
          </li>
          <li>
            <strong>Real-time Lookups:</strong> For hostname resolution and other dynamic data
          </li>
        </ul>
        <div class="note">
          <p>
            <strong>Note:</strong> For production use, you should sign up for a MaxMind account to access their database downloads.
            The included updater script can be configured with your license key.
          </p>
        </div>
      </div>
      
      <div class="section">
        <h3>Getting Started</h3>
        <p>
          To get started with Self-Hosted IP Info:
        </p>
        <ol class="steps-list">
          <li>Clone the repository from GitHub</li>
          <li>Configure your environment variables (optional)</li>
          <li>Run <code>docker-compose up -d</code> to start the services</li>
          <li>Access the web UI at <code>http://localhost:8081</code></li>
          <li>Use the API at <code>http://localhost:8080</code></li>
        </ol>
        <p>
          For more detailed instructions, check out the project's README file.
        </p>
      </div>
      
      <div class="section">
        <h3>Customization</h3>
        <p>
          Self-Hosted IP Info is designed to be customizable. You can:
        </p>
        <ul class="customization-list">
          <li>Add additional data sources</li>
          <li>Modify the API to include custom fields</li>
          <li>Extend the UI with new features</li>
          <li>Implement authentication for the API</li>
          <li>Add usage analytics and reporting</li>
        </ul>
      </div>
      
      <div class="section">
        <h3>License</h3>
        <p>
          Self-Hosted IP Info is open-source software released under the MIT License.
          You are free to use, modify, and distribute it according to the terms of the license.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'About'
}
</script>

<style scoped>
.about-container {
  max-width: 900px;
  margin: 0 auto;
}

.about-content {
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.intro {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.section {
  margin-bottom: 3rem;
}

.section:last-child {
  margin-bottom: 0;
}

.section h3 {
  color: #3498db;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.feature-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.feature-card {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h4 {
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 0.75rem;
}

.feature-card p {
  margin: 0;
  color: #7f8c8d;
}

.feature-list,
.data-sources-list,
.steps-list,
.customization-list {
  padding-left: 1.5rem;
  line-height: 1.6;
}

.feature-list li,
.data-sources-list li,
.customization-list li {
  margin-bottom: 0.75rem;
}

.steps-list li {
  margin-bottom: 0.5rem;
}

.steps-list code {
  background-color: #f5f5f5;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-family: monospace;
}

.note {
  background-color: #fdf6e3;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1.5rem;
  border-left: 4px solid #f39c12;
}

.note p {
  margin: 0;
  color: #7f8c8d;
}

.architecture-diagram {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: repeat(2, auto);
  gap: 1.5rem;
  margin: 1.5rem 0;
}

.component {
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
}

.component h4 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #2c3e50;
}

.component p {
  margin: 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.component.api {
  grid-column: 1 / 4;
  background-color: #3498db;
}

.component.api h4,
.component.api p {
  color: white;
}

.component.db {
  background-color: #2ecc71;
}

.component.db h4,
.component.db p {
  color: white;
}

.component.cache {
  background-color: #e74c3c;
}

.component.cache h4,
.component.cache p {
  color: white;
}

.component.updater {
  background-color: #f39c12;
}

.component.updater h4,
.component.updater p {
  color: white;
}

.component.ui {
  background-color: #9b59b6;
}

.component.ui h4,
.component.ui p {
  color: white;
}

@media (max-width: 768px) {
  .about-content {
    padding: 1.5rem;
  }
  
  .feature-grid {
    grid-template-columns: 1fr;
  }
  
  .architecture-diagram {
    grid-template-columns: 1fr;
  }
  
  .component.api {
    grid-column: auto;
  }
}
</style>
