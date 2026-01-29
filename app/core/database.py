from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os
from urllib.parse import quote_plus

# MongoDB connection settings - read at module load time
_MONGODB_URL_RAW = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")

def encode_mongodb_url(url: str) -> str:
    """
    Encode MongoDB URL credentials according to RFC 3986.
    This is CRITICAL - MongoDB driver requires credentials to be percent-encoded.
    """
    if not url:
        return url
    
    # If already encoded (has % signs), return as-is
    if "%" in url:
        return url
    
    # Must have @ to have credentials
    if "@" not in url:
        return url
    
    try:
        # Split protocol from rest
        if url.startswith("mongodb+srv://"):
            protocol = "mongodb+srv://"
            rest = url[14:]  # len("mongodb+srv://") = 14
        elif url.startswith("mongodb://"):
            protocol = "mongodb://"
            rest = url[10:]  # len("mongodb://") = 10
        else:
            return url
        
        # Split credentials from host
        at_index = rest.find("@")
        if at_index == -1:
            return url
        
        credentials = rest[:at_index]
        host = rest[at_index + 1:]
        
        # Split username and password
        colon_index = credentials.find(":")
        if colon_index == -1:
            # No password, just username
            username = credentials
            password = ""
        else:
            username = credentials[:colon_index]
            password = credentials[colon_index + 1:]
        
        # Encode username and password
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password) if password else ""
        
        # Reconstruct URL
        if password:
            encoded_credentials = f"{encoded_username}:{encoded_password}"
        else:
            encoded_credentials = encoded_username
        
        encoded_url = f"{protocol}{encoded_credentials}@{host}"
        return encoded_url
        
    except Exception as e:
        print(f"ERROR encoding MongoDB URL: {e}")
        return url

# CRITICAL: Encode URL immediately at module load time
print(f"[STARTUP] Loading MongoDB configuration...")
MONGODB_URL = encode_mongodb_url(_MONGODB_URL_RAW)
print(f"[STARTUP] MongoDB URL configured (encoding applied if needed)")

# Global MongoDB client
mongodb_client: Optional[AsyncIOMotorClient] = None

# Get database instance
def get_database():
    """Get MongoDB database instance"""
    return mongodb_client[DATABASE_NAME]

# Get specific collection
def get_collection(collection_name: str):
    """Get a specific MongoDB collection"""
    db = get_database()
    return db[collection_name]

# Initialize MongoDB connection
async def connect_to_mongo():
    """Connect to MongoDB on startup"""
    global mongodb_client
    try:
        print(f"[MONGO] Connecting to MongoDB...")
        print(f"[MONGO] Database: {DATABASE_NAME}")
        
        # Use the pre-encoded MONGODB_URL
        mongodb_client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        
        # Verify connection
        await mongodb_client.admin.command('ping')
        print(f"[MONGO] ✅ Connected to MongoDB successfully")
        print(f"[MONGO] ✅ Using database: {DATABASE_NAME}")
        
        # Create indexes for better performance
        await create_indexes()
        print(f"[MONGO] ✅ Database indexes created")
    except Exception as e:
        print(f"[MONGO] ❌ FAILED to connect to MongoDB")
        print(f"[MONGO] Error: {e}")
        print(f"[MONGO] Make sure MONGODB_URL environment variable is set correctly")
        raise

# Close MongoDB connection
async def close_mongo_connection():
    """Close MongoDB connection on shutdown"""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("✅ MongoDB connection closed")

# Create database indexes
async def create_indexes():
    """Create indexes for all collections"""
    db = get_database()
    
    # Users collection indexes
    await db.users.create_index("phone", unique=True)
    await db.users.create_index("email", unique=True, sparse=True)
    await db.users.create_index([("city", 1), ("state", 1)])
    await db.users.create_index([("latitude", 1), ("longitude", 1)])
    
    # Venues collection indexes
    await db.venues.create_index("city")
    await db.venues.create_index([("latitude", 1), ("longitude", 1)])
    await db.venues.create_index("is_active")
    
    # Tournaments collection indexes
    await db.tournaments.create_index("city")
    await db.tournaments.create_index("sport_type")
    await db.tournaments.create_index([("latitude", 1), ("longitude", 1)])
    await db.tournaments.create_index("status")
    
    # Shops collection indexes
    await db.shops.create_index("city")
    await db.shops.create_index("category")
    await db.shops.create_index([("latitude", 1), ("longitude", 1)])
    
    # Jobs collection indexes
    await db.jobs.create_index("city")
    await db.jobs.create_index("job_type")
    await db.jobs.create_index("status")
    
    # Dictionary collection indexes
    await db.dictionary.create_index("sport")
    await db.dictionary.create_index("term")
    await db.dictionary.create_index("city")
    await db.dictionary.create_index("slug", unique=True, sparse=True)
    
    # Bookings collection indexes
    await db.bookings.create_index("booking_number", unique=True)
    await db.bookings.create_index("user_id")
    await db.bookings.create_index("venue_id")
    await db.bookings.create_index([("booking_date", 1), ("venue_id", 1)])

# Dependency to get DB (for compatibility with existing code)
async def get_db():
    """Get database instance - for dependency injection"""
    return get_database()

# Initialize database
async def init_db():
    """Initialize database connection"""
    await connect_to_mongo()
