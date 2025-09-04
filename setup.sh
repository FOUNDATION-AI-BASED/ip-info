#!/bin/bash

# Self-Hosted IP Info Service Setup Script
echo "Setting up Self-Hosted IP Info Service..."

# Create required directories
echo "Creating directories..."
mkdir -p api
mkdir -p updater
mkdir -p ui
mkdir -p ui/src
mkdir -p ui/src/views
mkdir -p ui/src/components
mkdir -p data

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create API files
echo "Creating API files..."
cat > api/Dockerfile << 'EOL'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create data directory if it doesn't exist
RUN mkdir -p /app/data

# Expose API port
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
EOL

cat > api/requirements.txt << 'EOL'
fastapi==0.104.1
uvicorn==0.23.2
sqlalchemy==2.0.22
psycopg2-binary==2.9.9
redis==5.0.1
pydantic==2.4.2
python-dotenv==1.0.0
geoip2==4.7.0
aiohttp==3.8.6
ipaddress==1.0.23
python-multipart==0.0.6
maxminddb==2.4.0
python-whois==0.8.0
ratelimit==2.2.1
EOL

# Copy main.py from the template
echo "Copying main API application..."
cp ../api-main/main.py api/

# Create Updater files
echo "Creating Updater files..."
cat > updater/Dockerfile << 'EOL'
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir requests geoip2 psycopg2-binary python-dotenv

# Copy updater script
COPY update_databases.py .

# Create data directory if it doesn't exist
RUN mkdir -p /app/data

# Command to run the updater
CMD ["python", "update_databases.py"]
EOL

# Copy updater script from the template
echo "Copying updater script..."
cp ../updater-script/update_databases.py updater/

# Create UI files
echo "Creating UI files..."
cat > ui/Dockerfile << 'EOL'
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install

# Copy application code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
EOL

cat > ui/nginx.conf << 'EOL'
server {
    listen 80;
    server_name localhost;

    root /usr/share/nginx/html;
    index index.html;

    # Proxy API requests to the API service
    location /api/ {
        proxy_pass http://ipinfo-api:8080/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Serve static files
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Cache control for static assets
    location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
        expires 1d;
        add_header Cache-Control "public";
    }

    # Error pages
    error_page 404 /index.html;
    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
        root /usr/share/nginx/html;
    }
}
EOL

cat > ui/package.json << 'EOL'
{
  "name": "ipinfo-ui",
  "version": "1.0.0",
  "description": "UI for self-hosted IP information service",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "serve": "vite preview"
  },
  "dependencies": {
    "axios": "^1.5.0",
    "vue": "^3.3.4",
    "vue-router": "^4.2.4",
    "leaflet": "^1.9.4"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^4.3.4",
    "vite": "^4.4.9"
  }
}
EOL

cat > ui/vite.config.js << 'EOL'
import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://ipinfo-api:8080',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
});
EOL

cat > ui/index.html << 'EOL'
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Self-Hosted IP Info Service</title>
  <meta name="description" content="A self-hosted alternative to ipinfo.io for IP geolocation and information lookup">
  <link rel="icon" href="/favicon.ico">
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
EOL

# Copy UI component files
echo "Copying UI component files..."
mkdir -p ui/src/views
# Copy component files from templates here

# Create docker-compose.yml
echo "Creating docker-compose.yml..."
cat > docker-compose.yml << 'EOL'
version: '3.8'

services:
  # API service
  ipinfo-api:
    build:
      context: ./api
    ports:
      - "8080:8080"
    volumes:
      - ./data:/app/data
    environment:
      - DB_HOST=ipinfo-db
      - DB_PORT=5432
      - DB_USER=ipuser
      - DB_PASSWORD=ippassword
      - DB_NAME=ipinfodb
      - REDIS_HOST=ipinfo-cache
      - REDIS_PORT=6379
      - LOG_LEVEL=info
      - RATE_LIMIT=100
    depends_on:
      - ipinfo-db
      - ipinfo-cache
    restart: always

  # Database for IP data storage
  ipinfo-db:
    image: postgres:14-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_USER=ipuser
      - POSTGRES_PASSWORD=ippassword
      - POSTGRES_DB=ipinfodb
    restart: always

  # Redis for caching
  ipinfo-cache:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: always

  # Updater service to keep IP databases current
  ipinfo-updater:
    build:
      context: ./updater
    volumes:
      - ./data:/app/data
    environment:
      - DB_HOST=ipinfo-db
      - DB_PORT=5432
      - DB_USER=ipuser
      - DB_PASSWORD=ippassword
      - DB_NAME=ipinfodb
      - UPDATE_INTERVAL=86400  # Update databases daily (in seconds)
    depends_on:
      - ipinfo-db
    restart: always

  # Web UI
  ipinfo-ui:
    build:
      context: ./ui
    ports:
      - "8081:80"
    depends_on:
      - ipinfo-api
    restart: always

volumes:
  postgres_data:
  redis_data:
EOL

# Ask for MaxMind license key
echo
echo "To use this service in production, you need a MaxMind GeoLite2 license key."
read -p "Do you have a MaxMind license key? (y/n): " has_key

if [ "$has_key" = "y" ]; then
    read -p "Enter your MaxMind license key: " maxmind_key
    
    # Update the license key in the updater script
    sed -i "s/YOUR_LICENSE_KEY/$maxmind_key/g" updater/update_databases.py
    echo "MaxMind license key has been configured."
else
    echo "You can add your MaxMind license key later by editing updater/update_databases.py"
    echo "For testing purposes, the system will use dummy data."
fi

echo
echo "Setup completed successfully!"
echo "To start the services, run: docker-compose up -d"
echo "Then access the Web UI at: http://localhost:8081"
echo "The API will be available at: http://localhost:8080"