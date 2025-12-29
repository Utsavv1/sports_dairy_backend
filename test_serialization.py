"""Test if all jobs can be serialized to JobResponse schema"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.models import Job
from app.schemas.schemas import JobResponse

async def test_all_jobs():
    """Test each job individually"""
    async with AsyncSessionLocal() as db:
        query = select(Job).where(Job.status == "active")
        result = await db.execute(query)
        jobs = result.scalars().all()
        
        print(f"\nTesting {len(jobs)} jobs for serialization...")
        print("="*70)
        
        failed = []
        for job in jobs:
            try:
                # Try to serialize
                job_response = JobResponse.model_validate(job)
                print(f"[OK] {job.id}: {job.title}")
            except Exception as e:
                print(f"[ERROR] {job.id}: {job.title}")
                print(f"  Error: {str(e)}")
                failed.append((job.id, job.title, str(e)))
        
        print("="*70)
        if failed:
            print(f"\n{len(failed)} jobs FAILED serialization:")
            for job_id, title, error in failed:
                print(f"\n  Job ID {job_id}: {title}")
                print(f"  Error: {error}")
        else:
            print("\nALL jobs can be serialized successfully! ✓")

if __name__ == "__main__":
    asyncio.run(test_all_jobs())

