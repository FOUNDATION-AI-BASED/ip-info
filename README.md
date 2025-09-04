# IP Info - Self-Hosted IP Information Service

Welcome to IP Info, a powerful and self-hosted solution for retrieving comprehensive IP address information. This project provides a Docker-based alternative to services like ipinfo.io, giving you full control over your IP data and infrastructure.

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](Installation.md)
- [Usage](Usage.md)
- [API Endpoints](API.md)
- [Configuration](Configuration.md)
- [How It Works](HowItWorks.md)
- [Troubleshooting](Troubleshooting.md)
- [Production Deployment](ProductionDeployment.md)
- [License](#license)

## Features

- **Complete IP Information**: Get detailed data about any IP address, including geolocation, ASN, and network details.
- **Self-Hosted**: Maintain full control and privacy over your IP data.
- **Easy Deployment**: Simple setup using Docker and Docker Compose.
- **User-Friendly Interface**: A web UI for convenient IP lookups.
- **Fast & Reliable API**: A RESTful API with JSON responses for programmatic access.
- **IPv4 & IPv6 Support**: Comprehensive support for both IP protocols.
- **Caching System**: Redis-based caching for enhanced performance.

## Quick Start

Get your IP Info service up and running in minutes:

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/ip-info.git
    cd ip-info
    ```

2.  **Build and start the services**:
    ```bash
    docker compose build
    docker compose up -d
    ```

3.  **Access the Web UI**:
    Open your browser and navigate to `http://localhost:8081`.

For detailed installation instructions, including MaxMind GeoLite2 setup, please refer to the [Installation Guide](Installation.md).

## License

This project is open source and available under the [MIT License](LICENSE).