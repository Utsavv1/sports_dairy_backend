import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def check_mongodb_schema():
    """Check MongoDB collections and their schema"""
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
        print(f"📂 Collections in database: {collections}\n")
        
        # Check each collection
        for collection_name in collections:
            collection = db[collection_name]
            count = await collection.count_documents({})
            print(f"\n{'='*60}")
            print(f"Collection: {collection_name}")
            print(f"{'='*60}")
            print(f"Document count: {count}")
            
            # Get a sample document to show schema
            if count > 0:
                sample = await collection.find_one()
                if sample:
                    print(f"\nSample document structure:")
                    for key in sample.keys():
                        value_type = type(sample[key]).__name__
                        print(f"  - {key}: {value_type}")
            
            # Get indexes
            indexes = await collection.index_information()
            if indexes:
                print(f"\nIndexes:")
                for index_name, index_info in indexes.items():
                    print(f"  - {index_name}: {index_info.get('key', [])}")
        
        # Close connection
        client.close()
        print("\n" + "="*60)
        print("✅ Database check complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_mongodb_schema())
