"""
Count academies in MongoDB database
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

async def count_academies():
    """Count and display all academies in database"""
    try:
        # Get MongoDB connection string
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "sports_diary")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        
        # Get all academies (dictionary entries)
        items = await db.dictionary.find().to_list(length=None)
        
        print(f'\nTotal academies in database: {len(items)}')
        print('='*60)
        
        if items:
            for item in items:
                term = item.get('term', 'N/A')
                city = item.get('city') or 'Not set'
                sport = item.get('sport', 'N/A')
                category = item.get('category') or 'Not set'
                
                print(f'  - {term}')
                print(f'    City: {city}')
                print(f'    Sport: {sport}')
                print(f'    Category: {category}')
                print()
        else:
            print('  No academies found!')
        
        print('='*60)
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(count_academies())
