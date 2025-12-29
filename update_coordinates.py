"""
Script to update venues, tournaments, shops, jobs, and academies with lat/lng coordinates
"""
import asyncio
from sqlalchemy import select, update
from app.core.database import AsyncSessionLocal
from app.models.models import Venue, Tournament, Shop, Job, Dictionary

# Approximate coordinates for major Gujarat cities
CITY_COORDINATES = {
    "Ahmedabad": {"lat": 23.0225, "lng": 72.5714},
    "Surat": {"lat": 21.1702, "lng": 72.8311},
    "Vadodara": {"lat": 22.3072, "lng": 73.1812},
    "Rajkot": {"lat": 22.3039, "lng": 70.8022},
    "Gandhinagar": {"lat": 23.2156, "lng": 72.6369},
    "Bhavnagar": {"lat": 21.7645, "lng": 72.1519},
    "Jamnagar": {"lat": 22.4707, "lng": 70.0577},
    "Junagadh": {"lat": 21.5222, "lng": 70.4579},
    "Anand": {"lat": 22.5645, "lng": 72.9289},
    "Mehsana": {"lat": 23.5880, "lng": 72.3693}
}

def add_random_offset(base_lat, base_lng, offset_km=5):
    """Add random offset to coordinates to spread locations within a city"""
    import random
    # 1 degree ≈ 111 km
    offset_deg = offset_km / 111
    lat_offset = random.uniform(-offset_deg, offset_deg)
    lng_offset = random.uniform(-offset_deg, offset_deg)
    return base_lat + lat_offset, base_lng + lng_offset

async def update_venues():
    """Update venues with coordinates"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Venue))
        venues = result.scalars().all()
        
        updated = 0
        for venue in venues:
            if venue.city in CITY_COORDINATES and not venue.latitude:
                base = CITY_COORDINATES[venue.city]
                venue.latitude, venue.longitude = add_random_offset(base["lat"], base["lng"], 10)
                updated += 1
        
        await session.commit()
        print(f"[OK] Updated {updated} venues with coordinates")

async def update_tournaments():
    """Update tournaments with coordinates"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Tournament))
        tournaments = result.scalars().all()
        
        updated = 0
        for tournament in tournaments:
            if tournament.city in CITY_COORDINATES and not tournament.latitude:
                base = CITY_COORDINATES[tournament.city]
                tournament.latitude, tournament.longitude = add_random_offset(base["lat"], base["lng"], 8)
                updated += 1
        
        await session.commit()
        print(f"[OK] Updated {updated} tournaments with coordinates")

async def update_shops():
    """Update shops with coordinates"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Shop))
        shops = result.scalars().all()
        
        updated = 0
        for shop in shops:
            if shop.city in CITY_COORDINATES and not shop.latitude:
                base = CITY_COORDINATES[shop.city]
                shop.latitude, shop.longitude = add_random_offset(base["lat"], base["lng"], 6)
                updated += 1
        
        await session.commit()
        print(f"[OK] Updated {updated} shops with coordinates")

async def update_jobs():
    """Update jobs with coordinates"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Job))
        jobs = result.scalars().all()
        
        updated = 0
        for job in jobs:
            if job.city in CITY_COORDINATES and not job.latitude:
                base = CITY_COORDINATES[job.city]
                job.latitude, job.longitude = add_random_offset(base["lat"], base["lng"], 7)
                updated += 1
        
        await session.commit()
        print(f"[OK] Updated {updated} jobs with coordinates")

async def update_academies():
    """Update academies with coordinates"""
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Dictionary).where(Dictionary.category == "Academy")
        )
        academies = result.scalars().all()
        
        updated = 0
        for academy in academies:
            if academy.city in CITY_COORDINATES and not academy.latitude:
                base = CITY_COORDINATES[academy.city]
                academy.latitude, academy.longitude = add_random_offset(base["lat"], base["lng"], 5)
                updated += 1
        
        await session.commit()
        print(f"[OK] Updated {updated} academies with coordinates")

async def main():
    print("Updating coordinates for all locations...")
    print("=" * 50)
    
    await update_venues()
    await update_tournaments()
    await update_shops()
    await update_jobs()
    await update_academies()
    
    print("=" * 50)
    print("All coordinates updated successfully!")

if __name__ == "__main__":
    asyncio.run(main())

