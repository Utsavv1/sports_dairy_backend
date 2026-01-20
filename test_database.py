import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def check_database():
    """Check all data in MongoDB database"""
    try:
        # Get MongoDB connection string
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "sports_diary")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        
        print("\n" + "="*50)
        print("DATABASE CONTENT CHECK")
        print("="*50 + "\n")
        
        # Count venues
        venue_count = await db.venues.count_documents({})
        print(f"[OK] Venues: {venue_count}")
        
        # Count tournaments
        tournament_count = await db.tournaments.count_documents({})
        print(f"[OK] Tournaments: {tournament_count}")
        
        # Count shops
        shop_count = await db.shops.count_documents({})
        print(f"[OK] Shops: {shop_count}")
        
        # Count academies (dictionary)
        academy_count = await db.dictionary.count_documents({})
        print(f"[OK] Academies: {academy_count}")
        
        # Count jobs
        job_count = await db.jobs.count_documents({})
        print(f"[OK] Jobs: {job_count}")
        
        print("\n" + "-"*50)
        total = venue_count + tournament_count + shop_count + academy_count + job_count
        print(f"TOTAL RECORDS: {total}")
        print("-"*50 + "\n")
        
        # Show some sample data
        print("SAMPLE VENUES:")
        venues = await db.venues.find().limit(3).to_list(length=3)
        for v in venues:
            print(f"  - {v.get('name', 'N/A')} ({v.get('city', 'N/A')})")
        
        print("\nSAMPLE TOURNAMENTS:")
        tournaments = await db.tournaments.find().limit(3).to_list(length=3)
        for t in tournaments:
            print(f"  - {t.get('name', 'N/A')} ({t.get('city', 'N/A')})")
        
        print("\nSAMPLE SHOPS:")
        shops = await db.shops.find().limit(3).to_list(length=3)
        for s in shops:
            print(f"  - {s.get('name', 'N/A')} ({s.get('city', 'N/A')})")
        
        print("\n" + "="*50 + "\n")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_database())
