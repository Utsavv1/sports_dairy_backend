import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def check_all_tables():
    """Check all collections in MongoDB database"""
    try:
        # Get MongoDB connection string
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "sports_diary")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        
        print("\n" + "="*70)
        print("DATABASE STATUS CHECK - SPORTS DIARY")
        print("="*70)
        
        # Users
        users = await db.users.find().to_list(length=None)
        print(f"\nUSERS: {len(users)} total")
        for i, user in enumerate(users[:3], 1):
            name = user.get('name', 'N/A')
            phone = user.get('phone', 'N/A')
            city = user.get('city', 'No city')
            print(f"   {i}. {name} ({phone}) - {city}")
        if len(users) > 3:
            print(f"   ... and {len(users) - 3} more")
        
        # Jobs
        jobs = await db.jobs.find().to_list(length=None)
        print(f"\nJOBS: {len(jobs)} total")
        for i, job in enumerate(jobs[:3], 1):
            title = job.get('title', 'N/A')
            job_type = job.get('job_type', 'N/A')
            city = job.get('city', 'N/A')
            print(f"   {i}. {title} ({job_type}) - {city}")
        if len(jobs) > 3:
            print(f"   ... and {len(jobs) - 3} more")
        
        # Venues
        venues = await db.venues.find().to_list(length=None)
        print(f"\nVENUES: {len(venues)} total")
        for i, venue in enumerate(venues[:3], 1):
            name = venue.get('name', 'N/A')
            city = venue.get('city', 'N/A')
            print(f"   {i}. {name} - {city}")
        if len(venues) > 3:
            print(f"   ... and {len(venues) - 3} more")
        
        # Tournaments
        tournaments = await db.tournaments.find().to_list(length=None)
        print(f"\nTOURNAMENTS: {len(tournaments)} total")
        for i, tournament in enumerate(tournaments[:3], 1):
            name = tournament.get('name', 'N/A')
            sport_type = tournament.get('sport_type', 'N/A')
            city = tournament.get('city', 'N/A')
            print(f"   {i}. {name} ({sport_type}) - {city}")
        if len(tournaments) > 3:
            print(f"   ... and {len(tournaments) - 3} more")
        
        # Shops
        shops = await db.shops.find().to_list(length=None)
        print(f"\nSHOPS: {len(shops)} total")
        for i, shop in enumerate(shops[:3], 1):
            name = shop.get('name', 'N/A')
            shop_type = shop.get('shop_type', shop.get('category', 'N/A'))
            city = shop.get('city', 'N/A')
            print(f"   {i}. {name} ({shop_type}) - {city}")
        if len(shops) > 3:
            print(f"   ... and {len(shops) - 3} more")
        
        # Dictionary/Academy
        academies = await db.dictionary.find().to_list(length=None)
        print(f"\nACADEMIES: {len(academies)} total")
        for i, academy in enumerate(academies[:3], 1):
            term = academy.get('term', 'N/A')
            sport = academy.get('sport', 'N/A')
            print(f"   {i}. {term} ({sport})")
        if len(academies) > 3:
            print(f"   ... and {len(academies) - 3} more")
        
        # Summary
        total = len(users) + len(jobs) + len(venues) + len(tournaments) + len(shops) + len(academies)
        print("\n" + "="*70)
        print(f"SUMMARY:")
        print(f"  Total Users:       {len(users)}")
        print(f"  Total Jobs:        {len(jobs)}")
        print(f"  Total Venues:      {len(venues)}")
        print(f"  Total Tournaments: {len(tournaments)}")
        print(f"  Total Shops:       {len(shops)}")
        print(f"  Total Academies:   {len(academies)}")
        print(f"  ---")
        print(f"  GRAND TOTAL:       {total} records")
        print("="*70)
        
        # Status
        if total > 0:
            print(f"\nSTATUS: Database is populated and working!")
        else:
            print(f"\nSTATUS: Database is empty - run seed scripts!")
        
        print(f"\nDatabase: MongoDB ({database_name})")
        print("="*70 + "\n")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_all_tables())
