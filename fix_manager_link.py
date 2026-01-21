import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

async def fix_manager_link():
    # Get MongoDB URL from environment
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    phone = "+91 22222 22222"
    
    print("=" * 60)
    print("FIXING MANAGER-USER LINK")
    print("=" * 60)
    
    # Find the user
    user = await db.users.find_one({"phone": phone})
    if not user:
        print(f"[ERROR] No user found with phone: {phone}")
        client.close()
        return
    
    user_id = str(user["_id"])
    print(f"\n[FOUND] User: {user.get('name')}")
    print(f"  - User ID: {user_id}")
    print(f"  - onboarding_completed: {user.get('onboarding_completed')}")
    
    # Find the manager record
    manager = await db.organizer_managers.find_one({"phone": phone})
    if not manager:
        print(f"\n[ERROR] No manager record found with phone: {phone}")
        client.close()
        return
    
    print(f"\n[FOUND] Manager Record")
    print(f"  - Manager ID: {manager['_id']}")
    print(f"  - Current manager_user_id: {manager.get('manager_user_id')}")
    print(f"  - Current is_active: {manager.get('is_active')}")
    print(f"  - Current is_verified: {manager.get('is_verified')}")
    
    # Update the manager record
    print(f"\n[UPDATING] Linking manager to user...")
    result = await db.organizer_managers.update_one(
        {"_id": manager["_id"]},
        {
            "$set": {
                "manager_user_id": user_id,
                "is_active": True,
                "is_verified": True,
                "updated_at": datetime.utcnow()
            }
        }
    )
    
    if result.modified_count > 0:
        print(f"[SUCCESS] Manager record updated!")
        
        # Verify the update
        updated_manager = await db.organizer_managers.find_one({"_id": manager["_id"]})
        print(f"\n[VERIFIED] Updated Manager Record:")
        print(f"  - manager_user_id: {updated_manager.get('manager_user_id')}")
        print(f"  - is_active: {updated_manager.get('is_active')}")
        print(f"  - is_verified: {updated_manager.get('is_verified')}")
        print(f"\n[SUCCESS] Manager can now login and access dashboard!")
    else:
        print(f"[ERROR] Failed to update manager record")
    
    print("\n" + "=" * 60)
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_manager_link())

