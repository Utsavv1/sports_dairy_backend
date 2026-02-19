#!/usr/bin/env python3
"""
Verification script to check manager permissions in MongoDB
This script helps debug why team members can't edit tournaments
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "sports_diary")

async def verify_manager_permissions():
    """Verify manager permissions setup"""
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    print("=" * 80)
    print("MANAGER PERMISSIONS VERIFICATION SCRIPT")
    print("=" * 80)
    
    try:
        # Get all organizers
        organizers = await db.users.find({"role": "organizer"}).to_list(None)
        print(f"\n✓ Found {len(organizers)} organizers")
        
        for org in organizers:
            org_id = str(org["_id"])
            org_name = org.get("name", "Unknown")
            org_phone = org.get("phone", "Unknown")
            
            print(f"\n{'─' * 80}")
            print(f"Organizer: {org_name} ({org_phone})")
            print(f"ID: {org_id}")
            
            # Get managers for this organizer
            managers = await db.organizer_managers.find({
                "organizer_id": org_id,
                "is_active": True
            }).to_list(None)
            
            print(f"  Managers: {len(managers)}")
            
            for mgr in managers:
                mgr_id = str(mgr["_id"])
                mgr_user_id = mgr.get("manager_user_id")
                mgr_name = mgr.get("name", "Unknown")
                mgr_phone = mgr.get("phone", "Unknown")
                permissions = mgr.get("permissions", [])
                
                print(f"\n  Manager: {mgr_name} ({mgr_phone})")
                print(f"    Manager ID: {mgr_id}")
                print(f"    User ID: {mgr_user_id}")
                print(f"    Organizer ID: {mgr.get('organizer_id')}")
                print(f"    Permissions: {permissions}")
                print(f"    Is Active: {mgr.get('is_active')}")
                print(f"    Is Verified: {mgr.get('is_verified')}")
                
                # Check if edit_tournament permission exists
                if "edit_tournament" in permissions:
                    print(f"    ✓ Has edit_tournament permission")
                else:
                    print(f"    ✗ MISSING edit_tournament permission")
                
                # Get tournaments for this organizer
                tournaments = await db.tournaments.find({
                    "organizer_id": org_id,
                    "is_active": True
                }).to_list(None)
                
                print(f"    Tournaments: {len(tournaments)}")
                
                for tourn in tournaments[:3]:  # Show first 3
                    tourn_id = str(tourn["_id"])
                    tourn_name = tourn.get("name", "Unknown")
                    print(f"      - {tourn_name} ({tourn_id})")
            
            # Get tournaments for this organizer
            tournaments = await db.tournaments.find({
                "organizer_id": org_id,
                "is_active": True
            }).to_list(None)
            
            print(f"\n  Total Tournaments: {len(tournaments)}")
        
        print(f"\n{'=' * 80}")
        print("VERIFICATION COMPLETE")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(verify_manager_permissions())
