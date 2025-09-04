from fastapi import FastAPI, Request, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional, Dict, Any, List
import os
import json
import ipaddress
import time
import socket
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ipinfo-api")

app = FastAPI(title="Self-Hosted IP Info API", 
              description="A self-hosted alternative to ipinfo.io",
              version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
DB_USER = os.getenv("DB_USER", "ipuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ippassword")
DB_HOST = os.getenv("DB_HOST", "ipinfo-db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "ipinfodb")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Path to GeoIP databases
GEOIP_CITY_DB = "/app/data/GeoLite2-City.mmdb"
GEOIP_ASN_DB = "/app/data/GeoLite2-ASN.mmdb"

# Check database availability
logger.info(f"Checking for GeoIP databases")
logger.info(f"City DB path: {GEOIP_CITY_DB}")
logger.info(f"ASN DB path: {GEOIP_ASN_DB}")

if os.path.exists(GEOIP_CITY_DB):
    logger.info(f"City DB exists, size: {os.path.getsize(GEOIP_CITY_DB)} bytes")
else:
    logger.warning(f"City DB does not exist")

if os.path.exists(GEOIP_ASN_DB):
    logger.info(f"ASN DB exists, size: {os.path.getsize(GEOIP_ASN_DB)} bytes")
else:
    logger.warning(f"ASN DB does not exist")

# Check if databases exist and are valid
use_real_databases = False
try:
    import geoip2.database
    if os.path.exists(GEOIP_CITY_DB) and os.path.exists(GEOIP_ASN_DB):
        # Test open each database
        try:
            with geoip2.database.Reader(GEOIP_CITY_DB) as reader:
                logger.info("Successfully opened City database")
            use_real_databases = True
        except Exception as e:
            logger.error(f"Failed to open City database: {e}")
        
        try:
            with geoip2.database.Reader(GEOIP_ASN_DB) as reader:
                logger.info("Successfully opened ASN database")
            use_real_databases = True
        except Exception as e:
            logger.error(f"Failed to open ASN database: {e}")
        
        if use_real_databases:
            logger.info("Using real GeoIP databases")
        else:
            logger.warning("Failed to open one or both databases")
    else:
        logger.warning("One or both GeoIP databases do not exist")
except Exception as e:
    logger.error(f"Error checking GeoIP databases: {e}")

# Database models
class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    user_email = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    request_count = Column(Integer, default=0)
    last_used = Column(DateTime, default=None, nullable=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper function to validate IP
def is_valid_ip(ip_str):
    try:
        ipaddress.ip_address(ip_str)
        return True
    except ValueError:
        return False

# Helper function to get IP info - NO CACHING
def get_ip_info(ip_address: str) -> Dict[str, Any]:
    # No cache check - caching disabled
    logger.info(f"Looking up IP {ip_address} (no cache)")
    
    # Initialize result dict with empty values
    result = {
        "ip": ip_address,
        "hostname": None,
        "city": None,
        "region": None,
        "country": None,
        "loc": None,
        "org": None,
        "postal": None,
        "timezone": None,
        "asn": None,
        "asn_org": None,
        "is_vpn": False,
        "is_proxy": False,
        "is_hosting": False
    }
    
    # Get hostname
    try:
        hostname = socket.gethostbyaddr(ip_address)[0]
        result["hostname"] = hostname
    except:
        pass
    
    # Try to use real databases
    try:
        import geoip2.database
        
        # Test if City database exists and works
        if os.path.exists(GEOIP_CITY_DB):
            try:
                with geoip2.database.Reader(GEOIP_CITY_DB) as reader:
                    response = reader.city(ip_address)
                    logger.info(f"Got City data for {ip_address}")
                    
                    if response.city.name:
                        result["city"] = response.city.name
                    
                    if response.subdivisions.most_specific.name:
                        result["region"] = response.subdivisions.most_specific.name
                    
                    if response.country.iso_code:
                        result["country"] = response.country.iso_code
                    
                    if response.location.latitude and response.location.longitude:
                        result["loc"] = f"{response.location.latitude},{response.location.longitude}"
                    
                    if response.postal.code:
                        result["postal"] = response.postal.code
                    
                    if response.location.time_zone:
                        result["timezone"] = response.location.time_zone
            except Exception as e:
                logger.error(f"Error getting City data for {ip_address}: {e}")
        
        # Test if ASN database exists and works
        if os.path.exists(GEOIP_ASN_DB):
            try:
                with geoip2.database.Reader(GEOIP_ASN_DB) as reader:
                    response = reader.asn(ip_address)
                    logger.info(f"Got ASN data for {ip_address}")
                    
                    if response.autonomous_system_number:
                        result["asn"] = f"AS{response.autonomous_system_number}"
                    
                    if response.autonomous_system_organization:
                        result["asn_org"] = response.autonomous_system_organization
                        result["org"] = response.autonomous_system_organization
            except Exception as e:
                logger.error(f"Error getting ASN data for {ip_address}: {e}")
    
    except ImportError as e:
        logger.error(f"Error importing geoip2: {e}")
    except Exception as e:
        logger.error(f"Unexpected error processing IP {ip_address}: {e}")
    
    # Debug log the result
    logger.info(f"IP data for {ip_address}: {json.dumps(result)}")
    
    # No caching - just return the result
    return result

# Routes
@app.get("/")
async def get_own_ip(request: Request):
    client_ip = request.client.host
    try:
        return get_ip_info(client_ip)
    except Exception as e:
        logger.error(f"Error processing IP {client_ip}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing IP: {str(e)}")

@app.get("/ip/{ip_address}")
async def get_ip_data(ip_address: str, request: Request):
    if not is_valid_ip(ip_address):
        try:
            # Try to resolve hostname to IP
            ip_address = socket.gethostbyname(ip_address)
        except:
            raise HTTPException(status_code=400, detail="Invalid IP address or hostname")
    
    try:
        return get_ip_info(ip_address)
    except Exception as e:
        logger.error(f"Error processing IP {ip_address}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing IP: {str(e)}")

@app.get("/{ip_address}")
async def get_ip_direct(ip_address: str, request: Request):
    if not is_valid_ip(ip_address):
        try:
            # Try to resolve hostname to IP
            ip_address = socket.gethostbyname(ip_address)
        except:
            raise HTTPException(status_code=400, detail="Invalid IP address or hostname")
    
    try:
        return get_ip_info(ip_address)
    except Exception as e:
        logger.error(f"Error processing IP {ip_address}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing IP: {str(e)}")

@app.get("/field/{ip_address}/{field}")
async def get_ip_field(ip_address: str, field: str, request: Request):
    if not is_valid_ip(ip_address):
        try:
            # Try to resolve hostname to IP
            ip_address = socket.gethostbyname(ip_address)
        except:
            raise HTTPException(status_code=400, detail="Invalid IP address or hostname")
    
    try:
        ip_data = get_ip_info(ip_address)
        
        if field not in ip_data:
            raise HTTPException(status_code=404, detail=f"Field '{field}' not found")
        
        return {field: ip_data[field]}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing IP {ip_address}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing IP: {str(e)}")

@app.get("/bulk")
async def bulk_ip_lookup(request: Request, ips: str = Query(..., description="Comma-separated list of IP addresses")):
    ip_list = [ip.strip() for ip in ips.split(",")]
    
    if len(ip_list) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 IPs per request")
    
    results = {}
    for ip in ip_list:
        if is_valid_ip(ip):
            try:
                results[ip] = get_ip_info(ip)
            except Exception as e:
                results[ip] = {"error": str(e)}
        else:
            results[ip] = {"error": "Invalid IP address"}
    
    return results

@app.get("/health")
async def health_check():
    db_status = {
        "city_db_exists": os.path.exists(GEOIP_CITY_DB),
        "asn_db_exists": os.path.exists(GEOIP_ASN_DB)
    }
    
    if db_status["city_db_exists"]:
        db_status["city_db_size"] = os.path.getsize(GEOIP_CITY_DB)
    
    if db_status["asn_db_exists"]:
        db_status["asn_db_size"] = os.path.getsize(GEOIP_ASN_DB)
    
    return {
        "status": "ok", 
        "timestamp": datetime.utcnow().isoformat(),
        "databases": db_status,
        "caching": "disabled"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)