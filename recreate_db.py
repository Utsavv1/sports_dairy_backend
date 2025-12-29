"""
Recreate database with all tables
"""
import asyncio
import sys

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def main():
    print("Importing models...")
    # Import all models first so they're registered with Base.metadata
    from app.models.models import (
        User, Venue, VenueSlot, Booking, VenueReview,
        Tournament, Team, TournamentRegistration,
        Shop, Job, Dictionary
    )
    
    print(f"Found {len(User.metadata.tables)} tables to create")
    print(f"Tables: {list(User.metadata.tables.keys())}")
    
    print("\nCreating database tables...")
    from app.core.database import engine, Base
    
    async with engine.begin() as conn:
        # Drop all tables first
        print("Dropping existing tables...")
        await conn.run_sync(Base.metadata.drop_all)
        
        # Create all tables
        print("Creating new tables...")
        await conn.run_sync(Base.metadata.create_all)
    
    print("\n✓ Database created successfully!")
    
    # Verify
    print("\nVerifying tables...")
    import sqlite3
    conn = sqlite3.connect('sports_diary.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables in database: {[t[0] for t in tables]}")
    conn.close()

if __name__ == "__main__":
    asyncio.run(main())

