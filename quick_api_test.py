"""Quick test of the jobs API endpoint"""
import asyncio
from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.models import Job

async def test_query():
    """Test the exact query used in the API"""
    async with AsyncSessionLocal() as db:
        try:
            # Same query as API
            query = select(Job).where(Job.status == "active")
            query = query.order_by(Job.is_featured.desc(), Job.created_at.desc())
            
            result = await db.execute(query)
            jobs = result.scalars().all()
            
            print(f"SUCCESS! Found {len(jobs)} jobs")
            for i, job in enumerate(jobs[:3], 1):
                print(f"  {i}. {job.title} - {job.city}")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_query())

