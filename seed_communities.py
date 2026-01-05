import asyncio
import sys
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient

# Set UTF-8 encoding for console output
sys.stdout.reconfigure(encoding='utf-8')

MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "sports_diary"

async def seed_communities():
    """Seed communities for different sports"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print("🌍 Seeding Communities...")
    
    # Clear existing communities
    await db.communities.delete_many({})
    await db.community_members.delete_many({})
    await db.community_posts.delete_many({})
    print("   Cleared existing data")
    
    communities = [
        {
            "name": "Cricket Community",
            "description": "Connect with cricket enthusiasts, share tips, organize matches, and discuss everything cricket!",
            "sport_type": "Cricket",
            "icon": "🏏",
            "cover_image": "https://images.unsplash.com/photo-1540747913346-19e32365cea3?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Football Community",
            "description": "Join football lovers, discuss tactics, share match highlights, and find local games!",
            "sport_type": "Football",
            "icon": "⚽",
            "cover_image": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Basketball Community",
            "description": "Connect with basketball players, share training tips, organize pickup games, and more!",
            "sport_type": "Basketball",
            "icon": "🏀",
            "cover_image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Badminton Community",
            "description": "Meet badminton players, discuss techniques, find partners, and join tournaments!",
            "sport_type": "Badminton",
            "icon": "🏸",
            "cover_image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Tennis Community",
            "description": "Join tennis enthusiasts, share practice routines, find courts, and compete!",
            "sport_type": "Tennis",
            "icon": "🎾",
            "cover_image": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Volleyball Community",
            "description": "Connect with volleyball players, organize beach games, and share training videos!",
            "sport_type": "Volleyball",
            "icon": "🏐",
            "cover_image": "https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Table Tennis Community",
            "description": "Meet table tennis players, share techniques, find clubs, and compete in tournaments!",
            "sport_type": "Table Tennis",
            "icon": "🏓",
            "cover_image": "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Hockey Community",
            "description": "Join hockey enthusiasts, discuss matches, share training tips, and find teams!",
            "sport_type": "Hockey",
            "icon": "🏑",
            "cover_image": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Kabaddi Community",
            "description": "Connect with kabaddi players, share strategies, organize matches, and celebrate the sport!",
            "sport_type": "Kabaddi",
            "icon": "🤼",
            "cover_image": "https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Running & Athletics",
            "description": "Join runners and athletes, share training plans, find running groups, and track progress!",
            "sport_type": "Athletics",
            "icon": "🏃",
            "cover_image": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800",
            "members_count": 0,
            "posts_count": 0,
            "is_active": True,
            "is_featured": False,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.communities.insert_many(communities)
    print(f"   ✅ Created {len(result.inserted_ids)} communities")
    
    print("\n✅ Community seeding completed!")
    print(f"   Total communities: {len(communities)}")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_communities())

