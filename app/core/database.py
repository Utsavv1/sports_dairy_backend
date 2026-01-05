from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import os

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")

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
        mongodb_client = AsyncIOMotorClient(MONGODB_URL)
        # Verify connection
        await mongodb_client.admin.command('ping')
        print(f"✅ Connected to MongoDB at {MONGODB_URL}")
        print(f"✅ Using database: {DATABASE_NAME}")
        
        # Create indexes for better performance
        await create_indexes()
        print("✅ Database indexes created")
    except Exception as e:
        print(f"❌ Error connecting to MongoDB: {e}")
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
