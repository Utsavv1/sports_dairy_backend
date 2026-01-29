#!/usr/bin/env python3
"""
Quick test script to verify MongoDB connection.
Run this to test if your MongoDB URL is correctly configured.
"""

import asyncio
import os
import sys
from urllib.parse import quote_plus

async def test_connection():
    """Test MongoDB connection"""
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from app.core.database import encode_mongodb_url, MONGODB_URL, DATABASE_NAME
        
        print("=" * 60)
        print("MongoDB Connection Test")
        print("=" * 60)
        
        # Show original URL (masked for security)
        if MONGODB_URL:
            masked_url = MONGODB_URL.replace(MONGODB_URL.split("@")[0], "[CREDENTIALS]") if "@" in MONGODB_URL else MONGODB_URL
            print(f"\n📝 Original URL: {masked_url}")
        else:
            print("\n❌ MONGODB_URL environment variable not set")
            return False
        
        # Encode URL
        encoded_url = encode_mongodb_url(MONGODB_URL)
        
        if MONGODB_URL != encoded_url:
            print(f"✅ URL encoding applied (special characters detected)")
        else:
            print(f"ℹ️ URL has no special characters or already encoded")
        
        # Try to connect
        print(f"\n🔗 Attempting to connect to MongoDB...")
        client = AsyncIOMotorClient(encoded_url, serverSelectionTimeoutMS=5000)
        
        # Test connection with ping
        await client.admin.command('ping')
        print(f"✅ Successfully connected to MongoDB")
        
        # Get database info
        db = client[DATABASE_NAME]
        print(f"✅ Using database: {DATABASE_NAME}")
        
        # List collections
        collections = await db.list_collection_names()
        print(f"✅ Found {len(collections)} collections")
        if collections:
            print(f"   Collections: {', '.join(collections[:5])}")
            if len(collections) > 5:
                print(f"   ... and {len(collections) - 5} more")
        
        # Close connection
        client.close()
        print(f"\n✅ Connection test passed!")
        print("=" * 60)
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure you're running this from the backend directory")
        print("   and all dependencies are installed")
        return False
    except Exception as e:
        print(f"\n❌ Connection failed: {e}")
        print("\n🔍 Troubleshooting:")
        print("   1. Check that MONGODB_URL environment variable is set")
        print("   2. Verify credentials are correct")
        print("   3. Ensure special characters are properly encoded")
        print("   4. Check that MongoDB cluster allows your IP")
        print("   5. Run: python backend/verify_mongodb_url.py")
        print("=" * 60)
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(test_connection())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)
