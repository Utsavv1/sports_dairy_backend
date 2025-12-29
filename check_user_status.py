"""
Check user status in database
"""
import asyncio
import sys

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def check_users():
    from app.core.database import AsyncSessionLocal
    from app.models.models import User
    from sqlalchemy import select
    
    async with AsyncSessionLocal() as session:
        print("\nChecking users in database...")
        print("="*60)
        
        # Get all users
        result = await session.execute(select(User))
        users = result.scalars().all()
        
        if not users:
            print("NO USERS FOUND IN DATABASE")
            print("\nThis means:")
            print("  - First time login will create a new user")
            print("  - New user will have onboarding_completed = False")
            print("  - User will be redirected to create-profile correctly")
        else:
            print(f"Found {len(users)} user(s):\n")
            for user in users:
                print(f"Phone: {user.phone}")
                print(f"  Name: {user.name or '(not set)'}")
                print(f"  Role: {user.role or '(not set)'}")
                print(f"  City: {user.city or '(not set)'}")
                print(f"  Sports: {user.sports_interests or '(not set)'}")
                print(f"  Onboarding Complete: {user.onboarding_completed}")
                print(f"  Is Verified: {user.is_verified}")
                print()
                
                # Determine what should happen on login
                if user.onboarding_completed:
                    print(f"  --> On login: Should go to DASHBOARD")
                elif not user.name:
                    print(f"  --> On login: Should go to CREATE PROFILE (no name)")
                elif not user.role:
                    print(f"  --> On login: Should go to CREATE PROFILE (no role)")
                else:
                    print(f"  --> On login: Should continue ONBOARDING")
                print("-" * 60)
        
        print("\n")

if __name__ == "__main__":
    asyncio.run(check_users())

