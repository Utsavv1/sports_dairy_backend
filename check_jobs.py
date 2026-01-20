import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def check_jobs():
    """Check all jobs in MongoDB database"""
    try:
        # Get MongoDB connection string
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "sports_diary")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        
        # Get all jobs
        jobs = await db.jobs.find().to_list(length=None)
        
        print(f"\n{'='*60}")
        print(f"DATABASE VERIFICATION")
        print(f"{'='*60}")
        print(f"\nTotal jobs in database: {len(jobs)}")
        print(f"\nFirst 5 jobs:")
        for i, job in enumerate(jobs[:5], 1):
            title = job.get('title', 'N/A')
            job_type = job.get('job_type', 'N/A')
            city = job.get('city', 'N/A')
            print(f"  {i}. {title} ({job_type}) - {city}")
        
        if len(jobs) > 5:
            print(f"\n... and {len(jobs) - 5} more jobs")
        
        print(f"\nJobs by type:")
        job_types = {}
        for job in jobs:
            jt = job.get('job_type', 'N/A')
            job_types[jt] = job_types.get(jt, 0) + 1
        for job_type, count in job_types.items():
            print(f"  - {job_type}: {count}")
        
        print(f"\nJobs by city:")
        cities = {}
        for job in jobs:
            city = job.get('city', 'N/A')
            cities[city] = cities.get(city, 0) + 1
        for city, count in sorted(cities.items()):
            print(f"  - {city}: {count}")
        
        print(f"\n{'='*60}")
        status = 'VERIFIED - Data is in database!' if len(jobs) > 0 else 'ERROR - No data found!'
        print(f"STATUS: {status}")
        print(f"{'='*60}\n")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_jobs())
