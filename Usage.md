[< Back to README](../README.md)

# IP Info - Usage Guide

This guide provides information on how to use the IP Info service, both through its web user interface (UI) and its RESTful API.

## Web UI Usage

Once the IP Info service is running, you can access its web UI to perform quick IP lookups:

1.  Open your web browser.
2.  Navigate to `http://localhost:8081` (or the IP address/hostname and port where your UI is exposed).
3.  Enter an IP address in the provided input field and press Enter or click the lookup button.
4.  The UI will display detailed information for the entered IP address.

## API Usage

The IP Info service exposes a RESTful API that allows you to programmatically retrieve IP information. The API is accessible at `http://localhost:8080` (or the IP address/hostname and port where your API is exposed).

### API Endpoints

| Endpoint                  | Description                               |
| :------------------------ | :---------------------------------------- |
| `/`                       | Get information about your own IP address. |
| `/{ip_address}`           | Get information about a specific IP address. |
| `/ip/{ip_address}`        | Alternative endpoint for IP lookup.       |
| `/field/{ip_address}/{field}` | Get a specific field for an IP address (e.g., `/field/8.8.8.8/country`). |
| `/bulk?ips=ip1,ip2,ip3`   | Perform a bulk lookup for multiple IP addresses (comma-separated). |
| `/health`                 | Health check endpoint to verify API status. |

### Example API Response

Here's an example of the JSON response you can expect from an IP lookup:

```json
{
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
}
```

### Making API Requests

You can use tools like `curl` or any programming language's HTTP client to interact with the API.

**Example using `curl`:**

```bash
curl http://localhost:8080/8.8.8.8
```

This will return the JSON response for the IP address `8.8.8.8`.