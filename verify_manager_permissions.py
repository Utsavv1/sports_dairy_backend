"""
Verify and fix manager permissions in MongoDB
This script checks if managers have the correct permissions assigned
"""
import asyncio
import os
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")

async def verify_and_fix_permissions():
    """Verify all managers have correct permissions"""
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    try:
        await client.admin.command('ping')
        print("✅ Connected to MongoDB\n")
        
        print("🔍 Checking manager permissions...\n")
        
        # Get all active managers
        managers = await db.organizer_managers.find({"is_active": True}).to_list(None)
        
        if not managers:
            print("❌ No managers found in database")
            return
        
        print(f"Found {len(managers)} active managers\n")
        
        issues_found = 0
        fixed_count = 0
        
        for manager in managers:
            manager_id = str(manager["_id"])
            organizer_id = manager.get("organizer_id")
            manager_name = manager.get("name")
            permissions = manager.get("permissions", [])
            
            print(f"Manager: {manager_name}")
            print(f"  ID: {manager_id}")
            print(f"  Organizer ID: {organizer_id}")
            print(f"  Current Permissions: {permissions}")
            
            # Check if edit_tournament permission exists
            if "edit_tournament" not in permissions:
                print(f"  ⚠️  MISSING 'edit_tournament' permission!")
                issues_found += 1
                
                # Fix it
                permissions.append("edit_tournament")
                await db.organizer_managers.update_one(
                    {"_id": ObjectId(manager_id)},
                    {"$set": {
                        "permissions": permissions,
                        "updated_at": datetime.utcnow()
                    }}
                )
                print(f"  ✅ Fixed! Added 'edit_tournament' permission")
                fixed_count += 1
            else:
                print(f"  ✅ Has 'edit_tournament' permission")
            
            # Check if permissions list is empty
            if len(permissions) == 0:
                print(f"  ⚠️  EMPTY permissions list!")
                issues_found += 1
                
                # Fix with default permissions
                default_perms = ["create_tournament", "edit_tournament", "view_registrations"]
                await db.organizer_managers.update_one(
                    {"_id": ObjectId(manager_id)},
                    {"$set": {
                        "permissions": default_perms,
                        "updated_at": datetime.utcnow()
                    }}
                )
                print(f"  ✅ Fixed! Set default permissions: {default_perms}")
                fixed_count += 1
            
            print()
        
        # Summary
        print("="*60)
        print(f"✅ VERIFICATION COMPLETE")
        print("="*60)
        print(f"Total Managers: {len(managers)}")
        print(f"Issues Found: {issues_found}")
        print(f"Issues Fixed: {fixed_count}")
        print()
        
        if fixed_count > 0:
            print("🔄 Refreshing manager list...")
            managers = await db.organizer_managers.find({"is_active": True}).to_list(None)
            
            print("\n📋 Updated Manager Permissions:")
            for manager in managers:
                print(f"  • {manager.get('name')}: {manager.get('permissions', [])}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(verify_and_fix_permissions())
