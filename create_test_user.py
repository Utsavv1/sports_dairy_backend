import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_test_user():
    """Create a test user with complete profile"""
    try:
        # Get MongoDB connection string
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "sports_diary")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ Connected to MongoDB\n")
        
        # Check if user already exists
        phone = "+919999999999"
        existing_user = await db.users.find_one({"phone": phone})
        
        user_data = {
            "phone": phone,
            "name": "Test Player",
            "email": "test@player.com",
            "age": 25,
            "gender": "Male",
            "role": "player",
            "city": "Ahmedabad",
            "state": "Gujarat",
            "bio": "Professional cricket player",
            "sports_interests": ["Cricket", "Football", "Badminton"],
            "player_position": "All-rounder",
            "playing_style": "Aggressive",
            "is_verified": True,
            "onboarding_completed": True,
            "updated_at": datetime.utcnow()
        }
        
        if existing_user:
            # Update existing user
            await db.users.update_one(
                {"phone": phone},
                {"$set": user_data}
            )
            print(f"✅ Updated existing user: {phone}")
        else:
            # Create new user
            user_data["created_at"] = datetime.utcnow()
            result = await db.users.insert_one(user_data)
            print(f"✅ Created new user: {phone}")
            print(f"   User ID: {result.inserted_id}")
        
        # Verify the user
        user = await db.users.find_one({"phone": phone})
        
        print("\n" + "="*60)
        print("SUCCESS! Test user details:")
        print("="*60)
        print(f"   Phone: {user.get('phone')}")
        print(f"   Name: {user.get('name')}")
        print(f"   Email: {user.get('email')}")
        print(f"   Role: {user.get('role')}")
        print(f"   City: {user.get('city')}")
        print(f"   Sports: {user.get('sports_interests')}")
        print(f"   Onboarding Complete: {user.get('onboarding_completed')}")
        print(f"\nUse this to login:")
        print(f"   Phone: {phone}")
        print(f"   OTP: Any 6 digits (OTP will be shown in console)")
        print("="*60 + "\n")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ ERROR: Failed to create user: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(create_test_user())
