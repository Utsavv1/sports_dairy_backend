import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_login_response():
    # Get MongoDB URL from environment
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    
    phone = "+91 22222 22222"
    
    print("=" * 60)
    print("SIMULATING LOGIN RESPONSE")
    print("=" * 60)
    
    # Find the user (same as OTP verification does)
    user_data = await db.users.find_one({"phone": phone})
    
    if not user_data:
        print(f"[ERROR] No user found with phone: {phone}")
        client.close()
        return
    
    print(f"\n[DATABASE] Raw user data from MongoDB:")
    print(f"  - _id: {user_data['_id']}")
    print(f"  - phone: {user_data.get('phone')}")
    print(f"  - name: {user_data.get('name')}")
    print(f"  - role: {user_data.get('role')}")
    print(f"  - onboarding_completed: {user_data.get('onboarding_completed')}")
    print(f"  - is_verified: {user_data.get('is_verified')}")
    
    # Simulate what auth endpoint returns
    is_new_user = False  # User already exists
    
    response_user = {
        "id": str(user_data["_id"]),
        "phone": user_data.get("phone"),
        "name": user_data.get("name"),
        "email": user_data.get("email"),
        "age": user_data.get("age"),
        "gender": user_data.get("gender"),
        "role": user_data.get("role"),
        "professional_type": user_data.get("professional_type"),
        "city": user_data.get("city"),
        "state": user_data.get("state"),
        "bio": user_data.get("bio"),
        "avatar": user_data.get("avatar"),
        "sports_interests": user_data.get("sports_interests", []),
        "onboarding_completed": user_data.get("onboarding_completed", False),
        "is_new_user": is_new_user,
        "is_verified": user_data.get("is_verified", False)
    }
    
    print(f"\n[API RESPONSE] What would be sent to frontend:")
    print(f"  - id: {response_user['id']}")
    print(f"  - name: {response_user['name']}")
    print(f"  - role: {response_user['role']}")
    print(f"  - city: {response_user['city']}")
    print(f"  - onboarding_completed: {response_user['onboarding_completed']}")
    print(f"  - is_new_user: {response_user['is_new_user']}")
    print(f"  - is_verified: {response_user['is_verified']}")
    
    print(f"\n[ROUTING LOGIC] Frontend should:")
    if response_user['onboarding_completed']:
        print(f"  -> Redirect to DASHBOARD (onboarding_completed is True)")
    elif response_user['is_new_user'] or not response_user['name'] or not response_user['role']:
        print(f"  -> Redirect to CREATE PROFILE (new user or missing profile)")
    elif not response_user['city']:
        print(f"  -> Redirect to CITY SELECTION (missing city)")
    else:
        print(f"  -> Redirect to DASHBOARD (has all fields)")
    
    print("\n" + "=" * 60)
    client.close()

if __name__ == "__main__":
    asyncio.run(test_login_response())

