import asyncio
from sqlalchemy import select, func
from app.core.database import AsyncSessionLocal
from app.models.models import Venue, Tournament, Shop, Dictionary, Job

async def check_database():
    """Check all data in database"""
    async with AsyncSessionLocal() as db:
        print("\n" + "="*50)
        print("DATABASE CONTENT CHECK")
        print("="*50 + "\n")
        
        # Count venues
        result = await db.execute(select(func.count()).select_from(Venue))
        venue_count = result.scalar()
        print(f"[OK] Venues: {venue_count}")
        
        # Count tournaments
        result = await db.execute(select(func.count()).select_from(Tournament))
        tournament_count = result.scalar()
        print(f"[OK] Tournaments: {tournament_count}")
        
        # Count shops
        result = await db.execute(select(func.count()).select_from(Shop))
        shop_count = result.scalar()
        print(f"[OK] Shops: {shop_count}")
        
        # Count academies (dictionary)
        result = await db.execute(select(func.count()).select_from(Dictionary))
        academy_count = result.scalar()
        print(f"[OK] Academies: {academy_count}")
        
        # Count jobs
        result = await db.execute(select(func.count()).select_from(Job))
        job_count = result.scalar()
        print(f"[OK] Jobs: {job_count}")
        
        print("\n" + "-"*50)
        print(f"TOTAL RECORDS: {venue_count + tournament_count + shop_count + academy_count + job_count}")
        print("-"*50 + "\n")
        
        # Show some sample data
        print("SAMPLE VENUES:")
        result = await db.execute(select(Venue).limit(3))
        venues = result.scalars().all()
        for v in venues:
            print(f"  - {v.name} ({v.city})")
        
        print("\nSAMPLE TOURNAMENTS:")
        result = await db.execute(select(Tournament).limit(3))
        tournaments = result.scalars().all()
        for t in tournaments:
            print(f"  - {t.name} ({t.city})")
        
        print("\nSAMPLE SHOPS:")
        result = await db.execute(select(Shop).limit(3))
        shops = result.scalars().all()
        for s in shops:
            print(f"  - {s.name} ({s.city})")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    asyncio.run(check_database())

