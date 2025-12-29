import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.models import User, Job, Shop, Dictionary, Tournament, Venue

async def check_all_tables():
    async with AsyncSessionLocal() as db:
        print("\n" + "="*70)
        print("DATABASE STATUS CHECK - SPORTS DIARY")
        print("="*70)
        
        # Users
        result = await db.execute(select(User))
        users = result.scalars().all()
        print(f"\nUSERS: {len(users)} total")
        for i, user in enumerate(users[:3], 1):
            print(f"   {i}. {user.name} ({user.phone}) - {user.city or 'No city'}")
        if len(users) > 3:
            print(f"   ... and {len(users) - 3} more")
        
        # Jobs
        result = await db.execute(select(Job))
        jobs = result.scalars().all()
        print(f"\nJOBS: {len(jobs)} total")
        for i, job in enumerate(jobs[:3], 1):
            print(f"   {i}. {job.title} ({job.job_type}) - {job.city}")
        if len(jobs) > 3:
            print(f"   ... and {len(jobs) - 3} more")
        
        # Venues
        result = await db.execute(select(Venue))
        venues = result.scalars().all()
        print(f"\nVENUES: {len(venues)} total")
        for i, venue in enumerate(venues[:3], 1):
            print(f"   {i}. {venue.name} - {venue.city}")
        if len(venues) > 3:
            print(f"   ... and {len(venues) - 3} more")
        
        # Tournaments
        result = await db.execute(select(Tournament))
        tournaments = result.scalars().all()
        print(f"\nTOURNAMENTS: {len(tournaments)} total")
        for i, tournament in enumerate(tournaments[:3], 1):
            print(f"   {i}. {tournament.name} ({tournament.sport_type}) - {tournament.city}")
        if len(tournaments) > 3:
            print(f"   ... and {len(tournaments) - 3} more")
        
        # Shops
        result = await db.execute(select(Shop))
        shops = result.scalars().all()
        print(f"\nSHOPS: {len(shops)} total")
        for i, shop in enumerate(shops[:3], 1):
            print(f"   {i}. {shop.name} ({shop.shop_type}) - {shop.city}")
        if len(shops) > 3:
            print(f"   ... and {len(shops) - 3} more")
        
        # Dictionary/Academy
        result = await db.execute(select(Dictionary))
        academies = result.scalars().all()
        print(f"\nACADEMIES: {len(academies)} total")
        for i, academy in enumerate(academies[:3], 1):
            print(f"   {i}. {academy.term} ({academy.sport})")
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
        
        print(f"\nDatabase location: backend/player_app.db")
        print("="*70 + "\n")

if __name__ == "__main__":
    asyncio.run(check_all_tables())

