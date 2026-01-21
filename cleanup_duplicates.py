import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def cleanup_duplicates():
    """Remove duplicate entries from MongoDB database"""
    try:
        # Get MongoDB connection string
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "sports_diary")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB\n")
        
        print("\n" + "="*50)
        print("CLEANING UP DUPLICATE DATA")
        print("="*50 + "\n")
        
        # Check current counts
        print("BEFORE CLEANUP:")
        venue_count = await db.venues.count_documents({})
        print(f"  Venues: {venue_count}")
        
        tournament_count = await db.tournaments.count_documents({})
        print(f"  Tournaments: {tournament_count}")
        
        shop_count = await db.shops.count_documents({})
        print(f"  Shops: {shop_count}")
        
        academy_count = await db.dictionary.count_documents({})
        print(f"  Academies: {academy_count}")
        
        job_count = await db.jobs.count_documents({})
        print(f"  Jobs: {job_count}")
        
        print("\n" + "-"*50)
        print("REMOVING DUPLICATES...")
        print("-"*50 + "\n")
        
        # Get all venues and keep only first occurrence of each name
        all_venues = await db.venues.find().to_list(length=None)
        
        seen_names = {}
        duplicates_to_delete = []
        
        for venue in all_venues:
            venue_name = venue.get('name', '')
            venue_id = venue.get('_id')
            
            if venue_name in seen_names:
                # This is a duplicate, mark for deletion
                duplicates_to_delete.append(venue_id)
                print(f"  [DUPLICATE] {venue_name} (ID: {venue_id})")
            else:
                # First occurrence, keep it
                seen_names[venue_name] = venue_id
                print(f"  [KEEP] {venue_name} (ID: {venue_id})")
        
        # Delete duplicates
        if duplicates_to_delete:
            print(f"\nDeleting {len(duplicates_to_delete)} duplicate venues...")
            result = await db.venues.delete_many({"_id": {"$in": duplicates_to_delete}})
            print(f"[OK] {result.deleted_count} duplicates removed!")
        else:
            print("\n[OK] No duplicates found!")
        
        # Check final counts
        print("\n" + "-"*50)
        print("AFTER CLEANUP:")
        print("-"*50 + "\n")
        
        venue_count_after = await db.venues.count_documents({})
        print(f"  Venues: {venue_count_after}")
        
        tournament_count_after = await db.tournaments.count_documents({})
        print(f"  Tournaments: {tournament_count_after}")
        
        shop_count_after = await db.shops.count_documents({})
        print(f"  Shops: {shop_count_after}")
        
        academy_count_after = await db.dictionary.count_documents({})
        print(f"  Academies: {academy_count_after}")
        
        job_count_after = await db.jobs.count_documents({})
        print(f"  Jobs: {job_count_after}")
        
        total = venue_count_after + tournament_count_after + shop_count_after + academy_count_after + job_count_after
        
        print("\n" + "-"*50)
        print(f"TOTAL RECORDS: {total}")
        print("-"*50 + "\n")
        
        print("="*50)
        print("CLEANUP COMPLETE!")
        print("="*50 + "\n")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(cleanup_duplicates())
