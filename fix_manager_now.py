import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

async def fix_manager():
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print("\n" + "=" * 80)
    print("QUICK FIX: Manager Edit Permission")
    print("=" * 80)
    
    # Get manager phone
    manager_phone = "+912222222222"  # Default from screenshot
    custom_phone = input(f"\nManager phone number (press Enter for {manager_phone}): ").strip()
    if custom_phone:
        manager_phone = custom_phone
    
    print(f"\nFixing manager: {manager_phone}")
    print("-" * 80)
    
    # Step 1: Find and fix user account
    user = await db.users.find_one({"phone": manager_phone})
    if not user:
        print(f"❌ ERROR: User {manager_phone} not found!")
        print("   Create the manager first in the 'My Team' page")
        client.close()
        return
    
    user_id = str(user["_id"])
    print(f"✓ Found user: {user.get('name')}")
    
    # Fix role if wrong
    if user.get('role') != 'organizer':
        await db.users.update_one(
            {"_id": user["_id"]},
            {"$set": {"role": "organizer"}}
        )
        print(f"  ✓ Fixed role: {user.get('role')} → organizer")
    else:
        print(f"  ✓ Role is correct: organizer")
    
    # Step 2: Find and fix manager record
    manager_record = await db.organizer_managers.find_one({
        "manager_user_id": user_id
    })
    
    if not manager_record:
        print(f"❌ ERROR: No manager record found!")
        print("   User exists but is not set up as a manager")
        print("   Add them as a manager in 'My Team' page")
        client.close()
        return
    
    print(f"✓ Found manager record")
    print(f"  - Organizer ID: {manager_record.get('organizer_id')}")
    print(f"  - Current Permissions: {manager_record.get('permissions', [])}")
    
    # Fix manager record
    updates = {}
    
    if not manager_record.get('is_active'):
        updates['is_active'] = True
        print(f"  ✓ Activating manager")
    
    permissions = manager_record.get('permissions', [])
    if 'edit_tournament' not in permissions:
        permissions.append('edit_tournament')
        updates['permissions'] = permissions
        print(f"  ✓ Adding edit_tournament permission")
    
    if updates:
        await db.organizer_managers.update_one(
            {"_id": manager_record["_id"]},
            {"$set": updates}
        )
        print(f"✓ Manager record updated")
    else:
        print(f"✓ Manager record already correct")
    
    # Step 3: Check tournaments
    organizer_id = manager_record.get('organizer_id')
    tournaments = await db.tournaments.find({
        "organizer_id": organizer_id,
        "is_active": True
    }).to_list(length=None)
    
    print(f"\n✓ Found {len(tournaments)} tournament(s) by this organizer:")
    for i, t in enumerate(tournaments, 1):
        print(f"  {i}. {t.get('name')} (ID: {t['_id']})")
    
    print("\n" + "=" * 80)
    print("✅ ALL FIXES APPLIED!")
    print("=" * 80)
    print("\nNEXT STEPS:")
    print("1. Go to browser and LOGOUT")
    print("2. Clear cache: Ctrl+Shift+Delete → Cached images")
    print("3. Clear localStorage: F12 → Console → type: localStorage.clear()")
    print("4. Refresh page (F5)")
    print("5. LOGIN as manager with phone:", manager_phone)
    print("6. Go to tournament page")
    print("7. Edit button should now appear!")
    print("\nIf still not working, check browser console (F12) for logs")
    print("=" * 80 + "\n")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(fix_manager())

