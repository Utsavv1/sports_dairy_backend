#!/usr/bin/env python3
"""
Fix script for manager permissions issues
This script can identify and fix common permission problems
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "sports_diary")

async def fix_manager_permissions():
    """Fix manager permissions"""
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    print("=" * 80)
    print("MANAGER PERMISSIONS FIX SCRIPT")
    print("=" * 80)
    
    try:
        # Find all managers without edit_tournament permission
        managers_without_edit = await db.organizer_managers.find({
            "permissions": {"$nin": ["edit_tournament"]},
            "is_active": True
        }).to_list(None)
        
        print(f"\n✓ Found {len(managers_without_edit)} managers without edit_tournament permission")
        
        if managers_without_edit:
            print("\nManagers to fix:")
            for mgr in managers_without_edit:
                mgr_id = str(mgr["_id"])
                mgr_name = mgr.get("name", "Unknown")
                mgr_phone = mgr.get("phone", "Unknown")
                current_perms = mgr.get("permissions", [])
                
                print(f"\n  Manager: {mgr_name} ({mgr_phone})")
                print(f"    ID: {mgr_id}")
                print(f"    Current permissions: {current_perms}")
                
                # Add edit_tournament permission
                result = await db.organizer_managers.update_one(
                    {"_id": ObjectId(mgr_id)},
                    {"$addToSet": {"permissions": "edit_tournament"}}
                )
                
                if result.modified_count > 0:
                    print(f"    ✓ Added edit_tournament permission")
                else:
                    print(f"    ✗ Failed to add permission")
        
        # Find all inactive managers
        inactive_managers = await db.organizer_managers.find({
            "is_active": False
        }).to_list(None)
        
        print(f"\n✓ Found {len(inactive_managers)} inactive managers")
        
        if inactive_managers:
            print("\nInactive managers:")
            for mgr in inactive_managers:
                mgr_id = str(mgr["_id"])
                mgr_name = mgr.get("name", "Unknown")
                mgr_phone = mgr.get("phone", "Unknown")
                
                print(f"\n  Manager: {mgr_name} ({mgr_phone})")
                print(f"    ID: {mgr_id}")
                print(f"    Status: Inactive")
                
                # Ask if user wants to reactivate
                response = input("    Reactivate? (y/n): ").strip().lower()
                
                if response == 'y':
                    result = await db.organizer_managers.update_one(
                        {"_id": ObjectId(mgr_id)},
                        {"$set": {"is_active": True}}
                    )
                    
                    if result.modified_count > 0:
                        print(f"    ✓ Reactivated manager")
                    else:
                        print(f"    ✗ Failed to reactivate")
        
        # Find managers with mismatched organizer_id
        print(f"\n✓ Checking for ID type mismatches...")
        
        all_managers = await db.organizer_managers.find({
            "is_active": True
        }).to_list(None)
        
        mismatched = 0
        for mgr in all_managers:
            org_id = mgr.get("organizer_id")
            
            # Check if organizer exists
            if isinstance(org_id, ObjectId):
                organizer = await db.users.find_one({"_id": org_id})
            else:
                try:
                    organizer = await db.users.find_one({"_id": ObjectId(str(org_id))})
                except:
                    organizer = None
            
            if not organizer:
                mismatched += 1
                mgr_name = mgr.get("name", "Unknown")
                mgr_phone = mgr.get("phone", "Unknown")
                
                print(f"\n  ✗ Manager {mgr_name} ({mgr_phone}) has invalid organizer_id: {org_id}")
        
        if mismatched == 0:
            print("  ✓ All manager organizer_ids are valid")
        
        print(f"\n{'=' * 80}")
        print("FIX COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(fix_manager_permissions())
