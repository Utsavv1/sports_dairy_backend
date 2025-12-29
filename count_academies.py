"""
Count academies in database
"""
import asyncio
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def count_academies():
    from app.core.database import AsyncSessionLocal
    from app.models.models import Dictionary
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Dictionary))
        items = result.scalars().all()
        
        print(f'\nTotal academies in database: {len(items)}')
        print('='*60)
        
        if items:
            for item in items:
                print(f'  - {item.term}')
                print(f'    City: {item.city or "Not set"}')
                print(f'    Sport: {item.sport}')
                print(f'    Category: {item.category or "Not set"}')
                print()
        else:
            print('  No academies found!')
        
        print('='*60)

if __name__ == "__main__":
    asyncio.run(count_academies())

