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
