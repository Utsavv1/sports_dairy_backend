import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_manager_user():
    # Get MongoDB URL from environment
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    # Check for the manager user by phone (try different formats)
    phones_to_check = [
        "+91 22222 22222",
        "+912222222222",
        "912222222222",
        "2222222222"
    ]
    
    print("=" * 60)
    print("CHECKING MANAGER USER IN DATABASE")
    print("=" * 60)
    
    for phone in phones_to_check:
        print(f"\nSearching for phone: {phone}")
        user = await db.users.find_one({"phone": phone})
        
        if user:
            print(f"[SUCCESS] FOUND USER!")
            print(f"  - ID: {user['_id']}")
            print(f"  - Name: {user.get('name', 'N/A')}")
            print(f"  - Phone: {user.get('phone')}")
            print(f"  - Email: {user.get('email', 'N/A')}")
            print(f"  - Role: {user.get('role', 'N/A')}")
            print(f"  - City: {user.get('city', 'N/A')}")
            print(f"  - Age: {user.get('age', 'N/A')}")
            print(f"  - Gender: {user.get('gender', 'N/A')}")
            print(f"  - is_verified: {user.get('is_verified', False)}")
            print(f"  - is_active: {user.get('is_active', False)}")
            print(f"  - onboarding_completed: {user.get('onboarding_completed', False)}")
            print(f"  - sports_interests: {user.get('sports_interests', [])}")
            
            # Check if this user is a manager
            manager = await db.organizer_managers.find_one({"phone": phone})
            if manager:
                print(f"\n[MANAGER] MANAGER RECORD FOUND:")
                print(f"  - Manager ID: {manager['_id']}")
                print(f"  - Organizer ID: {manager.get('organizer_id')}")
                print(f"  - Manager User ID: {manager.get('manager_user_id')}")
                print(f"  - Permissions: {manager.get('permissions', [])}")
                print(f"  - Is Active: {manager.get('is_active', False)}")
                print(f"  - Is Verified: {manager.get('is_verified', False)}")
            
            break
    else:
        print("\n[ERROR] NO USER FOUND with any of these phone numbers!")
        print("\nLet's check all users in organizer_managers collection:")
        managers = await db.organizer_managers.find({}).to_list(length=100)
        print(f"\nTotal managers: {len(managers)}")
        for idx, mgr in enumerate(managers, 1):
            print(f"\n{idx}. Manager:")
            print(f"   Phone: {mgr.get('phone')}")
            print(f"   Name: {mgr.get('name')}")
            print(f"   Manager User ID: {mgr.get('manager_user_id')}")
    
    print("\n" + "=" * 60)
    client.close()

if __name__ == "__main__":
    asyncio.run(check_manager_user())

