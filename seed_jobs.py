import asyncio
from datetime import datetime, timedelta
from sqlalchemy import select
from app.core.database import AsyncSessionLocal, init_db
from app.models.models import Job, User

async def get_or_create_admin_user():
    """Get or create an admin user for posting jobs"""
    async with AsyncSessionLocal() as db:
        try:
            # Try to find existing user
            result = await db.execute(select(User).where(User.phone_number == "+919999999999"))
            user = result.scalar_one_or_none()
            
            if user:
                return user.id
            else:
                # Create a basic admin user for job postings
                admin_user = User(
                    phone_number="+919999999999",
                    name="Admin",
                    is_verified=True,
                    onboarding_completed=True
                )
                db.add(admin_user)
                await db.commit()
                await db.refresh(admin_user)
                return admin_user.id
        except Exception as e:
            await db.rollback()
            print(f"Error getting/creating admin user: {str(e)}")
            return 1  # Fallback to ID 1

async def clear_existing_jobs():
    """Clear existing jobs"""
    async with AsyncSessionLocal() as db:
        try:
            result = await db.execute(select(Job))
            jobs = result.scalars().all()
            for job in jobs:
                await db.delete(job)
            await db.commit()
            print(f"Cleared {len(jobs)} existing jobs")
        except Exception as e:
            await db.rollback()
            print(f"Error clearing jobs: {str(e)}")

