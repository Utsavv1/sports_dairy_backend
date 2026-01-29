#!/usr/bin/env python3
"""
Utility script to verify and encode MongoDB URLs for RFC 3986 compliance.
Use this to check if your MongoDB URL needs encoding before deployment.
"""

import os
from urllib.parse import quote_plus

def encode_mongodb_url(url: str) -> str:
    """Encode MongoDB URL credentials according to RFC 3986"""
    if not url or "mongodb" not in url:
        return url
    
    if "%" in url and "@" in url:
        return url  # Already encoded
    
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
                return f"{prefix}{encoded_username}:{encoded_password}@{host}"
            else:
                encoded_username = quote_plus(credentials)
                return f"{prefix}{encoded_username}@{host}"
        except Exception as e:
            print(f"Error encoding URL: {e}")
            return url
    
    return url

def main():
    """Main function to verify MongoDB URL"""
    mongodb_url = os.getenv("MONGODB_URL", "")
    
    if not mongodb_url:
        print("❌ MONGODB_URL environment variable not set")
        print("\nExample MongoDB URLs:")
        print("  Local: mongodb://localhost:27017")
        print("  Atlas: mongodb+srv://username:password@cluster.mongodb.net/database")
        return
    
    print(f"📝 Original URL: {mongodb_url}")
    
    encoded_url = encode_mongodb_url(mongodb_url)
    
    if mongodb_url == encoded_url:
        print("✅ URL is valid (no encoding needed)")
    else:
        print(f"✅ Encoded URL: {encoded_url}")
        print("\n⚠️ Your MongoDB URL contains special characters that need encoding.")
        print("Use the encoded URL above in your MONGODB_URL environment variable.")
    
    # Check for common issues
    print("\n🔍 Checking for common issues:")
    
    if "@" not in mongodb_url:
        print("  ⚠️ No credentials found in URL (@ symbol missing)")
    else:
        print("  ✅ Credentials found in URL")
    
    if "mongodb+srv://" in mongodb_url:
        print("  ✅ Using MongoDB Atlas (mongodb+srv://)")
    elif "mongodb://" in mongodb_url:
        print("  ℹ️ Using standard MongoDB connection (mongodb://)")
    else:
        print("  ❌ Invalid MongoDB URL format")
    
    # Check for special characters that need encoding
    special_chars = ['@', ':', '/', '?', '#', '[', ']', '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', '=']
    if "@" in mongodb_url:
        credentials_part = mongodb_url.split("@")[0]
        found_special = [c for c in special_chars if c in credentials_part]
        if found_special:
            print(f"  ⚠️ Found special characters in credentials: {found_special}")
            print(f"     These will be encoded in the URL")
        else:
            print("  ✅ No special characters in credentials")

if __name__ == "__main__":
    main()
