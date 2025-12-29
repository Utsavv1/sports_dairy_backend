import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, init_db
from app.models.models import Shop, Job, Dictionary, Tournament, Team
from datetime import datetime, timedelta

async def seed_marketplace_data():
    """Seed comprehensive marketplace data"""
    async with AsyncSessionLocal() as db:
        try:
            # ==================== SPORTS SHOPS ====================
            shops_data = [
                {
                    "name": "Decathlon Ahmedabad",
                    "description": "India's largest sports retailer offering equipment for 80+ sports",
                    "shop_type": "Retail",
                    "category": "Equipment",
                    "products": [
                        {"name": "Cricket Bat", "price": 2500, "brand": "Kipsta"},
                        {"name": "Football", "price": 899, "brand": "Kipsta"},
                        {"name": "Badminton Racket", "price": 1499, "brand": "Perfly"}
                    ],
                    "specialization": ["Cricket", "Football", "Badminton", "Tennis"],
                    "brands_available": ["Kipsta", "Perfly", "Artengo", "Domyos"],
                    "city": "Ahmedabad",
                    "address": "Iscon Mall, Satellite Road",
                    "landmark": "Near ISCON Temple",
                    "contact_number": "+917947012345",
                    "whatsapp_number": "+917947012345",
                    "email": "ahmedabad@decathlon.in",
                    "website": "https://www.decathlon.in",
                    "opening_time": "10:00",
                    "closing_time": "22:00",
                    "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
                    "images": ["https://images.unsplash.com/photo-1556906781-9a412961c28c?w=800", "https://images.unsplash.com/photo-1587280501635-68a0e82cd5ff?w=800"],
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
                    "products": [
                        {"name": "SG English Willow Bat", "price": 8500, "brand": "SG"},
                        {"name": "SG Cricket Pads", "price": 3200, "brand": "SG"},
                        {"name": "SG Batting Gloves", "price": 1800, "brand": "SG"}
                    ],
                    "specialization": ["Cricket Equipment"],
                    "brands_available": ["SG", "MRF", "SS", "GM"],
                    "city": "Surat",
                    "address": "Ring Road, Athwa",
                    "contact_number": "+919825012345",
                    "whatsapp_number": "+919825012345",
                    "opening_time": "09:00",
                    "closing_time": "21:00",
                    "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    "images": ["https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=800", "https://images.unsplash.com/photo-1624526267942-ab0ff8a3e972?w=800"],
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
                    "images": ["https://images.unsplash.com/photo-1460353581641-37baddab0fa2?w=800"],
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
                    "whatsapp_number": "+919825678901",
                    "opening_time": "10:00",
                    "closing_time": "19:00",
                    "operating_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
                    "images": ["https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800"],
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
                    "images": ["https://images.unsplash.com/photo-1593095948071-474c5cc2989d?w=800"],
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

            # ==================== JOBS PORTAL ====================
            jobs_data = [
                {
                    "title": "Cricket Umpire Needed for T20 Tournament",
                    "job_type": "Umpire",
                    "description": "Looking for experienced cricket umpires for upcoming T20 tournament. Must have Level 1 certification.",
                    "sport_type": "Cricket",
                    "employment_type": "Per Match",
                    "experience_required": "1-2 years",
                    "certification_required": ["Level 1 Umpire Certification"],
                    "city": "Ahmedabad",
                    "location_type": "On-site",
                    "salary_min": 1500,
                    "salary_max": 2500,
                    "salary_type": "Per Match",
                    "skills_required": ["Match Management", "Rules Knowledge", "Communication"],
                    "language_required": ["English", "Gujarati", "Hindi"],
                    "application_deadline": datetime.utcnow() + timedelta(days=15),
                    "application_phone": "+919825111000",
                    "posted_by": 1,
                    "status": "active",
                    "is_verified": True
                },
                {
                    "title": "Football Coach for Youth Academy",
                    "job_type": "Coach",
                    "description": "Experienced football coach needed for youth academy (U-14 to U-19). Must have coaching certification.",
                    "sport_type": "Football",
                    "employment_type": "Full-time",
                    "experience_required": "3-5 years",
                    "certification_required": ["AFC/AIFF B License", "First Aid Certificate"],
                    "city": "Surat",
                    "location_type": "On-site",
                    "salary_min": 25000,
                    "salary_max": 40000,
                    "salary_type": "Per Month",
                    "other_benefits": ["Accommodation", "Travel Allowance"],
                    "skills_required": ["Youth Development", "Training Programs", "Match Strategy"],
                    "language_required": ["English", "Hindi"],
                    "application_deadline": datetime.utcnow() + timedelta(days=30),
                    "application_email": "hr@sportsacademy.com",
                    "posted_by": 1,
                    "status": "active",
                    "is_verified": True
                },
                {
                    "title": "Badminton Trainer for Club",
                    "job_type": "Trainer",
                    "description": "Professional badminton trainer required for sports club. Evening and weekend batches.",
                    "sport_type": "Badminton",
                    "employment_type": "Part-time",
                    "experience_required": "2-4 years",
                    "city": "Vadodara",
                    "location_type": "On-site",
                    "salary_min": 500,
                    "salary_max": 800,
                    "salary_type": "Per Session",
                    "skills_required": ["Player Development", "Technique Training"],
                    "application_phone": "+919879222333",
                    "posted_by": 1,
                    "status": "active"
                },
                {
                    "title": "Sports Physiotherapist",
                    "job_type": "Physio",
                    "description": "Qualified physiotherapist for sports injury treatment and rehabilitation.",
                    "sport_type": "All",
                    "employment_type": "Full-time",
                    "experience_required": "2-5 years",
                    "certification_required": ["BPT/MPT Degree", "Sports Physio Certification"],
                    "city": "Ahmedabad",
                    "location_type": "On-site",
                    "salary_min": 30000,
                    "salary_max": 50000,
                    "salary_type": "Per Month",
                    "skills_required": ["Injury Assessment", "Rehabilitation", "Sports Medicine"],
                    "application_email": "careers@sportsmed.in",
                    "posted_by": 1,
                    "status": "active",
                    "is_verified": True
                },
                {
                    "title": "Cricket Scorer - Tournament",
                    "job_type": "Scorer",
                    "description": "Digital scorer needed for cricket tournament. Experience with CricHeroes or similar apps preferred.",
                    "sport_type": "Cricket",
                    "employment_type": "Freelance",
                    "experience_required": "0-2 years",
                    "city": "Rajkot",
                    "location_type": "On-site",
                    "salary_min": 800,
                    "salary_max": 1200,
                    "salary_type": "Per Match",
                    "skills_required": ["Scoring Apps", "Match Recording"],
                    "application_phone": "+919825333444",
                    "posted_by": 1,
                    "status": "active"
                }
            ]

            for job_data in jobs_data:
                job = Job(**job_data)
                db.add(job)

            # ==================== SPORTS ACADEMIES ====================
            dictionary_data = [
                {
                    "term": "Champions Cricket Academy",
                    "sport": "Cricket",
                    "category": "Coaching",
                    "definition": "Professional cricket coaching academy with certified coaches and modern facilities. Specialized training for all age groups.",
                    "explanation": "Monthly Fee: ₹3,500 | Location: Ahmedabad | Timings: 6 AM - 8 PM | Features: Indoor nets, bowling machines, video analysis, match practice. Certified coaches with state/national level experience.",
                    "examples": ["Beginner batch: ₹3,000/month", "Advanced training: ₹5,000/month", "Personal coaching: ₹8,000/month"],
                    "images": ["https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=800", "https://images.unsplash.com/photo-1531415074968-036ba1b575da?w=800"],
                    "gujarati_term": "ક્રિકેટ એકેડમી",
                    "slug": "champions-cricket-academy",
                    "difficulty_level": "All Levels",
                    "is_featured": True
                },
                {
                    "term": "Elite Football Training Center",
                    "sport": "Football",
                    "category": "Training",
                    "definition": "Premier football academy with UEFA certified coaches. Focus on skill development, fitness, and tactical training.",
                    "explanation": "Monthly Fee: ₹4,000 | Location: Surat | Age Groups: U-10 to U-19 | Features: Professional turf, goalkeeper training, nutrition guidance, tournament participation. Summer camps available.",
                    "examples": ["Kids program (5-10 yrs): ₹2,500/month", "Youth training (11-16 yrs): ₹4,000/month", "Elite squad: ₹6,000/month"],
                    "images": ["https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800", "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=800"],
                    "slug": "elite-football-training",
                    "difficulty_level": "All Levels"
                },
                {
                    "term": "Smash Badminton Academy",
                    "sport": "Badminton",
                    "category": "Coaching",
                    "definition": "State-of-the-art badminton academy with international standard courts and expert coaching for competitive players.",
                    "explanation": "Monthly Fee: ₹3,000 | Location: Vadodara | Facilities: 6 wooden courts, AC hall, fitness center, physio support. Personal attention to technique and strategy. Weekend batches available.",
                    "examples": ["Hobby class: ₹2,000/month", "Competitive training: ₹3,500/month", "Tournament prep: ₹5,000/month"],
                    "images": ["https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=800"],
                    "gujarati_term": "બેડમિન્ટન એકેડમી",
                    "slug": "smash-badminton-academy",
                    "difficulty_level": "Intermediate"
                },
                {
                    "term": "Ace Tennis Academy",
                    "sport": "Tennis",
                    "category": "Coaching",
                    "definition": "Professional tennis coaching academy with hard courts and synthetic grass. AITA certified coaches available.",
                    "explanation": "Monthly Fee: ₹5,000 | Location: Rajkot | Features: 4 courts, ball machines, video analysis, fitness training, tournament entries. Special programs for juniors and adults.",
                    "examples": ["Beginner: ₹3,500/month", "Intermediate: ₹5,000/month", "Advanced: ₹7,000/month"],
                    "images": ["https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800", "https://images.unsplash.com/photo-1622279457486-62dcc4a431d6?w=800"],
                    "slug": "ace-tennis-academy",
                    "difficulty_level": "Advanced",
                    "is_featured": True
                },
                {
                    "term": "Pro Basketball Academy",
                    "sport": "Basketball",
                    "category": "Training",
                    "definition": "Complete basketball development program with NBA-style training methods. Focus on fundamentals and game IQ.",
                    "explanation": "Monthly Fee: ₹4,500 | Location: Gandhinagar | Age: 8+ years | Features: Indoor court, strength training, shooting drills, game strategy, league participation. Former national players as coaches.",
                    "examples": ["Youth development: ₹3,000/month", "Competitive program: ₹4,500/month", "Elite training: ₹6,500/month"],
                    "images": ["https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800"],
                    "slug": "pro-basketball-academy",
                    "difficulty_level": "All Levels"
                },
                {
                    "term": "Multi-Sport Excellence Center",
                    "sport": "All Sports",
                    "category": "Multi-Sport",
                    "definition": "Comprehensive sports training center offering cricket, football, badminton, table tennis, and athletics under one roof.",
                    "explanation": "Monthly Fee: ₹6,000 (all sports) | Location: Ahmedabad | Features: Multiple sport facilities, cross-training, fitness gym, sports psychology, nutrition counseling. Flexible batch timings.",
                    "examples": ["Single sport: ₹3,500/month", "Two sports: ₹5,500/month", "All sports access: ₹6,500/month"],
                    "images": ["https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=800", "https://images.unsplash.com/photo-1517649763962-0c623066013b?w=800"],
                    "gujarati_term": "મલ્ટી-સ્પોર્ટ સેન્ટર",
                    "slug": "multi-sport-center",
                    "difficulty_level": "All Levels",
                    "is_featured": True
                },
                {
                    "term": "Swimming & Aquatics Academy",
                    "sport": "Swimming",
                    "category": "Aquatics",
                    "definition": "Olympic-size swimming pool with certified swimming coaches. Programs for beginners to competitive swimmers.",
                    "explanation": "Monthly Fee: ₹4,000 | Location: Surat | Features: Heated pool, separate kids pool, diving board, water safety training, competition preparation. Morning and evening batches.",
                    "examples": ["Learn to swim: ₹2,500/month", "Stroke improvement: ₹3,500/month", "Competitive swimming: ₹5,000/month"],
                    "images": ["https://images.unsplash.com/photo-1519315901367-f34ff9154487?w=800"],
                    "slug": "swimming-academy",
                    "difficulty_level": "All Levels"
                }
            ]

            for dict_data in dictionary_data:
                entry = Dictionary(**dict_data)
                db.add(entry)

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
                    "min_teams": 8,
                    "age_category": "Open",
                    "gender_category": "Men",
                    "skill_level": "Intermediate",
                    "city": "Ahmedabad",
                    "venue_name": "Sardar Patel Stadium Grounds",
                    "venue_address": "Near Sardar Patel Stadium, Motera",
                    "start_date": datetime.utcnow() + timedelta(days=30),
                    "end_date": datetime.utcnow() + timedelta(days=45),
                    "registration_start": datetime.utcnow(),
                    "registration_deadline": datetime.utcnow() + timedelta(days=20),
                    "entry_fee": 5000,
                    "prize_pool": 200000,
                    "prize_distribution": [
                        {"position": "Winner", "prize": 100000},
                        {"position": "Runner-up", "prize": 60000},
                        {"position": "3rd Place", "prize": 40000}
                    ],
                    "documents_required": ["ID Proof", "Age Certificate"],
                    "rules": "Standard T20 cricket rules apply. Tennis ball tournament. 15 overs per side.",
                    "contact_person": "Rajesh Patel",
                    "contact_number": "+919825000111",
                    "contact_email": "apl2025@gmail.com",
                    "banner_image": "https://images.unsplash.com/photo-1540747913346-19e32dc3e97e?w=800",
                    "organizer_id": 1,
                    "status": "upcoming",
                    "is_verified": True,
                    "is_featured": True
                },
                {
                    "name": "Surat Football Championship U-19",
                    "description": "Under-19 football championship with knockout format. Great opportunity for young talents!",
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
                    "prize_distribution": [
                        {"position": "Winner", "prize": 80000},
                        {"position": "Runner-up", "prize": 50000},
                        {"position": "3rd Place", "prize": 20000}
                    ],
                    "contact_person": "Amit Shah",
                    "contact_number": "+919879000222",
                    "banner_image": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?w=800",
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
                    "banner_image": "https://images.unsplash.com/photo-1626224583764-f87db24ac4ea?w=800",
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
                    "banner_image": "https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800",
                    "organizer_id": 1,
                    "status": "upcoming"
                },
                {
                    "name": "Gandhinagar Basketball League 2025",
                    "description": "Premier basketball league featuring top teams from across Gujarat. Fast-paced action guaranteed!",
                    "sport_type": "Basketball",
                    "tournament_type": "League",
                    "format": "5-on-5",
                    "team_size": 12,
                    "max_teams": 10,
                    "min_teams": 8,
                    "age_category": "Open",
                    "gender_category": "Men",
                    "skill_level": "Professional",
                    "city": "Gandhinagar",
                    "venue_name": "Capital Complex Sports Arena",
                    "venue_address": "Sector 10, Gandhinagar",
                    "start_date": datetime.utcnow() + timedelta(days=50),
                    "end_date": datetime.utcnow() + timedelta(days=80),
                    "registration_start": datetime.utcnow(),
                    "registration_deadline": datetime.utcnow() + timedelta(days=28),
                    "entry_fee": 8000,
                    "prize_pool": 300000,
                    "prize_distribution": [
                        {"position": "Winner", "prize": 150000},
                        {"position": "Runner-up", "prize": 100000},
                        {"position": "3rd Place", "prize": 50000}
                    ],
                    "documents_required": ["ID Proof", "Team Registration"],
                    "rules": "FIBA rules apply. 4 quarters of 10 minutes each.",
                    "contact_person": "Kiran Desai",
                    "contact_number": "+919825444555",
                    "contact_email": "gandhibbl@gmail.com",
                    "banner_image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800",
                    "live_scoring": True,
                    "organizer_id": 1,
                    "status": "upcoming",
                    "is_verified": True,
                    "is_featured": True
                },
                {
                    "name": "Bhavnagar Marathon 2025",
                    "description": "Annual marathon event - 5K, 10K, and Half Marathon categories. Run for fitness and fun!",
                    "sport_type": "Athletics",
                    "tournament_type": "Individual",
                    "age_category": "Open",
                    "gender_category": "Mixed",
                    "max_teams": 500,
                    "city": "Bhavnagar",
                    "venue_name": "Gaurishankar Lake Start Point",
                    "venue_address": "Gaurishankar Lake Road, Bhavnagar",
                    "start_date": datetime.utcnow() + timedelta(days=60),
                    "registration_deadline": datetime.utcnow() + timedelta(days=35),
                    "entry_fee": 300,
                    "prize_pool": 100000,
                    "prize_distribution": [
                        {"position": "1st - Half Marathon", "prize": 25000},
                        {"position": "2nd - Half Marathon", "prize": 15000},
                        {"position": "3rd - Half Marathon", "prize": 10000},
                        {"position": "1st - 10K", "prize": 15000},
                        {"position": "1st - 5K", "prize": 10000}
                    ],
                    "documents_required": ["ID Proof", "Medical Certificate"],
                    "rules": "Participants must carry their own hydration. Medical support available.",
                    "contact_person": "Dr. Mehul Patel",
                    "contact_number": "+919879555666",
                    "contact_email": "bhavnagarmarathon@gmail.com",
                    "banner_image": "https://images.unsplash.com/photo-1552674605-db6ffd4facb5?w=800",
                    "certificates_provided": True,
                    "organizer_id": 1,
                    "status": "upcoming",
                    "is_verified": True
                },
                {
                    "name": "Jamnagar Volleyball Championship",
                    "description": "Beach volleyball tournament on the shores of Gujarat. Sand, sun, and sports!",
                    "sport_type": "Volleyball",
                    "tournament_type": "Knockout",
                    "format": "Beach Volleyball (2v2)",
                    "team_size": 4,
                    "max_teams": 24,
                    "age_category": "Open",
                    "gender_category": "Mixed",
                    "city": "Jamnagar",
                    "venue_name": "Marine National Park Beach",
                    "venue_address": "Marine National Park, Jamnagar",
                    "start_date": datetime.utcnow() + timedelta(days=55),
                    "end_date": datetime.utcnow() + timedelta(days=57),
                    "registration_deadline": datetime.utcnow() + timedelta(days=30),
                    "entry_fee": 1500,
                    "prize_pool": 75000,
                    "prize_distribution": [
                        {"position": "Winner", "prize": 40000},
                        {"position": "Runner-up", "prize": 25000},
                        {"position": "3rd Place", "prize": 10000}
                    ],
                    "contact_person": "Yash Jadeja",
                    "contact_number": "+919825666777",
                    "banner_image": "https://images.unsplash.com/photo-1612872087720-bb876e2e67d1?w=800",
                    "organizer_id": 1,
                    "status": "upcoming"
                }
            ]

            for tournament_data in tournaments_data:
                tournament = Tournament(**tournament_data)
                db.add(tournament)

            await db.commit()
            print("SUCCESS: Marketplace data seeded successfully!")
            print("- Added 5 sports shops")
            print("- Added 5 job postings")
            print("- Added 7 sports academies with photos & prices")
            print("- Added 7 tournaments with images")

        except Exception as e:
            print(f"ERROR: Failed to seed data: {str(e)}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(seed_marketplace_data())

