import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.models import Job

async def check_jobs():
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Job))
        jobs = result.scalars().all()
        
        print(f"\n{'='*60}")
        print(f"DATABASE VERIFICATION")
        print(f"{'='*60}")
        print(f"\nTotal jobs in database: {len(jobs)}")
        print(f"\nFirst 5 jobs:")
        for i, job in enumerate(jobs[:5], 1):
            print(f"  {i}. {job.title} ({job.job_type}) - {job.city}")
        
        if len(jobs) > 5:
            print(f"\n... and {len(jobs) - 5} more jobs")
        
        print(f"\nJobs by type:")
        job_types = {}
        for job in jobs:
            job_types[job.job_type] = job_types.get(job.job_type, 0) + 1
        for job_type, count in job_types.items():
            print(f"  - {job_type}: {count}")
        
        print(f"\nJobs by city:")
        cities = {}
        for job in jobs:
            cities[job.city] = cities.get(job.city, 0) + 1
        for city, count in sorted(cities.items()):
            print(f"  - {city}: {count}")
        
        print(f"\n{'='*60}")
        print(f"STATUS: {'VERIFIED - Data is in database!' if len(jobs) > 0 else 'ERROR - No data found!'}")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    asyncio.run(check_jobs())

