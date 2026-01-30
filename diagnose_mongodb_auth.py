#!/usr/bin/env python3
"""
Diagnose MongoDB authentication issues.
This script helps identify why authentication is failing.
"""

import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from urllib.parse import quote_plus

async def test_mongodb_connection():
    """Test MongoDB connection and provide detailed diagnostics"""
    
    print("=" * 70)
    print("MongoDB Authentication Diagnostics")
    print("=" * 70)
    
    # Get the URL from environment
    mongodb_url = os.getenv("MONGODB_URL", "")
    
    if not mongodb_url:
        print("\n❌ MONGODB_URL environment variable is NOT set")
        print("\nYou need to set it:")
        print("  export MONGODB_URL='mongodb+srv://user:pass@cluster.mongodb.net/db'")
        return False
    
    print(f"\n📝 MongoDB URL is set")
    
    # Mask the URL for display
    if "@" in mongodb_url:
        parts = mongodb_url.split("@")
        masked = f"{parts[0][:20]}...@{parts[1]}"
    else:
        masked = mongodb_url
    
    print(f"   (masked): {masked}")
    
    # Try to connect
    print(f"\n🔗 Attempting to connect to MongoDB...")
    
    try:
        # Create client with timeout
        client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
        
        # Try to ping
        print(f"   Sending ping command...")
        await client.admin.command('ping')
        
        print(f"\n✅ Connection successful!")
        print(f"✅ Authentication successful!")
        
        # Get server info
        server_info = await client.server_info()
        print(f"✅ MongoDB version: {server_info.get('version', 'unknown')}")
        
        client.close()
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"\n❌ Connection failed")
        print(f"   Error: {error_str}")
        
        # Analyze the error
        print(f"\n🔍 Error Analysis:")
        
        if "Authentication failed" in error_str or "bad auth" in error_str:
            print(f"   ❌ Authentication failed")
            print(f"   This means:")
            print(f"      - Username or password is incorrect")
            print(f"      - User doesn't have access to this database")
            print(f"      - User account is disabled")
            print(f"\n   Solutions:")
            print(f"      1. Verify username and password in MongoDB Atlas")
            print(f"      2. Check that the user has database access")
            print(f"      3. Reset the password if needed")
            print(f"      4. Ensure special characters are properly encoded")
            
        elif "connection refused" in error_str.lower():
            print(f"   ❌ Connection refused")
            print(f"   This means:")
            print(f"      - MongoDB server is not running")
            print(f"      - IP address is not whitelisted")
            print(f"      - Wrong host/port")
            print(f"\n   Solutions:")
            print(f"      1. For MongoDB Atlas: Add Render IP to IP Whitelist")
            print(f"      2. For local MongoDB: Ensure service is running")
            print(f"      3. Check the cluster URL is correct")
            
        elif "timeout" in error_str.lower():
            print(f"   ❌ Connection timeout")
            print(f"   This means:")
            print(f"      - Cannot reach MongoDB server")
            print(f"      - Network connectivity issue")
            print(f"      - IP is not whitelisted")
            print(f"\n   Solutions:")
            print(f"      1. For MongoDB Atlas: Whitelist 0.0.0.0/0 (or Render IP)")
            print(f"      2. Check network connectivity")
            print(f"      3. Verify the cluster URL")
            
        else:
            print(f"   ❌ Unknown error: {error_str}")
        
        return False

async def main():
    success = await test_mongodb_connection()
    print(f"\n" + "=" * 70)
    if success:
        print("✅ MongoDB is working correctly")
    else:
        print("❌ MongoDB connection failed - see above for solutions")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())
