import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from app.core.database import AsyncSessionLocal, init_db
from app.models.models import Shop, Dictionary, Tournament

async def clear_and_seed():
    """Clear existing marketplace data and seed fresh data"""
    await init_db()
    
    async with AsyncSessionLocal() as db:
        try:
            # Clear existing data
            print("Clearing existing marketplace data...")
            result = await db.execute(select(Shop))
            for shop in result.scalars().all():
                await db.delete(shop)
            
            result = await db.execute(select(Dictionary))
            for dict_entry in result.scalars().all():
                await db.delete(dict_entry)
                
            result = await db.execute(select(Tournament))
            for tournament in result.scalars().all():
                await db.delete(tournament)
            
            await db.commit()
            print("[OK] Cleared existing data")
            
            # ==================== SPORTS SHOPS ====================
            shops_data = [
                {
                    "name": "Decathlon Ahmedabad",
                    "description": "India's largest sports retailer offering equipment for 80+ sports",
                    "shop_type": "Retail",
                    "category": "Equipment",
                    "specialization": ["Cricket", "Football", "Badminton", "Tennis"],
                    "brands_available": ["Kipsta", "Perfly", "Artengo", "Domyos"],
                    "city": "Ahmedabad",
                    "address": "Iscon Mall, Satellite Road",
                    "landmark": "Near ISCON Temple",
                    "contact_number": "+917947012345",
                    "email": "ahmedabad@decathlon.in",
                    "website": "https://www.decathlon.in",
                    "opening_time": "10:00",
                    "closing_time": "22:00",
                    "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "home_delivery": True,
                    "online_payment": True,
                    "bulk_orders": True,
                    "rating": 4.5,
                    "total_reviews": 234,
                    "is_verified": True
                },
                {
                    "name": "SG Cricket Store",
                    "description": "Premium cricket equipment manufacturer and retailer",
                    "shop_type": "Retail",
                    "category": "Equipment",
                    "specialization": ["Cricket Equipment"],
                    "brands_available": ["SG", "MRF", "SS", "GM"],
                    "city": "Surat",
                    "address": "Ring Road, Athwa",
                    "contact_number": "+919825012345",
                    "opening_time": "09:00",
                    "closing_time": "21:00",
                    "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    "home_delivery": True,
                    "online_payment": True,
                    "bulk_orders": True,
                    "rating": 4.7,
                    "total_reviews": 187,
                    "is_verified": True
                },
                {
                    "name": "Sports Junction Vadodara",
                    "description": "Your one-stop shop for all sports equipment and accessories",
                    "shop_type": "Retail",
                    "category": "Equipment",
                    "specialization": ["Cricket", "Football", "Badminton", "Tennis", "Table Tennis"],
                    "brands_available": ["Nike", "Adidas", "Puma", "Yonex", "Cosco"],
                    "city": "Vadodara",
                    "address": "Alkapuri Main Road",
                    "contact_number": "+919879012345",
                    "home_delivery": True,
                    "online_payment": True,
                    "rating": 4.3,
                    "total_reviews": 98,
                    "is_verified": True
                },
                {
                    "name": "Jersey Master Ahmedabad",
                    "description": "Custom jersey manufacturing for teams and academies",
                    "shop_type": "Manufacturer",
                    "category": "Jerseys",
                    "specialization": ["Custom Jerseys", "Team Uniforms"],
                    "city": "Ahmedabad",
                    "address": "Maninagar Industrial Area",
                    "contact_number": "+919825678901",
                    "opening_time": "10:00",
                    "closing_time": "19:00",
                    "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    "bulk_orders": True,
                    "custom_manufacturing": True,
                    "rating": 4.6,
                    "total_reviews": 145,
                    "is_verified": True
                },
                {
                    "name": "Fitness Nutrition Store",
                    "description": "Sports nutrition, supplements and wellness products",
                    "shop_type": "Retail",
                    "category": "Nutrition",
                    "specialization": ["Protein Supplements", "Energy Drinks", "Vitamins"],
                    "brands_available": ["MuscleBlaze", "Optimum Nutrition", "MyProtein"],
                    "city": "Rajkot",
                    "address": "Kalawad Road",
                    "contact_number": "+919825111222",
                    "online_payment": True,
                    "home_delivery": True,
                    "rating": 4.4,
                    "total_reviews": 76,
                    "is_verified": True
                }
            ]

            for shop_data in shops_data:
                shop = Shop(**shop_data)
                db.add(shop)
            
            await db.commit()
            print(f"[OK] Added {len(shops_data)} shops")

            # ==================== ACADEMIES ====================
            academies_data = [
                {
                    "term": "Champions Cricket Academy",
                    "sport": "Cricket",
                    "category": "Coaching",
                    "definition": "Professional cricket coaching academy with certified coaches and modern facilities",
                    "explanation": "Monthly Fee: Rs 3,500 | Location: Ahmedabad | Timings: 6 AM - 8 PM | Features: Indoor nets, bowling machines, video analysis",
                    "slug": "champions-cricket-academy-ahd",
                    "difficulty_level": "All Levels",
                    "is_featured": True
                },
                {
                    "term": "Elite Football Training Center",
                    "sport": "Football",
                    "category": "Training",
                    "definition": "Premier football academy with UEFA certified coaches",
                    "explanation": "Monthly Fee: Rs 4,000 | Location: Surat | Age Groups: U-10 to U-19 | Professional turf available",
                    "slug": "elite-football-surat",
                    "difficulty_level": "All Levels"
                },
                {
                    "term": "Smash Badminton Academy",
                    "sport": "Badminton",
                    "category": "Coaching",
                    "definition": "State-of-the-art badminton academy with international standard courts",
                    "explanation": "Monthly Fee: Rs 3,000 | Location: Vadodara | Facilities: 6 wooden courts, AC hall",
                    "slug": "smash-badminton-vad",
                    "difficulty_level": "Intermediate"
                },
                {
                    "term": "Ace Tennis Academy",
                    "sport": "Tennis",
                    "category": "Coaching",
                    "definition": "Professional tennis coaching academy with hard courts",
                    "explanation": "Monthly Fee: Rs 5,000 | Location: Rajkot | Features: 4 courts, ball machines, video analysis",
                    "slug": "ace-tennis-rajkot",
                    "difficulty_level": "Advanced",
                    "is_featured": True
                },
                {
                    "term": "Pro Basketball Academy",
                    "sport": "Basketball",
                    "category": "Training",
                    "definition": "Complete basketball development program with NBA-style training",
                    "explanation": "Monthly Fee: Rs 4,500 | Location: Gandhinagar | Age: 8+ years | Indoor court",
                    "slug": "pro-basketball-gandhinagar",
                    "difficulty_level": "All Levels"
                }
            ]

            for academy_data in academies_data:
                academy = Dictionary(**academy_data)
                db.add(academy)
            
            await db.commit()
            print(f"[OK] Added {len(academies_data)} academies")

            # ==================== TOURNAMENTS ====================
            tournaments_data = [
                {
                    "name": "Ahmedabad Premier League 2025",
                    "description": "Annual T20 cricket tournament featuring teams from across Ahmedabad. Prize pool of Rs. 2 lakhs!",
                    "sport_type": "Cricket",
                    "tournament_type": "League",
                    "format": "T20",
                    "team_size": 15,
                    "max_teams": 16,
                    "age_category": "Open",
                    "gender_category": "Men",
                    "skill_level": "Intermediate",
                    "city": "Ahmedabad",
                    "venue_name": "Sardar Patel Stadium Grounds",
                    "start_date": datetime.utcnow() + timedelta(days=30),
                    "end_date": datetime.utcnow() + timedelta(days=45),
                    "registration_start": datetime.utcnow(),
                    "registration_deadline": datetime.utcnow() + timedelta(days=20),
                    "entry_fee": 5000,
                    "prize_pool": 200000,
                    "contact_person": "Rajesh Patel",
                    "contact_number": "+919825000111",
                    "contact_email": "apl2025@gmail.com",
                    "organizer_id": 1,
                    "status": "upcoming",
                    "is_verified": True,
                    "is_featured": True
                },
                {
                    "name": "Surat Football Championship U-19",
                    "description": "Under-19 football championship with knockout format",
                    "sport_type": "Football",
                    "tournament_type": "Knockout",
                    "format": "11-a-side",
                    "team_size": 16,
                    "max_teams": 32,
                    "age_category": "U-19",
                    "gender_category": "Men",
                    "city": "Surat",
                    "venue_name": "Surat Sports Complex",
                    "start_date": datetime.utcnow() + timedelta(days=45),
                    "end_date": datetime.utcnow() + timedelta(days=60),
                    "registration_deadline": datetime.utcnow() + timedelta(days=25),
                    "entry_fee": 3000,
                    "prize_pool": 150000,
                    "contact_person": "Amit Shah",
                    "contact_number": "+919879000222",
                    "organizer_id": 1,
                    "status": "upcoming",
                    "is_verified": True
                },
                {
                    "name": "Gujarat Open Badminton Tournament",
                    "description": "State-level badminton tournament with singles and doubles categories",
                    "sport_type": "Badminton",
                    "tournament_type": "Mixed",
                    "age_category": "Open",
                    "gender_category": "Mixed",
                    "max_teams": 64,
                    "city": "Vadodara",
                    "venue_name": "Vadodara Indoor Stadium",
                    "start_date": datetime.utcnow() + timedelta(days=40),
                    "registration_deadline": datetime.utcnow() + timedelta(days=22),
                    "entry_fee": 500,
                    "prize_pool": 50000,
                    "contact_number": "+919879111333",
                    "organizer_id": 1,
                    "status": "upcoming"
                },
                {
                    "name": "Rajkot Tennis Championship",
                    "description": "Open tennis championship with men's and women's singles",
                    "sport_type": "Tennis",
                    "tournament_type": "Knockout",
                    "age_category": "Open",
                    "gender_category": "Mixed",
                    "max_teams": 32,
                    "city": "Rajkot",
                    "start_date": datetime.utcnow() + timedelta(days=35),
                    "registration_deadline": datetime.utcnow() + timedelta(days=18),
                    "entry_fee": 1000,
                    "prize_pool": 80000,
                    "organizer_id": 1,
                    "status": "upcoming"
                },
                {
                    "name": "Gandhinagar Basketball League 2025",
                    "description": "Premier basketball league featuring top teams from across Gujarat",
                    "sport_type": "Basketball",
                    "tournament_type": "League",
                    "format": "5-on-5",
                    "team_size": 12,
                    "max_teams": 10,
                    "age_category": "Open",
                    "gender_category": "Men",
                    "skill_level": "Professional",
                    "city": "Gandhinagar",
                    "venue_name": "Capital Complex Sports Arena",
                    "start_date": datetime.utcnow() + timedelta(days=50),
                    "end_date": datetime.utcnow() + timedelta(days=80),
                    "registration_start": datetime.utcnow(),
                    "registration_deadline": datetime.utcnow() + timedelta(days=28),
                    "entry_fee": 8000,
                    "prize_pool": 300000,
                    "contact_person": "Kiran Desai",
                    "contact_number": "+919825444555",
                    "organizer_id": 1,
                    "status": "upcoming",
                    "is_verified": True,
                    "is_featured": True
                }
            ]

            for tournament_data in tournaments_data:
                tournament = Tournament(**tournament_data)
                db.add(tournament)
            
            await db.commit()
            print(f"[OK] Added {len(tournaments_data)} tournaments")
            
            print("\n[SUCCESS] All marketplace data seeded!")
            print(f"   - {len(shops_data)} Sports Shops")
            print(f"   - {len(academies_data)} Academies")
            print(f"   - {len(tournaments_data)} Tournaments")

        except Exception as e:
            await db.rollback()
            print(f"[ERROR] {str(e)}")

if __name__ == "__main__":
    asyncio.run(clear_and_seed())

