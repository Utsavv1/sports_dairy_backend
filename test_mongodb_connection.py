"""
Test MongoDB Connection
Run this to verify MongoDB is running and accessible
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient

async def test_connection():
    # Set UTF-8 encoding for console
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass
    
    print("\n" + "="*60)
    print("  Testing MongoDB Connection")
    print("="*60)
    
    MONGODB_URL = "mongodb://localhost:27017"
    DATABASE_NAME = "sports_diary"
    
    print(f"\nConnecting to: {MONGODB_URL}")
    print(f"Database: {DATABASE_NAME}")
    
    try:
        # Create client
        client = AsyncIOMotorClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
        
        # Test connection with ping
        print("\nPinging MongoDB server...")
        await client.admin.command('ping')
        
        print("SUCCESS! MongoDB is running and accessible!")
        
        # Get database
        db = client[DATABASE_NAME]
        
        # List collections
        collections = await db.list_collection_names()
        print(f"\nCollections in '{DATABASE_NAME}' database:")
        if collections:
            for collection in collections:
                count = await db[collection].count_documents({})
                print(f"   - {collection}: {count} documents")
        else:
            print("   (No collections yet - run seed_mongodb.py to create data)")
        
        print("\n" + "="*60)
        print("  MongoDB Connection Test PASSED!")
        print("="*60)
        print("\nYour backend will connect successfully!")
        print("   Run: python run.py\n")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"\nCONNECTION FAILED!")
        print(f"   Error: {str(e)}")
        print("\n" + "="*60)
        print("  MongoDB is NOT running or not installed")
        print("="*60)
        print("\nTo fix this:")
        print("   1. Install MongoDB: https://www.mongodb.com/try/download/community")
        print("   2. Start MongoDB service: net start MongoDB")
        print("   3. Run this test again\n")
        print("See INSTALL_MONGODB.md for detailed instructions\n")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())

