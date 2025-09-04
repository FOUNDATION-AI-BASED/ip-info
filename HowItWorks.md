[< Back to README](../README.md)

# How It Works

The `ip-info` tool is designed to provide comprehensive IP address information by leveraging various data sources and a modular architecture. This section details the core components and their interactions.

## Architecture Overview

The system consists of three main components:

1.  **API Service (`api`)**: A Python-based Flask application that serves IP information. It queries various databases and external APIs to gather data.
2.  **UI Service (`ui`)**: A Vue.js frontend application that provides a user-friendly interface for querying IP addresses and displaying the results.
3.  **Updater Service (`updater`)**: A Python script responsible for periodically updating the MaxMind GeoLite2 databases, ensuring the IP information is always current.

## Data Sources

`ip-info` utilizes the following data sources:

*   **MaxMind GeoLite2 Databases**: These local databases provide geographical information (country, city, ASN) for IP addresses. The `updater` service ensures these databases are kept up-to-date.
*   **External APIs**: For certain information not available in local databases (e.g., abuse contact, reverse DNS), the API service may query external services.

## Request Flow

When a user queries an IP address through the UI:

1.  The UI sends a request to the API service.
2.  The API service receives the request and performs the following:
    *   Queries the local MaxMind GeoLite2 databases for geographical and ASN information.
    *   (Optionally) Queries external APIs for additional data.
    *   Aggregates the information from all sources.
3.  The API service returns the combined IP information to the UI.
4.  The UI displays the information to the user in a structured and readable format.

## Database Updates

The `updater` service runs periodically (e.g., daily via a cron job or Docker Compose service) to:

1.  Download the latest GeoLite2 City and ASN databases from MaxMind.
2.  Decompress and store these databases in a location accessible by the API service.

This ensures that the IP information provided by the service is always based on the most recent data available.