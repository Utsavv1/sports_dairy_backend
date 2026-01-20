import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def check_manager_and_tournament():
    """
    Debug script to check manager permissions and tournament ownership
    """
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")
    
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    print("=" * 80)
    print("DEBUGGING MANAGER EDIT PERMISSION")
    print("=" * 80)
    
    # Get manager phone (change this to your manager's phone)
    manager_phone = input("\nEnter manager's phone number (e.g., +912222222222): ").strip()
    
    # Step 1: Find manager's user account
    print("\n" + "=" * 80)
    print("STEP 1: Checking Manager's User Account")
    print("=" * 80)
    
    user = await db.users.find_one({"phone": manager_phone})
    if not user:
        print(f"❌ ERROR: User with phone {manager_phone} not found!")
        client.close()
        return
    
    user_id = str(user["_id"])
    print(f"✓ Found user: {user.get('name')}")
    print(f"  - User ID: {user_id}")
    print(f"  - Role: {user.get('role')}")
    print(f"  - Onboarding Complete: {user.get('onboarding_completed')}")
    print(f"  - Is Verified: {user.get('is_verified')}")
    
    if user.get('role') != 'organizer':
        print(f"\n⚠️  WARNING: Manager role is '{user.get('role')}' but should be 'organizer'")
        print("   Run this command to fix:")
        print(f"   db.users.update_one({{'_id': ObjectId('{user_id}')}}, {{'$set': {{'role': 'organizer'}}}}))")
    
    # Step 2: Find manager record
    print("\n" + "=" * 80)
    print("STEP 2: Checking Manager Record in organizer_managers")
    print("=" * 80)
    
    manager_record = await db.organizer_managers.find_one({
        "manager_user_id": user_id,
        "is_active": True
    })
    
    if not manager_record:
        print(f"❌ ERROR: No active manager record found for user {user_id}")
        print("\nPossible issues:")
        print("1. Manager was not properly linked when created")
        print("2. Manager is inactive (is_active: false)")
        client.close()
        return
    
    organizer_id = str(manager_record["organizer_id"])
    print(f"✓ Found manager record")
    print(f"  - Manager ID: {manager_record['_id']}")
    print(f"  - Works for Organizer ID: {organizer_id}")
    print(f"  - Organizer Name: {manager_record.get('organizer_name')}")
    print(f"  - Permissions: {manager_record.get('permissions', [])}")
    print(f"  - Is Active: {manager_record.get('is_active')}")
    
    has_edit_permission = 'edit_tournament' in manager_record.get('permissions', [])
    if has_edit_permission:
        print(f"  ✓ Has 'edit_tournament' permission")
    else:
        print(f"  ❌ MISSING 'edit_tournament' permission!")
        print(f"     Current permissions: {manager_record.get('permissions', [])}")
    
    # Step 3: Find organizer's user account
    print("\n" + "=" * 80)
    print("STEP 3: Checking Organizer's Account")
    print("=" * 80)
    
    organizer = await db.users.find_one({"_id": ObjectId(organizer_id)})
    if not organizer:
        print(f"❌ ERROR: Organizer with ID {organizer_id} not found!")
        client.close()
        return
    
    print(f"✓ Found organizer: {organizer.get('name')}")
    print(f"  - Organizer ID: {organizer_id}")
    print(f"  - Role: {organizer.get('role')}")
    
    # Step 4: Find tournaments created by this organizer
    print("\n" + "=" * 80)
    print("STEP 4: Checking Tournaments Created by This Organizer")
    print("=" * 80)
    
    tournaments_cursor = db.tournaments.find({
        "organizer_id": organizer_id,
        "is_active": True
    })
    tournaments = await tournaments_cursor.to_list(length=None)
    
    print(f"\nFound {len(tournaments)} tournament(s) created by organizer:")
    
    if len(tournaments) == 0:
        print("  No tournaments found. Create a tournament first.")
    else:
        for i, tournament in enumerate(tournaments, 1):
            print(f"\n  Tournament {i}:")
            print(f"    - ID: {tournament['_id']}")
            print(f"    - Name: {tournament.get('name')}")
            print(f"    - Organizer ID: {tournament.get('organizer_id')}")
            print(f"    - Created By: {tournament.get('created_by')}")
            print(f"    - Created By Manager: {tournament.get('created_by_manager', False)}")
    
    # Step 5: Test the permission check endpoint
    print("\n" + "=" * 80)
    print("STEP 5: Testing /api/organizer-team/check-permission Response")
    print("=" * 80)
    
    # Simulate what the endpoint returns
    if user.get('role') == 'organizer':
        if manager_record:
            expected_response = {
                "is_organizer": False,
                "is_manager": True,
                "organizer_id": organizer_id,
                "organizer_name": manager_record.get("organizer_name"),
                "permissions": manager_record.get("permissions", [])
            }
        else:
            expected_response = {
                "is_organizer": True,
                "is_manager": False,
                "organizer_id": user_id,
                "permissions": ["create_tournament", "edit_tournament", "view_registrations", "manage_team"]
            }
        
        print("Expected API response:")
        import json
        print(json.dumps(expected_response, indent=2))
    
    # Step 6: Summary and recommendations
    print("\n" + "=" * 80)
    print("SUMMARY & RECOMMENDATIONS")
    print("=" * 80)
    
    issues = []
    fixes = []
    
    if user.get('role') != 'organizer':
        issues.append(f"Manager role is '{user.get('role')}' instead of 'organizer'")
        fixes.append(f"Fix role: db.users.update_one({{'_id': ObjectId('{user_id}')}}, {{'$set': {{'role': 'organizer'}}}}))")
    
    if not has_edit_permission:
        issues.append("Manager doesn't have 'edit_tournament' permission")
        fixes.append(f"Add permission: db.organizer_managers.update_one({{'_id': ObjectId('{manager_record['_id']}')}}, {{'$addToSet': {{'permissions': 'edit_tournament'}}}}))")
    
    if len(tournaments) == 0:
        issues.append("No tournaments created by this organizer yet")
        fixes.append("Create a tournament as the main organizer first")
    
    if len(issues) == 0:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nThe manager should be able to see the edit button on tournaments.")
        print("\nIf the edit button still doesn't show:")
        print("1. Make sure manager is logged in (not organizer)")
        print("2. Clear browser cache and localStorage")
        print("3. Check browser console for errors")
        print("4. Verify the tournament page is loading manager info")
    else:
        print(f"\n❌ Found {len(issues)} issue(s):")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        
        print("\n🔧 Recommended fixes:")
        for i, fix in enumerate(fixes, 1):
            print(f"  {i}. {fix}")
    
    # Step 7: Quick fix option
    if len(fixes) > 0:
        print("\n" + "=" * 80)
        fix_now = input("\nDo you want to apply these fixes now? (yes/no): ").strip().lower()
        
        if fix_now == 'yes':
            print("\nApplying fixes...")
            
            if user.get('role') != 'organizer':
                await db.users.update_one(
                    {"_id": user["_id"]},
                    {"$set": {"role": "organizer"}}
                )
                print("✓ Fixed user role to 'organizer'")
            
            if not has_edit_permission and manager_record:
                await db.organizer_managers.update_one(
                    {"_id": manager_record["_id"]},
                    {"$addToSet": {"permissions": "edit_tournament"}}
                )
                print("✓ Added 'edit_tournament' permission")
            
            print("\n✅ Fixes applied successfully!")
            print("\nNext steps:")
            print("1. Logout from the application")
            print("2. Login again as manager")
            print("3. Navigate to a tournament created by your organizer")
            print("4. Edit button should now appear")
    
    print("\n" + "=" * 80)
    client.close()

if __name__ == "__main__":
    asyncio.run(check_manager_and_tournament())