async def seed_jobs_data():
    """Seed comprehensive sports jobs data"""
    await init_db()
    print("Starting jobs data seeding...")
    
    # Clear existing jobs first
    await clear_existing_jobs()
    
    # Get admin user ID
    admin_id = await get_or_create_admin_user()
    
    async with AsyncSessionLocal() as db:
        try:
            jobs_data = [
                # ============ CRICKET JOBS ============
                {
                    "posted_by": admin_id,
                    "title": "Cricket Umpire - State Level",
                    "description": "Gujarat Cricket Association is looking for certified cricket umpires for state-level matches. Must have BCCI certification and 2+ years experience in local matches. Officiate matches as per ICC rules, make on-field decisions, and maintain match records.",
                    "job_type": "Umpire",
                    "employment_type": "Per Match",
                    "sport_type": "Cricket",
                    "city": "Ahmedabad",
                    "state": "Gujarat",
                    "salary_min": 2000,
                    "salary_max": 5000,
                    "salary_type": "per match",
                    "experience_required": "2+ years umpiring experience",
                    "certification_required": ["BCCI Level 1 Umpire Certification"],
                    "skills_required": ["ICC Rules Knowledge", "On-field Decision Making", "Match Management"],
                    "application_email": "umpires@gujaratcricket.com",
                    "application_phone": "+919876543210",
                    "application_deadline": datetime.now() + timedelta(days=30),
                    "is_verified": True
                },
                {
                    "posted_by": admin_id,
                    "title": "Cricket Coach - Academy Head Coach",
                    "description": "Champions Cricket Academy seeking head coach for training players aged 10-18 years. Must have playing experience at district level or above. Conduct daily practice sessions, plan training programs, mentor young players, and organize practice matches.",
                    "job_type": "Coach",
                    "employment_type": "Full-time",
                    "sport_type": "Cricket",
                    "city": "Surat",
                    "state": "Gujarat",
                    "salary_min": 25000,
                    "salary_max": 40000,
                    "salary_type": "per month",
                    "experience_required": "3+ years coaching experience",
                    "certification_required": ["NIS Coaching Certificate"],
                    "skills_required": ["Player Development", "Training Program Design", "Youth Coaching"],
                    "other_benefits": ["Accommodation", "Travel Allowance"],
                    "application_email": "hr@championsacademy.com",
                    "application_phone": "+919876543211",
                    "application_deadline": datetime.now() + timedelta(days=45),
                    "is_verified": True
                },
                {
                    "posted_by": admin_id,
                    "title": "Cricket Scorer - Professional",
                    "description": "Vadodara Sports Council needs professional cricket scorer for state and local tournaments. Must be proficient in digital scoring apps and traditional scoring methods. Maintain accurate match records and coordinate with umpires.",
                    "job_type": "Scorer",
                    "employment_type": "Freelance",
                    "sport_type": "Cricket",
                    "city": "Vadodara",
                    "state": "Gujarat",
                    "salary_min": 1500,
                    "salary_max": 3000,
                    "salary_type": "per match",
                    "experience_required": "1+ years scoring experience",
                    "certification_required": ["BCCI Scorer Certification"],
                    "skills_required": ["Digital Scoring", "CricClubs App", "Match Recording"],
                    "application_email": "scoring@vadodarasports.com",
                    "application_phone": "+919876543212",
                    "application_deadline": datetime.now() + timedelta(days=20),
                    "is_verified": True
                },
                
                # ============ FOOTBALL JOBS ============
                {
                    "posted_by": admin_id,
                    "title": "Football Coach - Youth Development",
                    "description": "Rajkot Football Academy hiring youth football coach for U-14 and U-16 teams. Focus on skill development and team building. UEFA or AIFF certification required. Train youth players, develop training programs, scout talent.",
                    "job_type": "Coach",
                    "employment_type": "Full-time",
                    "sport_type": "Football",
                    "city": "Rajkot",
                    "state": "Gujarat",
                    "salary_min": 30000,
                    "salary_max": 45000,
                    "salary_type": "per month",
                    "experience_required": "2+ years youth coaching",
                    "certification_required": ["AIFF C License or higher"],
                    "skills_required": ["Youth Training", "Talent Scouting", "Match Strategy"],
                    "application_email": "coach@rajkotfootball.com",
                    "application_phone": "+919876543213",
                    "application_deadline": datetime.now() + timedelta(days=25),
                    "is_verified": True
                },
                {
                    "posted_by": admin_id,
                    "title": "Football Referee - District Level",
                    "description": "Gandhinagar Sports Authority seeking certified football referee for district-level matches and tournaments. Must have good fitness and knowledge of FIFA rules. Officiate football matches and enforce game rules.",
                    "job_type": "Umpire",
                    "employment_type": "Per Match",
                    "sport_type": "Football",
                    "city": "Gandhinagar",
                    "state": "Gujarat",
                    "salary_min": 1500,
                    "salary_max": 4000,
                    "salary_type": "per match",
                    "experience_required": "1+ years refereeing experience",
                    "certification_required": ["AIFF Referee Certification"],
                    "skills_required": ["FIFA Rules", "Match Management", "Fitness"],
                    "application_email": "referee@gandhinagarsports.com",
                    "application_phone": "+919876543214",
                    "application_deadline": datetime.now() + timedelta(days=35),
                    "is_verified": True
                },
                
                # ============ BADMINTON JOBS ============
                {
                    "posted_by": admin_id,
                    "title": "Badminton Coach - Advanced Training",
                    "description": "Elite Badminton Academy needs professional badminton coach for advanced level players. Experience in competitive training and tournament preparation required. Provide advanced skill training and strategy development.",
                    "job_type": "Coach",
                    "employment_type": "Full-time",
                    "sport_type": "Badminton",
                    "city": "Ahmedabad",
                    "state": "Gujarat",
                    "salary_min": 28000,
                    "salary_max": 42000,
                    "salary_type": "per month",
                    "experience_required": "3+ years professional coaching",
                    "certification_required": ["BWF Level 1 Coaching Certificate"],
                    "skills_required": ["Advanced Training", "Tournament Preparation", "Performance Analysis"],
                    "application_email": "jobs@elitebadminton.com",
                    "application_phone": "+919876543215",
                    "application_deadline": datetime.now() + timedelta(days=40),
                    "is_verified": True
                },
                {
                    "posted_by": admin_id,
                    "title": "Badminton Umpire - Tournament Official",
                    "description": "Surat Badminton Association looking for certified badminton umpire for state and district level tournaments. Must be familiar with BWF rules and regulations. Officiate badminton matches and maintain scoring.",
                    "job_type": "Umpire",
                    "employment_type": "Per Match",
                    "sport_type": "Badminton",
                    "city": "Surat",
                    "state": "Gujarat",
                    "salary_min": 1000,
                    "salary_max": 2500,
                    "salary_type": "per match",
                    "experience_required": "6 months+ umpiring experience",
                    "certification_required": ["BWF Umpire Certification"],
                    "skills_required": ["BWF Rules", "Score Tracking", "Match Coordination"],
                    "application_email": "umpire@suratbadminton.com",
                    "application_phone": "+919876543216",
                    "application_deadline": datetime.now() + timedelta(days=15),
                    "is_verified": True
                },
                
                # ============ TENNIS JOBS ============
                {
                    "posted_by": admin_id,
                    "title": "Tennis Coach - Professional",
                    "description": "Vadodara Tennis Club hiring professional tennis coach for adult and junior players. Focus on technique improvement and competitive play. USPTA or PTR certification preferred. Provide private and group coaching.",
                    "job_type": "Coach",
                    "employment_type": "Full-time",
                    "sport_type": "Tennis",
                    "city": "Vadodara",
                    "state": "Gujarat",
                    "salary_min": 32000,
                    "salary_max": 50000,
                    "salary_type": "per month",
                    "experience_required": "4+ years professional coaching",
                    "certification_required": ["USPTA/PTR Certification"],
                    "skills_required": ["Technical Training", "Tournament Prep", "Fitness Conditioning"],
                    "application_email": "coach@vadodaratennis.com",
                    "application_phone": "+919876543217",
                    "application_deadline": datetime.now() + timedelta(days=50),
                    "is_verified": True
                },
                {
                    "posted_by": admin_id,
                    "title": "Tennis Umpire - Chair Umpire",
                    "description": "Rajkot Tennis Association needs qualified chair umpire for tennis tournaments. Must have certification and experience in officiating matches at club/district level. Chair umpiring and score calling.",
                    "job_type": "Umpire",
                    "employment_type": "Per Match",
                    "sport_type": "Tennis",
                    "city": "Rajkot",
                    "state": "Gujarat",
                    "salary_min": 1500,
                    "salary_max": 3500,
                    "salary_type": "per match",
                    "experience_required": "1+ years umpiring",
                    "certification_required": ["ITF White Badge"],
                    "skills_required": ["Chair Umpiring", "Score Calling", "Rule Interpretation"],
                    "application_email": "umpire@rajkottennis.com",
                    "application_phone": "+919876543218",
                    "application_deadline": datetime.now() + timedelta(days=22),
                    "is_verified": True
                },
                
                # ============ BASKETBALL JOBS ============
                {
                    "posted_by": admin_id,
                    "title": "Basketball Coach - School Program",
                    "description": "Gandhinagar International School hiring basketball coach for school sports program. Train students aged 12-18 years in fundamentals and competitive play. Conduct daily practice sessions.",
                    "job_type": "Coach",
                    "employment_type": "Part-time",
                    "sport_type": "Basketball",
                    "city": "Gandhinagar",
                    "state": "Gujarat",
                    "salary_min": 15000,
                    "salary_max": 25000,
                    "salary_type": "per month",
                    "experience_required": "2+ years coaching experience",
                    "certification_required": ["Basketball Coaching Certificate"],
                    "skills_required": ["Youth Training", "Game Strategy", "Team Management"],
                    "application_email": "sports@gischool.com",
                    "application_phone": "+919876543219",
                    "application_deadline": datetime.now() + timedelta(days=18),
                    "is_verified": True
                },
                {
                    "posted_by": admin_id,
                    "title": "Basketball Referee - Local Leagues",
                    "description": "Ahmedabad Basketball League needs certified basketball referee for local leagues and school tournaments. Knowledge of FIBA rules required. Officiate basketball games and call fouls.",
                    "job_type": "Umpire",
                    "employment_type": "Per Match",
                    "sport_type": "Basketball",
                    "city": "Ahmedabad",
                    "state": "Gujarat",
                    "salary_min": 1000,
                    "salary_max": 2000,
                    "salary_type": "per match",
                    "experience_required": "6 months+ refereeing",
                    "certification_required": ["Basketball Referee Certificate"],
                    "skills_required": ["FIBA Rules", "Foul Calling", "Game Management"],
                    "application_email": "referee@amdbasketball.com",
                    "application_phone": "+919876543220",
                    "application_deadline": datetime.now() + timedelta(days=12),
                    "is_verified": True
                },
                
                # ============ VOLLEYBALL JOBS ============
                {
                    "posted_by": admin_id,
                    "title": "Volleyball Coach - College Team",
                    "description": "Surat College of Sports hiring head volleyball coach for college men's and women's teams. Prepare teams for inter-college competitions. Team training and match strategy development.",
                    "job_type": "Coach",
                    "employment_type": "Full-time",
                    "sport_type": "Volleyball",
                    "city": "Surat",
                    "state": "Gujarat",
                    "salary_min": 22000,
                    "salary_max": 35000,
                    "salary_type": "per month",
                    "experience_required": "2+ years coaching",
                    "certification_required": ["Volleyball Coaching Certificate"],
                    "skills_required": ["Team Training", "Match Strategy", "Player Development"],
                    "application_email": "coach@suratcollege.edu",
                    "application_phone": "+919876543221",
                    "application_deadline": datetime.now() + timedelta(days=28),
                    "is_verified": True
                },
                {
                    "posted_by": admin_id,
                    "title": "Volleyball Scorer - Tournament Official",
                    "description": "Bhavnagar Sports Complex needs official scorer for volleyball tournaments. Must be proficient in volleyball scoring systems and match recording. Maintain match scores and track statistics.",
                    "job_type": "Scorer",
                    "employment_type": "Freelance",
                    "sport_type": "Volleyball",
                    "city": "Bhavnagar",
                    "state": "Gujarat",
                    "salary_min": 800,
                    "salary_max": 1500,
                    "salary_type": "per match",
                    "experience_required": "Basic scoring knowledge",
                    "certification_required": ["Volleyball Scoring Certificate"],
                    "skills_required": ["Scoring Systems", "Match Recording", "Statistics Tracking"],
                    "application_email": "scoring@bhavnagarsports.com",
                    "application_phone": "+919876543222",
                    "application_deadline": datetime.now() + timedelta(days=10),
                    "is_verified": True
                },
                
                # ============ MULTI-SPORT JOBS ============
                {
                    "posted_by": admin_id,
                    "title": "Athletics Coach - Track & Field",
                    "description": "Jamnagar Athletics Club hiring track and field coach specializing in sprints, middle distance, and field events. Train athletes for state-level competitions. Athlete training programs and technique coaching.",
                    "job_type": "Coach",
                    "employment_type": "Full-time",
                    "sport_type": "All",
                    "city": "Jamnagar",
                    "state": "Gujarat",
                    "salary_min": 26000,
                    "salary_max": 38000,
                    "salary_type": "per month",
                    "experience_required": "3+ years coaching in athletics",
                    "certification_required": ["NIS Coaching Diploma"],
                    "skills_required": ["Training Programs", "Technique Coaching", "Performance Monitoring"],
                    "application_email": "coach@jamnagarathletics.com",
                    "application_phone": "+919876543223",
                    "application_deadline": datetime.now() + timedelta(days=33),
                    "is_verified": True
                },
                {
                    "posted_by": admin_id,
                    "title": "Multi-Sport Umpire/Referee",
                    "description": "Vadodara Sports Federation needs versatile sports official with certifications in multiple sports. Needed for school and club-level events. Officiate various sports and maintain fairness.",
                    "job_type": "Umpire",
                    "employment_type": "Per Match",
                    "sport_type": "All",
                    "city": "Vadodara",
                    "state": "Gujarat",
                    "salary_min": 1200,
                    "salary_max": 2500,
                    "salary_type": "per match",
                    "experience_required": "1+ years in sports officiating",
                    "certification_required": ["Certifications in 2+ sports"],
                    "skills_required": ["Multi-Sport Rules", "Match Management", "Fairness"],
                    "application_email": "officials@vadodarasportsfed.com",
                    "application_phone": "+919876543224",
                    "application_deadline": datetime.now() + timedelta(days=27),
                    "is_verified": True
                }
            ]
            
            # Create job entries
            for job_data in jobs_data:
                job = Job(**job_data)
                db.add(job)
            
            await db.commit()
            print(f"\nSuccessfully added {len(jobs_data)} jobs!")
            print("\nJobs Summary:")
            print(f"  - Umpire/Referee jobs: {sum(1 for j in jobs_data if j['job_type'] == 'Umpire')}")
            print(f"  - Coach jobs: {sum(1 for j in jobs_data if j['job_type'] == 'Coach')}")
            print(f"  - Scorer jobs: {sum(1 for j in jobs_data if j['job_type'] == 'Scorer')}")
            print(f"\nCities covered:")
            cities = set(j['city'] for j in jobs_data)
            for city in sorted(cities):
                count = sum(1 for j in jobs_data if j['city'] == city)
                print(f"  - {city}: {count} jobs")
            print(f"\nSports covered:")
            sports = set(j['sport_type'] for j in jobs_data)
            for sport in sorted(sports):
                count = sum(1 for j in jobs_data if j['sport_type'] == sport)
                print(f"  - {sport}: {count} jobs")
            
        except Exception as e:
            await db.rollback()
            print(f"ERROR: Failed to seed jobs data: {str(e)}")
            import traceback
            traceback.print_exc()
            raise

if __name__ == "__main__":
    asyncio.run(seed_jobs_data())
    print("\nJobs data seeding complete!")
