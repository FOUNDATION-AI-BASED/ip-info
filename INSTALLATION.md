[< Back to README](../README.md)

# Self-Hosted IP Info - Installation Guide

This guide will walk you through the process of setting up your own self-hosted IP information service as an alternative to ipinfo.io.

## Prerequisites

Before you begin, make sure you have:

- A server with Docker and Docker Compose installed
- At least 2GB of RAM and 10GB of storage space
- Basic knowledge of command-line operations
- (Optional but recommended) A MaxMind account with a license key

## Installation Options

### Option 1: Quick Setup (Recommended)

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/self-hosted-ipinfo.git
    cd self-hosted-ipinfo
    ```

2.  **Run the setup script:**
    ```bash
    chmod +x setup.sh
    ./setup.sh
    ```

3.  **Follow the prompts** to configure your installation. You'll be asked to provide your MaxMind license key if you have one.

4.  **Start the services:**
    ```bash
    docker-compose up -d
    ```

5.  **Access the service:**
    - Web UI: http://your-server-ip:8081
    - API: http://your-server-ip:8080

### Option 2: Manual Setup

If you prefer to set up everything manually or customize the installation, follow these steps:

1.  **Create the project structure:**
    ```bash
    mkdir -p self-hosted-ipinfo/{api,updater,ui,data}
    cd self-hosted-ipinfo
    ```

2.  **Create Docker Compose file:**
    Copy the `docker-compose.yml` file from the repository or create it according to the provided template.

3.  **Set up API service:**
    - Create the `api/Dockerfile` and `api/requirements.txt` files
    - Copy the `api/main.py` file to implement the API endpoints

4.  **Set up Updater service:**
    - Create the `updater/Dockerfile` file
    - Create the `updater/update_databases.py` script
    - If you have a MaxMind license key, add it to the script

5.  **Set up Web UI:**
    - Create the `ui/Dockerfile` and related configuration files
    - Set up the Vue.js application

6.  **Start the services:**
    ```bash
    docker-compose up -d
    ```

## Post-Installation Configuration

### Securing Your Installation

For production use, consider the following security measures:

1.  **Set up HTTPS:**
    - Use a reverse proxy like Nginx with Let's Encrypt certificates
    - Configure proper SSL/TLS settings

2.  **Change default credentials:**
    - Modify the database username and password in `docker-compose.yml`

3.  **Implement API authentication:**
    - Add API key verification to the FastAPI application
    - Restrict access to trusted clients

### MaxMind Database Setup

If you haven't added your MaxMind license key during installation:

1.  Sign up for a free account at [MaxMind](https://www.maxmind.com/en/geolite2/signup)
2.  Generate a license key
3.  Edit `updater/update_databases.py` and replace `YOUR_LICENSE_KEY` with your actual key
4.  Restart the updater service:
    ```bash
    docker-compose restart ipinfo-updater
    ```

## Troubleshooting

### Common Issues

**Database updater fails to download GeoIP databases:**
- Verify your MaxMind license key is correct
- Check network connectivity to MaxMind servers
- Examine logs with `docker-compose logs ipinfo-updater`

**API returns no data or incomplete data:**
- Ensure the database updater has run successfully
- Check if the databases exist in the `data` directory
- Verify database connectivity with `docker-compose logs ipinfo-api`

**Web UI shows connection errors:**
- Confirm the API service is running properly
- Check network settings and port forwarding
- Verify that the nginx configuration is correct

### Viewing Logs

To view logs for troubleshooting:

```bash
# View logs for all services
docker-compose logs

# View logs for a specific service
docker-compose logs ipinfo-api
docker-compose logs ipinfo-updater
docker-compose logs ipinfo-ui

# Follow logs in real-time
docker-compose logs -f
```

## Upgrading

To upgrade your installation:

1.  Pull the latest changes:
    ```bash
    git pull
    ```

2.  Rebuild and restart the services:
    ```bash
    docker-compose down
    docker-compose build
    docker-compose up -d
    ```

## Conclusion

Your self-hosted IP information service should now be up and running. You can use it as a drop-in replacement for ipinfo.io in your applications by changing the API endpoint URLs.

For further assistance or to report issues, please visit the repository's issue tracker.