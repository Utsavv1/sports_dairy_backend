"""Simple test to verify Jobs API works locally"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.models import Job
from app.schemas.schemas import JobResponse

async def test_schema():
    """Test if JobResponse schema can serialize Job model"""
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Job).limit(1))
        job = result.scalar_one_or_none()
        
        if job:
            try:
                # Try to create a response using the schema
                job_response = JobResponse.from_orm(job)
                print("SUCCESS! Schema can serialize Job model")
                print(f"\nJob Title: {job_response.title}")
                print(f"Job Type: {job_response.job_type}")
                print(f"City: {job_response.city}")
                print(f"Salary: Rs.{job_response.salary_min} - Rs.{job_response.salary_max}")
                return True
            except Exception as e:
                print(f"ERROR: {str(e)}")
                print(f"\nJob model fields: {dir(job)}")
                return False
        else:
            print("No jobs found in database!")
            return False

if __name__ == "__main__":
    success = asyncio.run(test_schema())
    if success:
        print("\n[OK] Jobs API should work now!")
    else:
        print("\n[ERROR] Schema still has issues")

