#!/usr/bin/env python3
import os
import requests
import tarfile
import zipfile
import gzip
import time
import logging
import shutil
import os.path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ipinfo-updater')

# Environment variables
DB_USER = os.getenv("DB_USER", "ipuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ippassword")
DB_HOST = os.getenv("DB_HOST", "ipinfo-db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ipinfodb")
UPDATE_INTERVAL = int(os.getenv("UPDATE_INTERVAL", "86400"))  # Default: daily
LICENSE_KEY = os.getenv("MAXMIND_LICENSE_KEY", "")  # Get this from environment variable

# Paths
DATA_DIR = "/app/data"
TEMP_DIR = "/app/data/temp"
GEOLITE2_CITY_DB = os.path.join(DATA_DIR, "GeoLite2-City.mmdb")
GEOLITE2_ASN_DB = os.path.join(DATA_DIR, "GeoLite2-ASN.mmdb")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# Function to download MaxMind GeoLite2 databases
def download_maxmind_databases():
    """
    Downloads MaxMind GeoLite2 City and ASN databases.
    """
    logger.info("Downloading MaxMind GeoLite2 databases")
    
    # Check if license key is provided
    if not LICENSE_KEY:
        logger.warning("No MaxMind license key provided. Using dummy database files for testing purposes.")
        logger.warning("For production use, sign up for a MaxMind account and set the MAXMIND_LICENSE_KEY environment variable")
        
        # Create dummy city database if it doesn't exist
        if not os.path.exists(GEOLITE2_CITY_DB):
            try:
                # Create an empty file for the city database
                with open(GEOLITE2_CITY_DB, 'wb') as f:
                    f.write(b'dummy city database')
                logger.info(f"Created dummy city database at {GEOLITE2_CITY_DB}")
            except Exception as e:
                logger.error(f"Failed to create dummy city database: {e}")
        
        # Create dummy ASN database if it doesn't exist
        if not os.path.exists(GEOLITE2_ASN_DB):
            try:
                # Create an empty file for the ASN database
                with open(GEOLITE2_ASN_DB, 'wb') as f:
                    f.write(b'dummy asn database')
                logger.info(f"Created dummy ASN database at {GEOLITE2_ASN_DB}")
            except Exception as e:
                logger.error(f"Failed to create dummy ASN database: {e}")
        
        return
    
    # URLs for the databases
    city_url = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key={LICENSE_KEY}&suffix=tar.gz"
    asn_url = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-ASN&license_key={LICENSE_KEY}&suffix=tar.gz"
    
    # Download and extract City database
    try:
        logger.info("Downloading City database")
        city_temp_file = os.path.join(TEMP_DIR, "GeoLite2-City.tar.gz")
        
        # Download the database
        response = requests.get(city_url, stream=True)
        if response.status_code != 200:
            logger.error(f"Failed to download City database. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            raise Exception("Download failed")
            
        with open(city_temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract the database
        logger.info("Extracting City database")
        with tarfile.open(city_temp_file) as tar:
            # Find the .mmdb file in the archive
            mmdb_file = None
            for member in tar.getmembers():
                if member.name.endswith('.mmdb'):
                    mmdb_file = member
                    break
            
            if mmdb_file:
                # Extract the file to a temporary location
                tar.extract(mmdb_file, path=TEMP_DIR)
                # Move the file to the final location with the standard name
                source_path = os.path.join(TEMP_DIR, mmdb_file.name)
                shutil.move(source_path, GEOLITE2_CITY_DB)
                logger.info(f"Extracted City database to {GEOLITE2_CITY_DB}")
            else:
                logger.error("No .mmdb file found in the City database archive")
        
        # Clean up
        os.remove(city_temp_file)
        logger.info("City database updated successfully")
        
    except Exception as e:
        logger.error(f"Failed to download or extract City database: {e}")
    
    # Download and extract ASN database
    try:
        logger.info("Downloading ASN database")
        asn_temp_file = os.path.join(TEMP_DIR, "GeoLite2-ASN.tar.gz")
        
        # Download the database
        response = requests.get(asn_url, stream=True)
        if response.status_code != 200:
            logger.error(f"Failed to download ASN database. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            raise Exception("Download failed")
            
        with open(asn_temp_file, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract the database
        logger.info("Extracting ASN database")
        with tarfile.open(asn_temp_file) as tar:
            # Find the .mmdb file in the archive
            mmdb_file = None
            for member in tar.getmembers():
                if member.name.endswith('.mmdb'):
                    mmdb_file = member
                    break
            
            if mmdb_file:
                # Extract the file to a temporary location
                tar.extract(mmdb_file, path=TEMP_DIR)
                # Move the file to the final location with the standard name
                source_path = os.path.join(TEMP_DIR, mmdb_file.name)
                shutil.move(source_path, GEOLITE2_ASN_DB)
                logger.info(f"Extracted ASN database to {GEOLITE2_ASN_DB}")
            else:
                logger.error("No .mmdb file found in the ASN database archive")
        
        # Clean up
        os.remove(asn_temp_file)
        logger.info("ASN database updated successfully")
        
    except Exception as e:
        logger.error(f"Failed to download or extract ASN database: {e}")

# Function to download IP-to-ASN mapping and VPN/Proxy lists
def download_ip_lists():
    """
    Downloads additional IP lists for enhanced functionality:
    - VPN/Proxy detection lists
    - Hosting provider lists
    """
    logger.info("Downloading additional IP lists")
    
    # Example: Download VPN/Proxy list (replace with actual source)
    vpn_proxy_file = os.path.join(DATA_DIR, "vpn_proxy_list.txt")
    try:
        # For demonstration - in production, replace with actual list source
        with open(vpn_proxy_file, 'w') as f:
            f.write("# VPN/Proxy IP addresses\n")
            f.write("# This is a dummy file for demonstration\n")
        logger.info(f"Created dummy VPN/Proxy list at {vpn_proxy_file}")
    except Exception as e:
        logger.error(f"Failed to create VPN/Proxy list: {e}")
    
    # Example: Download hosting provider list (replace with actual source)
    hosting_file = os.path.join(DATA_DIR, "hosting_providers.txt")
    try:
        # For demonstration - in production, replace with actual list source
        with open(hosting_file, 'w') as f:
            f.write("# Hosting provider IP ranges\n")
            f.write("# This is a dummy file for demonstration\n")
        logger.info(f"Created dummy hosting provider list at {hosting_file}")
    except Exception as e:
        logger.error(f"Failed to create hosting provider list: {e}")

# Main function
def main():
    logger.info("Starting IP database updater service")
    
    while True:
        try:
            # Download databases
            download_maxmind_databases()
            download_ip_lists()
            
            # Log success
            logger.info(f"Database update completed, next update in {UPDATE_INTERVAL} seconds")
            
            # Wait for the next update
            time.sleep(UPDATE_INTERVAL)
            
        except Exception as e:
            logger.error(f"Error in update process: {e}")
            # Wait a shorter time before retrying on error
            time.sleep(3600)  # 1 hour

if __name__ == "__main__":
    main()