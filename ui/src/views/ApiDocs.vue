<template>
  <div class="docs-container">
    <h2>API Documentation</h2>
    <p class="intro">Our IP Information API provides a simple and fast way to get detailed information about IP addresses. Here's how to use it:</p>
    
    <div class="section">
      <h3>Base URL</h3>
      <div class="code-block">{{ baseUrl }}</div>
    </div>
    
    <div class="section">
      <h3>Authentication</h3>
      <p>Currently, the API is available without authentication for self-hosted deployments. For rate limiting, the API uses the client's IP address.</p>
    </div>
    
    <div class="section">
      <h3>Rate Limits</h3>
      <p>The default rate limit is 100 requests per hour per IP address. This can be configured in the Docker environment variables.</p>
    </div>
    
    <div class="section">
      <h3>Endpoints</h3>
      
      <div class="endpoint">
        <h4>Get your own IP information</h4>
        <div class="endpoint-details">
          <div class="method">GET</div>
          <div class="url">{{ baseUrl }}</div>
        </div>
        <p>Returns information about the IP address making the request.</p>
        <div class="example-wrapper">
          <h5>Example Request:</h5>
          <div class="code-block">curl {{ baseUrl }}</div>
          
          <h5>Example Response:</h5>
          <pre class="code-block">{{
`{
  "ip": "203.0.113.1",
  "hostname": "example.com",
  "city": "San Francisco",
  "region": "California",
  "country": "US",
  "loc": "37.7749,-122.4194",
  "org": "Example ISP",
  "postal": "94107",
  "timezone": "America/Los_Angeles",
  "asn": "AS13335",
  "asn_org": "Example Network",
  "is_vpn": false,
  "is_proxy": false,
  "is_hosting": false
}`
          }}</pre>
        </div>
      </div>
      
      <div class="endpoint">
        <h4>Get information for a specific IP</h4>
        <div class="endpoint-details">
          <div class="method">GET</div>
          <div class="url">{{ baseUrl }}/{ip_address}</div>
        </div>
        <p>Returns information about the specified IP address or hostname.</p>
        <div class="example-wrapper">
          <h5>Example Request:</h5>
          <div class="code-block">curl {{ baseUrl }}/8.8.8.8</div>
          
          <h5>Example Response:</h5>
          <pre class="code-block">{{
`{
  "ip": "8.8.8.8",
  "hostname": "dns.google",
  "city": "Mountain View",
  "region": "California",
  "country": "US",
  "loc": "37.4056,-122.0775",
  "org": "Google LLC",
  "postal": "94043",
  "timezone": "America/Los_Angeles",
  "asn": "AS15169",
  "asn_org": "Google LLC",
  "is_vpn": false,
  "is_proxy": false,
  "is_hosting": true
}`
          }}</pre>
        </div>
      </div>
      
      <div class="endpoint">
        <h4>Get a specific field for an IP</h4>
        <div class="endpoint-details">
          <div class="method">GET</div>
          <div class="url">{{ baseUrl }}/{ip_address}/{field}</div>
        </div>
        <p>Returns a specific field from the IP information.</p>
        <div class="example-wrapper">
          <h5>Example Request:</h5>
          <div class="code-block">curl {{ baseUrl }}/8.8.8.8/country</div>
          
          <h5>Example Response:</h5>
          <pre class="code-block">{{
`{
  "country": "US"
}`
          }}</pre>
        </div>
        <div class="note">
          <p>Available fields: ip, hostname, city, region, country, loc, org, postal, timezone, asn, asn_org, is_vpn, is_proxy, is_hosting</p>
        </div>
      </div>
      
      <div class="endpoint">
        <h4>Bulk IP Lookup</h4>
        <div class="endpoint-details">
          <div class="method">GET</div>
          <div class="url">{{ baseUrl }}/bulk?ips=ip1,ip2,ip3</div>
        </div>
        <p>Returns information for multiple IP addresses in a single request (maximum 100 IPs).</p>
        <div class="example-wrapper">
          <h5>Example Request:</h5>
          <div class="code-block">curl "{{ baseUrl }}/bulk?ips=8.8.8.8,1.1.1.1"</div>
          
          <h5>Example Response:</h5>
          <pre class="code-block">{{
`{
  "8.8.8.8": {
    "ip": "8.8.8.8",
    "hostname": "dns.google",
    "city": "Mountain View",
    "region": "California",
    "country": "US",
    ...
  },
  "1.1.1.1": {
    "ip": "1.1.1.1",
    "hostname": "one.one.one.one",
    "city": "Los Angeles",
    "region": "California",
    "country": "US",
    ...
  }
}`
          }}</pre>
        </div>
      </div>
      
      <div class="endpoint">
        <h4>Health Check</h4>
        <div class="endpoint-details">
          <div class="method">GET</div>
          <div class="url">{{ baseUrl }}/health</div>
        </div>
        <p>Checks if the API is running properly.</p>
        <div class="example-wrapper">
          <h5>Example Request:</h5>
          <div class="code-block">curl {{ baseUrl }}/health</div>
          
          <h5>Example Response:</h5>
          <pre class="code-block">{{
`{
  "status": "ok",
  "timestamp": "2025-04-18T14:30:00.123456"
}`
          }}</pre>
        </div>
      </div>
    </div>
    
    <div class="section">
      <h3>Response Format</h3>
      <p>All responses are returned in JSON format with the following fields (when available):</p>
      
      <table class="response-fields">
        <thead>
          <tr>
            <th>Field</th>
            <th>Description</th>
            <th>Example</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>ip</td>
            <td>IP address</td>
            <td>8.8.8.8</td>
          </tr>
          <tr>
            <td>hostname</td>
            <td>Reverse DNS of the IP</td>
            <td>dns.google</td>
          </tr>
          <tr>
            <td>city</td>
            <td>City name</td>
            <td>Mountain View</td>
          </tr>
          <tr>
            <td>region</td>
            <td>Region/state</td>
            <td>California</td>
          </tr>
          <tr>
            <td>country</td>
            <td>Country code (ISO 3166-1 alpha-2)</td>
            <td>US</td>
          </tr>
          <tr>
            <td>loc</td>
            <td>Latitude,longitude</td>
            <td>37.4056,-122.0775</td>
          </tr>
          <tr>
            <td>org</td>
            <td>Organization name</td>
            <td>Google LLC</td>
          </tr>
          <tr>
            <td>postal</td>
            <td>Postal/ZIP code</td>
            <td>94043</td>
          </tr>
          <tr>
            <td>timezone</td>
            <td>Timezone (IANA format)</td>
            <td>America/Los_Angeles</td>
          </tr>
          <tr>
            <td>asn</td>
            <td>Autonomous System Number</td>
            <td>AS15169</td>
          </tr>
          <tr>
            <td>asn_org</td>
            <td>Organization associated with ASN</td>
            <td>Google LLC</td>
          </tr>
          <tr>
            <td>is_vpn</td>
            <td>Whether IP is a known VPN</td>
            <td>false</td>
          </tr>
          <tr>
            <td>is_proxy</td>
            <td>Whether IP is a known proxy</td>
            <td>false</td>
          </tr>
          <tr>
            <td>is_hosting</td>
            <td>Whether IP belongs to a hosting provider</td>
            <td>true</td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <div class="section">
      <h3>Error Handling</h3>
      <p>The API returns standard HTTP status codes:</p>
      
      <table class="error-codes">
        <thead>
          <tr>
            <th>Status Code</th>
            <th>Description</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>200</td>
            <td>Success</td>
          </tr>
          <tr>
            <td>400</td>
            <td>Bad request (invalid IP or parameter)</td>
          </tr>
          <tr>
            <td>404</td>
            <td>Not found (field not found)</td>
          </tr>
          <tr>
            <td>429</td>
            <td>Too many requests (rate limit exceeded)</td>
          </tr>
          <tr>
            <td>500</td>
            <td>Internal server error</td>
          </tr>
        </tbody>
      </table>
      
      <div class="example-wrapper">
        <h5>Example Error Response:</h5>
        <pre class="code-block">{{
`{
  "detail": "Invalid IP address or hostname"
}`
        }}</pre>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ApiDocs',
  data() {
    return {
      baseUrl: '/api'
    }
  }
}
</script>

