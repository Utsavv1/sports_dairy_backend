"""
Recreate MongoDB database - drops all collections and recreates indexes
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def recreate_mongodb():
    """Drop all collections and recreate with indexes"""
    try:
        # Get MongoDB connection string
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "sports_diary")
        
        print(f"🔗 Connecting to MongoDB at {mongodb_url}")
        print(f"📊 Database: {database_name}\n")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!\n")
        
        # Get all collections
        collections = await db.list_collection_names()
        
        if collections:
            print(f"🗑️  Dropping {len(collections)} collections...")
            for collection_name in collections:
                await db[collection_name].drop()
                print(f"   ✓ Dropped: {collection_name}")
            print()
        
        # Recreate indexes
        print("🔧 Creating indexes...")
        
        # Users collection indexes
        await db.users.create_index("phone", unique=True)
        await db.users.create_index("email", unique=True, sparse=True)
        await db.users.create_index([("city", 1), ("state", 1)])
        await db.users.create_index([("latitude", 1), ("longitude", 1)])
        print("   ✓ Users indexes created")
        
        # Venues collection indexes
        await db.venues.create_index("city")
        await db.venues.create_index([("latitude", 1), ("longitude", 1)])
        await db.venues.create_index("is_active")
        print("   ✓ Venues indexes created")
        
        # Tournaments collection indexes
        await db.tournaments.create_index("city")
        await db.tournaments.create_index("sport_type")
        await db.tournaments.create_index([("latitude", 1), ("longitude", 1)])
        await db.tournaments.create_index("status")
        print("   ✓ Tournaments indexes created")
        
        # Shops collection indexes
        await db.shops.create_index("city")
        await db.shops.create_index("category")
        await db.shops.create_index([("latitude", 1), ("longitude", 1)])
        print("   ✓ Shops indexes created")
        
        # Jobs collection indexes
        await db.jobs.create_index("city")
        await db.jobs.create_index("job_type")
        await db.jobs.create_index("status")
        print("   ✓ Jobs indexes created")
        
        # Dictionary collection indexes
        await db.dictionary.create_index("sport")
        await db.dictionary.create_index("term")
        await db.dictionary.create_index("city")
        await db.dictionary.create_index("slug", unique=True, sparse=True)
        print("   ✓ Dictionary indexes created")
        
        # Bookings collection indexes
        await db.bookings.create_index("booking_number", unique=True)
        await db.bookings.create_index("user_id")
        await db.bookings.create_index("venue_id")
        await db.bookings.create_index([("booking_date", 1), ("venue_id", 1)])
        print("   ✓ Bookings indexes created")
        
        # Community posts collection indexes
        await db.community_posts.create_index("user_id")
        await db.community_posts.create_index("created_at")
        await db.community_posts.create_index([("city", 1), ("sport_type", 1)])
        print("   ✓ Community posts indexes created")
        
        # Reviews collection indexes
        await db.reviews.create_index("venue_id")
        await db.reviews.create_index("user_id")
        await db.reviews.create_index("created_at")
        print("   ✓ Reviews indexes created")
        
        # Close connection
        client.close()
        print("\n✅ Database recreated successfully!")
        print("📝 All collections dropped and indexes recreated")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("⚠️  WARNING: This will DELETE ALL DATA in the database!")
    response = input("Are you sure you want to continue? (yes/no): ")
    
    if response.lower() == "yes":
        asyncio.run(recreate_mongodb())
    else:
        print("Operation cancelled.")
