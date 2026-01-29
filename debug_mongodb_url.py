#!/usr/bin/env python3
"""
Debug script to show exactly what MongoDB URL is being used.
Run this to verify the URL encoding is working correctly.
"""

import os
from urllib.parse import quote_plus

def encode_mongodb_url(url: str) -> str:
    """Encode MongoDB URL credentials"""
    if not url or "mongodb" not in url:
        return url
    
    if "%" in url and "@" in url:
        return url
    
    if "@" in url:
        try:
            if "mongodb+srv://" in url:
                prefix = "mongodb+srv://"
                rest = url.replace(prefix, "")
            elif "mongodb://" in url:
                prefix = "mongodb://"
                rest = url.replace(prefix, "")
            else:
                return url
            
            credentials, host = rest.split("@", 1)
            
            if ":" in credentials:
                username, password = credentials.split(":", 1)
                encoded_username = quote_plus(username)
                encoded_password = quote_plus(password)
                encoded_url = f"{prefix}{encoded_username}:{encoded_password}@{host}"
                return encoded_url
            else:
                encoded_username = quote_plus(credentials)
                return f"{prefix}{encoded_username}@{host}"
        except Exception as e:
            print(f"Error: {e}")
            return url
    
    return url

def mask_url(url: str) -> str:
    """Mask credentials in URL for display"""
    if "@" not in url:
        return url
    
    prefix_part = url.split("@")[0]
    host_part = url.split("@")[1]
    
    # Replace credentials with masked version
    if "://" in prefix_part:
        protocol = prefix_part.split("://")[0] + "://"
        return f"{protocol}[CREDENTIALS]@{host_part}"
    
    return url

def main():
    print("=" * 70)
    print("MongoDB URL Debug Information")
    print("=" * 70)
    
    # Get raw URL from environment
    raw_url = os.getenv("MONGODB_URL", "")
    
    if not raw_url:
        print("\n❌ MONGODB_URL environment variable is NOT set")
        print("\nYou need to set it before running the application:")
        print("  export MONGODB_URL='mongodb+srv://user:pass@cluster.mongodb.net/db'")
        return
    
    print(f"\n📝 Raw URL from environment:")
    print(f"   {mask_url(raw_url)}")
    
    # Encode the URL
    encoded_url = encode_mongodb_url(raw_url)
    
    print(f"\n🔄 After encoding:")
    print(f"   {mask_url(encoded_url)}")
    
    # Check if encoding happened
    if raw_url == encoded_url:
        print(f"\n✅ No encoding needed (no special characters in credentials)")
    else:
        print(f"\n✅ Encoding applied (special characters detected)")
    
    # Analyze the URL
    print(f"\n🔍 URL Analysis:")
    
    if "mongodb+srv://" in raw_url:
        print(f"   ✅ Protocol: MongoDB Atlas (mongodb+srv://)")
    elif "mongodb://" in raw_url:
        print(f"   ✅ Protocol: Standard MongoDB (mongodb://)")
    else:
        print(f"   ❌ Unknown protocol")
    
    if "@" in raw_url:
        print(f"   ✅ Credentials present")
        
        # Extract and analyze credentials
        cred_part = raw_url.split("@")[0]
        if "://" in cred_part:
            cred_part = cred_part.split("://")[1]
        
        if ":" in cred_part:
            username, password = cred_part.split(":", 1)
            print(f"   ✅ Username: {username}")
            print(f"   ✅ Password: {'*' * len(password)}")
            
            # Check for special characters
            special_chars = set()
            for char in username + password:
                if not char.isalnum() and char not in ['-', '_', '.']:
                    special_chars.add(char)
            
            if special_chars:
                print(f"   ⚠️ Special characters found: {sorted(special_chars)}")
                print(f"      These will be encoded in the URL")
            else:
                print(f"   ✅ No special characters in credentials")
    else:
        print(f"   ℹ️ No credentials (local MongoDB)")
    
    # Show what Python will use
    print(f"\n🐍 Python will use this URL:")
    print(f"   {mask_url(encoded_url)}")
    
    print(f"\n" + "=" * 70)
    print("✅ Debug complete")
    print("=" * 70)

if __name__ == "__main__":
    main()
