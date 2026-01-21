"""
Check user status in MongoDB database
"""
import asyncio
import sys
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set encoding
sys.stdout.reconfigure(encoding='utf-8')

async def check_users():
    """Check all users in MongoDB database"""
    try:
        # Get MongoDB connection string
        mongodb_url = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        database_name = os.getenv("DATABASE_NAME", "sports_diary")
        
        # Connect to MongoDB
        client = AsyncIOMotorClient(mongodb_url)
        db = client[database_name]
        
        # Test connection
        await client.admin.command('ping')
        
        print("\nChecking users in database...")
        print("="*60)
        
        # Get all users
        users = await db.users.find().to_list(length=None)
        
        if not users:
            print("NO USERS FOUND IN DATABASE")
            print("\nThis means:")
            print("  - First time login will create a new user")
            print("  - New user will have onboarding_completed = False")
            print("  - User will be redirected to create-profile correctly")
        else:
            print(f"Found {len(users)} user(s):\n")
            for user in users:
                phone = user.get('phone', 'N/A')
                name = user.get('name') or '(not set)'
                role = user.get('role') or '(not set)'
                city = user.get('city') or '(not set)'
                sports = user.get('sports_interests') or '(not set)'
                onboarding = user.get('onboarding_completed', False)
                verified = user.get('is_verified', False)
                
                print(f"Phone: {phone}")
                print(f"  Name: {name}")
                print(f"  Role: {role}")
                print(f"  City: {city}")
                print(f"  Sports: {sports}")
                print(f"  Onboarding Complete: {onboarding}")
                print(f"  Is Verified: {verified}")
                print()
                
                # Determine what should happen on login
                if onboarding:
                    print(f"  --> On login: Should go to DASHBOARD")
                elif not user.get('name'):
                    print(f"  --> On login: Should go to CREATE PROFILE (no name)")
                elif not user.get('role'):
                    print(f"  --> On login: Should go to CREATE PROFILE (no role)")
                else:
                    print(f"  --> On login: Should continue ONBOARDING")
                print("-" * 60)
        
        print("\n")
        
        # Close connection
        client.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(check_users())
