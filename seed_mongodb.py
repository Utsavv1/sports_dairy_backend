import asyncio
import sys
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
MONGODB_URL = "mongodb://localhost:27017"
DATABASE_NAME = "sports_diary"

async def clear_database(db):
    """Clear all collections"""
    print("\n🗑️  Clearing existing data...")
    
    collections = ["venues", "tournaments", "shops", "jobs", "dictionary"]
    for collection_name in collections:
        result = await db[collection_name].delete_many({})
        print(f"   Deleted {result.deleted_count} documents from {collection_name}")

async def seed_venues(db):
    """Seed venues data"""
    print("\n🏟️  Seeding Venues...")
    
    venues = [
        {
            "name": "Ahmedabad Cricket Turf",
            "description": "Premium cricket turf with professional facilities",
            "venue_type": "Turf",
            "sports_available": ["Cricket"],
            "amenities": ["Parking", "Changing Room", "First Aid", "Cafeteria"],
            "city": "Ahmedabad",
            "state": "Gujarat",
            "address": "SG Highway, Ahmedabad",
            "latitude": 23.0225,
            "longitude": 72.5714,
            "price_per_hour": 1500.0,
            "opening_time": "06:00",
            "closing_time": "23:00",
            "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "capacity": 22,
            "surface_type": "Artificial Turf",
            "indoor_outdoor": "Outdoor",
            "contact_number": "+919876543210",
            "rating": 4.5,
            "total_reviews": 45,
            "total_bookings": 234,
            "is_verified": True,
            "is_featured": True,
            "is_active": True,
            "images": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "name": "Surat Football Arena",
            "description": "5-a-side and 7-a-side football ground",
            "venue_type": "Ground",
            "sports_available": ["Football"],
            "amenities": ["Parking", "Changing Room", "Lighting", "Seating"],
            "city": "Surat",
            "state": "Gujarat",
            "address": "Ring Road, Surat",
            "latitude": 21.1702,
            "longitude": 72.8311,
            "price_per_hour": 1200.0,
            "opening_time": "06:00",
            "closing_time": "22:00",
            "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "capacity": 14,
            "surface_type": "Artificial Grass",
            "indoor_outdoor": "Outdoor",
            "contact_number": "+919876543211",
            "rating": 4.2,
            "total_reviews": 32,
            "total_bookings": 156,
            "is_verified": True,
            "is_featured": False,
            "is_active": True,
            "images": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    # Add more sample venues for other cities
    cities = ["Vadodara", "Rajkot", "Bhavnagar", "Jamnagar", "Gandhinagar"]
    sports = ["Badminton", "Tennis", "Basketball", "Volleyball"]
    
    for city in cities:
        for i, sport in enumerate(sports):
            venue = {
                "name": f"{city} {sport} Center",
                "description": f"Modern {sport} facilities in {city}",
                "venue_type": "Court" if sport in ["Badminton", "Tennis", "Basketball"] else "Ground",
                "sports_available": [sport],
                "amenities": ["Parking", "Changing Room", "Water"],
                "city": city,
                "state": "Gujarat",
                "address": f"Main Road, {city}",
                "latitude": 23.0 + (i * 0.1),
                "longitude": 72.5 + (i * 0.1),
                "price_per_hour": 800.0 + (i * 100),
                "opening_time": "06:00",
                "closing_time": "22:00",
                "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                "capacity": 10 + (i * 2),
                "surface_type": "Concrete" if sport == "Basketball" else "Wooden",
                "indoor_outdoor": "Indoor",
                "contact_number": f"+9198765432{i}{i}",
                "rating": 4.0 + (i * 0.1),
                "total_reviews": 20 + (i * 5),
                "total_bookings": 100 + (i * 20),
                "is_verified": True,
                "is_featured": False,
                "is_active": True,
                "images": [],
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            }
            venues.append(venue)
    
    result = await db.venues.insert_many(venues)
    print(f"   ✅ Inserted {len(result.inserted_ids)} venues")

async def seed_tournaments(db):
    """Seed tournaments data"""
    print("\n🏆  Seeding Tournaments...")
    
    tournaments = [
        {
            "organizer_id": "000000000000000000000001",  # Placeholder
            "name": "Ahmedabad Premier Cricket League",
            "description": "Annual cricket tournament for amateur teams",
            "sport_type": "Cricket",
            "tournament_type": "League",
            "format": "T20",
            "team_size": 11,
            "max_teams": 16,
            "min_teams": 8,
            "current_teams": 12,
            "age_category": "Open",
            "gender_category": "Men",
            "skill_level": "Intermediate",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "venue_name": "Ahmedabad Cricket Turf",
            "latitude": 23.0225,
            "longitude": 72.5714,
            "start_date": datetime.utcnow() + timedelta(days=30),
            "end_date": datetime.utcnow() + timedelta(days=60),
            "registration_deadline": datetime.utcnow() + timedelta(days=15),
            "entry_fee": 5000.0,
            "currency": "INR",
            "prize_pool": 100000.0,
            "status": "upcoming",
            "is_featured": True,
            "is_verified": True,
            "is_active": True,
            "views_count": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "organizer_id": "000000000000000000000001",
            "name": "Surat Football Championship",
            "description": "Inter-city football tournament",
            "sport_type": "Football",
            "tournament_type": "Knockout",
            "format": "11-a-side",
            "team_size": 11,
            "max_teams": 8,
            "min_teams": 4,
            "current_teams": 6,
            "age_category": "U-19",
            "gender_category": "Mixed",
            "skill_level": "Beginner",
            "city": "Surat",
            "state": "Gujarat",
            "venue_name": "Surat Football Arena",
            "latitude": 21.1702,
            "longitude": 72.8311,
            "start_date": datetime.utcnow() + timedelta(days=45),
            "end_date": datetime.utcnow() + timedelta(days=47),
            "registration_deadline": datetime.utcnow() + timedelta(days=20),
            "entry_fee": 3000.0,
            "currency": "INR",
            "prize_pool": 50000.0,
            "status": "upcoming",
            "is_featured": True,
            "is_verified": True,
            "is_active": True,
            "views_count": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.tournaments.insert_many(tournaments)
    print(f"   ✅ Inserted {len(result.inserted_ids)} tournaments")

async def seed_shops(db):
    """Seed shops data"""
    print("\n🏪  Seeding Shops...")
    
    shops = [
        {
            "name": "Sports World Ahmedabad",
            "description": "Complete sports equipment and apparel store",
            "shop_type": "Retail",
            "category": "Equipment",
            "specialization": ["Cricket Equipment", "Football Gear", "Jerseys"],
            "brands_available": ["Nike", "Adidas", "MRF", "SG"],
            "city": "Ahmedabad",
            "state": "Gujarat",
            "address": "CG Road, Ahmedabad",
            "latitude": 23.0225,
            "longitude": 72.5714,
            "contact_number": "+919876543210",
            "opening_time": "10:00",
            "closing_time": "21:00",
            "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "rating": 4.5,
            "total_reviews": 67,
            "total_enquiries": 234,
            "home_delivery": True,
            "online_payment": True,
            "bulk_orders": True,
            "is_featured": True,
            "is_verified": True,
            "is_active": True,
            "images": [],
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.shops.insert_many(shops)
    print(f"   ✅ Inserted {len(result.inserted_ids)} shops")

async def seed_jobs(db):
    """Seed jobs data"""
    print("\n💼  Seeding Jobs...")
    
    jobs = [
        {
            "posted_by": "000000000000000000000001",  # Placeholder
            "title": "Cricket Umpire Needed",
            "job_type": "Umpire",
            "description": "Experienced cricket umpire for local tournaments",
            "sport_type": "Cricket",
            "employment_type": "Per Match",
            "experience_required": "2-5 years",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "latitude": 23.0225,
            "longitude": 72.5714,
            "salary_min": 1000.0,
            "salary_max": 2000.0,
            "salary_type": "Per Match",
            "currency": "INR",
            "application_deadline": datetime.utcnow() + timedelta(days=30),
            "status": "active",
            "is_featured": False,
            "is_verified": True,
            "views_count": 0,
            "applications_count": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.jobs.insert_many(jobs)
    print(f"   ✅ Inserted {len(result.inserted_ids)} jobs")

async def seed_dictionary(db):
    """Seed dictionary/academies data"""
    print("\n📚  Seeding Dictionary/Academies...")
    
    entries = [
        {
            "term": "Ahmedabad Sports Academy",
            "sport": "Cricket",
            "category": "Academy",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "address": "Satellite Road, Ahmedabad, Gujarat 380015",
            "latitude": 23.0225,
            "longitude": 72.5714,
            "contact_number": "+919876543210",
            "email": "info@ahmedabadsports.com",
            "timing": "Monday-Saturday: 6:00 AM - 9:00 PM | Sunday: 7:00 AM - 7:00 PM",
            "fees": "₹5,000 - ₹15,000 per month",
            "capacity": 50,
            "definition": "Premier cricket coaching academy in Ahmedabad",
            "explanation": "Offers professional cricket training for all age groups with expert coaches and world-class facilities",
            "programs": [
                "Junior Cricket Training (6-12 years)",
                "Advanced Cricket Coaching (13-18 years)",
                "Professional Level Training",
                "Weekend Batches",
                "Personal Coaching Sessions",
                "Match Preparation Programs"
            ],
            "amenities": [
                "Professional Cricket Pitch",
                "Indoor Nets Practice Area",
                "Video Analysis Room",
                "Fitness & Gym Facilities",
                "Changing Rooms & Lockers",
                "First Aid & Medical Support",
                "Parent Waiting Area",
                "Equipment Rental Available"
            ],
            "coaching_staff": [
                "Rajesh Kumar - Head Coach (15 years experience)",
                "Amit Patel - Batting Coach (Former Ranji Player)",
                "Priya Shah - Fitness Trainer (Certified)",
                "Kiran Desai - Junior Coach"
            ],
            "age_groups": [
                "6-10 years",
                "11-15 years",
                "16-18 years",
                "Adults (19+)"
            ],
            "examples": [
                "Daily practice sessions with professional coaches",
                "Weekly match simulations and practice games",
                "Monthly tournaments for skill assessment",
                "Specialized training for different playing positions"
            ],
            "is_featured": True,
            "is_active": True,
            "views_count": 0,
            "helpful_count": 0,
            "rating": 0.0,
            "total_reviews": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "term": "Elite Football Academy",
            "sport": "Football",
            "category": "Academy",
            "city": "Surat",
            "state": "Gujarat",
            "address": "Vesu Main Road, Surat, Gujarat 395007",
            "latitude": 21.1702,
            "longitude": 72.8311,
            "contact_number": "+919876543211",
            "email": "info@elitefootball.com",
            "timing": "Monday-Sunday: 5:30 AM - 8:30 PM",
            "fees": "₹4,000 - ₹12,000 per month",
            "capacity": 60,
            "definition": "Professional football training academy in Surat",
            "explanation": "Comprehensive football training program following international standards with UEFA certified coaches",
            "programs": [
                "Kids Football Academy (4-8 years)",
                "Junior Football Training (9-14 years)",
                "Advanced Football Program (15-19 years)",
                "Goalkeeper Specialist Training",
                "Weekend Football Clinics",
                "Summer Football Camps"
            ],
            "amenities": [
                "Full-Size Football Field (Natural Grass)",
                "Artificial Turf Practice Area",
                "Floodlights for Evening Training",
                "Professional Changing Rooms",
                "Cafeteria & Refreshments",
                "Sports Psychology Counseling",
                "Physical Therapy & Recovery Room",
                "Equipment Storage & Rental"
            ],
            "coaching_staff": [
                "Coach John D'Souza - Director (UEFA A License)",
                "Michael Fernandes - Senior Coach (20 years exp)",
                "Sara Williams - Fitness Coach",
                "Rahul Sharma - Goalkeeper Coach"
            ],
            "age_groups": [
                "4-8 years",
                "9-14 years",
                "15-19 years",
                "Adults (20+)"
            ],
            "examples": [
                "Professional training methodology used in European clubs",
                "Regular friendly matches with other academies",
                "Player development programs focused on individual skills",
                "Participation in state and national level tournaments"
            ],
            "is_featured": True,
            "is_active": True,
            "views_count": 0,
            "helpful_count": 0,
            "rating": 0.0,
            "total_reviews": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        },
        {
            "term": "Tennis Pro Academy",
            "sport": "Tennis",
            "category": "Academy",
            "city": "Vadodara",
            "state": "Gujarat",
            "address": "Alkapuri, Vadodara, Gujarat 390007",
            "latitude": 22.3072,
            "longitude": 73.1812,
            "contact_number": "+919876543212",
            "email": "contact@tennisproacademy.com",
            "timing": "Monday-Saturday: 6:00 AM - 10:00 PM | Sunday: 7:00 AM - 8:00 PM",
            "fees": "₹6,000 - ₹20,000 per month",
            "capacity": 40,
            "definition": "Professional tennis training academy in Vadodara",
            "explanation": "Premier tennis academy offering world-class coaching and facilities for all skill levels",
            "programs": [
                "Beginner Tennis Program (5-8 years)",
                "Junior Development Program (9-15 years)",
                "Advanced Competitive Training (16+ years)",
                "Professional Circuit Preparation",
                "Private One-on-One Coaching",
                "Group Training Sessions"
            ],
            "amenities": [
                "6 Professional Tennis Courts (Hard & Clay)",
                "Indoor Air-Conditioned Courts",
                "Ball Machine Practice Facility",
                "Video Analysis System",
                "Strength & Conditioning Gym",
                "Sports Medicine Clinic",
                "Pro Shop & Equipment Store",
                "Player Lounge & Viewing Area"
            ],
            "coaching_staff": [
                "Coach Vikram Mehta - Head Coach (Former National Player)",
                "Neha Kapoor - Junior Development Coach",
                "Dr. Sanjay Patel - Sports Physiotherapist",
                "Anita Reddy - Fitness Specialist"
            ],
            "age_groups": [
                "5-8 years",
                "9-15 years",
                "16-18 years",
                "Adults (19+)"
            ],
            "examples": [
                "Structured training following ITF guidelines",
                "Regular tournaments and ranking opportunities",
                "Mental conditioning and sports psychology sessions",
                "Nutritional guidance for young athletes"
            ],
            "is_featured": True,
            "is_active": True,
            "views_count": 0,
            "helpful_count": 0,
            "rating": 0.0,
            "total_reviews": 0,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
    ]
    
    result = await db.dictionary.insert_many(entries)
    print(f"   ✅ Inserted {len(result.inserted_ids)} dictionary entries")

async def main():
    """Main seeding function"""
    try:
        # Set UTF-8 encoding for console output
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass
    
    print("\n" + "="*60)
    print("  🌱 MongoDB Database Seeding")
    print("="*60)
    print(f"\n  Database: {DATABASE_NAME}")
    print(f"  MongoDB: {MONGODB_URL}")
    print("\n" + "="*60)
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        # Ping to verify connection
        await client.admin.command('ping')
        print("\n✅ Connected to MongoDB")
        
        # Clear existing data
        await clear_database(db)
        
        # Seed collections
        await seed_venues(db)
        await seed_tournaments(db)
        await seed_shops(db)
        await seed_jobs(db)
        await seed_dictionary(db)
        
        # Print summary
        print("\n" + "="*60)
        print("  ✅ SEEDING COMPLETED SUCCESSFULLY!")
        print("="*60)
        
        # Get counts
        venue_count = await db.venues.count_documents({})
        tournament_count = await db.tournaments.count_documents({})
        shop_count = await db.shops.count_documents({})
        job_count = await db.jobs.count_documents({})
        dictionary_count = await db.dictionary.count_documents({})
        total_count = venue_count + tournament_count + shop_count + job_count + dictionary_count
        
        print(f"\n  📊 Database Summary:")
        print(f"     • Venues: {venue_count}")
        print(f"     • Tournaments: {tournament_count}")
        print(f"     • Shops: {shop_count}")
        print(f"     • Jobs: {job_count}")
        print(f"     • Dictionary: {dictionary_count}")
        print(f"     • TOTAL: {total_count} documents")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(main())

