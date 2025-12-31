import asyncio
from sqlalchemy import select, func, delete
from app.core.database import AsyncSessionLocal
from app.models.models import Venue, Tournament, Shop, Dictionary, Job

async def cleanup_duplicates():
    """Remove duplicate entries from database"""
    async with AsyncSessionLocal() as db:
        print("\n" + "="*50)
        print("CLEANING UP DUPLICATE DATA")
        print("="*50 + "\n")
        
        # Check current counts
        print("BEFORE CLEANUP:")
        result = await db.execute(select(func.count()).select_from(Venue))
        venue_count = result.scalar()
        print(f"  Venues: {venue_count}")
        
        result = await db.execute(select(func.count()).select_from(Tournament))
        tournament_count = result.scalar()
        print(f"  Tournaments: {tournament_count}")
        
        result = await db.execute(select(func.count()).select_from(Shop))
        shop_count = result.scalar()
        print(f"  Shops: {shop_count}")
        
        result = await db.execute(select(func.count()).select_from(Dictionary))
        academy_count = result.scalar()
        print(f"  Academies: {academy_count}")
        
        result = await db.execute(select(func.count()).select_from(Job))
        job_count = result.scalar()
        print(f"  Jobs: {job_count}")
        
        print("\n" + "-"*50)
        print("REMOVING DUPLICATES...")
        print("-"*50 + "\n")
        
        # Get all venues and keep only first occurrence of each name
        result = await db.execute(select(Venue))
        all_venues = result.scalars().all()
        
        seen_names = {}
        duplicates_to_delete = []
        
        for venue in all_venues:
            if venue.name in seen_names:
                # This is a duplicate, mark for deletion
                duplicates_to_delete.append(venue.id)
                print(f"  [DUPLICATE] {venue.name} (ID: {venue.id})")
            else:
                # First occurrence, keep it
                seen_names[venue.name] = venue.id
                print(f"  [KEEP] {venue.name} (ID: {venue.id})")
        
        # Delete duplicates
        if duplicates_to_delete:
            print(f"\nDeleting {len(duplicates_to_delete)} duplicate venues...")
            await db.execute(
                delete(Venue).where(Venue.id.in_(duplicates_to_delete))
            )
            await db.commit()
            print("[OK] Duplicates removed!")
        else:
            print("\n[OK] No duplicates found!")
        
        # Check final counts
        print("\n" + "-"*50)
        print("AFTER CLEANUP:")
        print("-"*50 + "\n")
        
        result = await db.execute(select(func.count()).select_from(Venue))
        venue_count_after = result.scalar()
        print(f"  Venues: {venue_count_after}")
        
        result = await db.execute(select(func.count()).select_from(Tournament))
        tournament_count_after = result.scalar()
        print(f"  Tournaments: {tournament_count_after}")
        
        result = await db.execute(select(func.count()).select_from(Shop))
        shop_count_after = result.scalar()
        print(f"  Shops: {shop_count_after}")
        
        result = await db.execute(select(func.count()).select_from(Dictionary))
        academy_count_after = result.scalar()
        print(f"  Academies: {academy_count_after}")
        
        result = await db.execute(select(func.count()).select_from(Job))
        job_count_after = result.scalar()
        print(f"  Jobs: {job_count_after}")
        
        total = venue_count_after + tournament_count_after + shop_count_after + academy_count_after + job_count_after
        
        print("\n" + "-"*50)
        print(f"TOTAL RECORDS: {total}")
        print("-"*50 + "\n")
        
        print("="*50)
        print("CLEANUP COMPLETE!")
        print("="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(cleanup_duplicates())