<style scoped>
.docs-container {
  max-width: 900px;
  margin: 0 auto;
  background-color: white;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.intro {
  font-size: 1.1rem;
  margin-bottom: 2rem;
}

.section {
  margin-bottom: 3rem;
}

.section h3 {
  color: #3498db;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
  margin-bottom: 1.5rem;
}

.code-block {
  background-color: #2c3e50;
  color: #ecf0f1;
  padding: 1rem;
  border-radius: 4px;
  font-family: monospace;
  overflow-x: auto;
}

pre.code-block {
  white-space: pre-wrap;
  word-break: break-all;
}

.endpoint {
  margin-bottom: 2rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 1.5rem;
  border-left: 4px solid #3498db;
}

.endpoint h4 {
  margin-top: 0;
  color: #2c3e50;
  margin-bottom: 1rem;
}

.endpoint-details {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.method {
  background-color: #3498db;
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: bold;
  margin-right: 1rem;
  font-family: monospace;
}

.url {
  font-family: monospace;
  background-color: #ecf0f1;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  color: #2c3e50;
}

.example-wrapper {
  margin-top: 1rem;
}

.example-wrapper h5 {
  margin-bottom: 0.5rem;
  color: #7f8c8d;
}

.note {
  background-color: #fdf6e3;
  padding: 0.75rem;
  border-radius: 4px;
  margin-top: 1rem;
  border-left: 4px solid #f39c12;
}

.note p {
  margin: 0;
  color: #b58900;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}

th {
  background-color: #3498db;
  color: white;
  text-align: left;
  padding: 0.75rem;
}

td {
  padding: 0.75rem;
  border-bottom: 1px solid #eee;
}

tr:nth-child(even) {
  background-color: #f9f9f9;
}

tr:hover {
  background-color: #f0f0f0;
}

@media (max-width: 768px) {
  .docs-container {
    padding: 1rem;
  }
  
  .endpoint-details {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .method {
    margin-bottom: 0.5rem;
  }
  
  table {
    display: block;
    overflow-x: auto;
  }
}
</style>