import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal, init_db
from app.models.models import User
from sqlalchemy import select

async def create_test_user():
    """Create a test user with complete profile"""
    async with AsyncSessionLocal() as db:
        try:
            # Check if user already exists
            phone = "+919999999999"
            result = await db.execute(select(User).where(User.phone == phone))
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                # Update existing user
                existing_user.name = "Test Player"
                existing_user.email = "test@player.com"
                existing_user.age = 25
                existing_user.gender = "Male"
                existing_user.role = "player"
                existing_user.city = "Ahmedabad"
                existing_user.state = "Gujarat"
                existing_user.bio = "Professional cricket player"
                existing_user.sports_interests = ["Cricket", "Football", "Badminton"]
                existing_user.player_position = "All-rounder"
                existing_user.playing_style = "Aggressive"
                existing_user.is_verified = True
                existing_user.onboarding_completed = True
                
                print(f"Updated existing user: {phone}")
            else:
                # Create new user
                new_user = User(
                    phone=phone,
                    name="Test Player",
                    email="test@player.com",
                    age=25,
                    gender="Male",
                    role="player",
                    city="Ahmedabad",
                    state="Gujarat",
                    bio="Professional cricket player",
                    sports_interests=["Cricket", "Football", "Badminton"],
                    player_position="All-rounder",
                    playing_style="Aggressive",
                    is_verified=True,
                    onboarding_completed=True
                )
                
                db.add(new_user)
                print(f"Created new user: {phone}")
            
            await db.commit()
            
            # Verify the user
            result = await db.execute(select(User).where(User.phone == phone))
            user = result.scalar_one_or_none()
            
            print("\nSUCCESS! Test user created:")
            print(f"   Phone: {user.phone}")
            print(f"   Name: {user.name}")
            print(f"   Role: {user.role}")
            print(f"   City: {user.city}")
            print(f"   Sports: {user.sports_interests}")
            print(f"   Onboarding Complete: {user.onboarding_completed}")
            print(f"\nUse this to login:")
            print(f"   Phone: {phone}")
            print(f"   OTP: Any 6 digits (will be shown)")
            
        except Exception as e:
            print(f"ERROR: Failed to create user: {str(e)}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(init_db())
    asyncio.run(create_test_user())

