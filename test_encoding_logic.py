#!/usr/bin/env python3
"""Test the MongoDB URL encoding logic"""

from urllib.parse import quote_plus

def encode_mongodb_url(url: str) -> str:
    """Encode MongoDB URL credentials according to RFC 3986."""
    if not url:
        return url
    
    if "%" in url:
        return url
    
    if "@" not in url:
        return url
    
    try:
        if url.startswith("mongodb+srv://"):
            protocol = "mongodb+srv://"
            rest = url[14:]
        elif url.startswith("mongodb://"):
            protocol = "mongodb://"
            rest = url[10:]
        else:
            return url
        
        # CRITICAL FIX: Use rfind to find the LAST @ (not the first)
        last_at_index = rest.rfind("@")
        if last_at_index == -1:
            return url
        
        credentials = rest[:last_at_index]
        host = rest[last_at_index + 1:]
        
        colon_index = credentials.find(":")
        if colon_index == -1:
            username = credentials
            password = ""
        else:
            username = credentials[:colon_index]
            password = credentials[colon_index + 1:]
        
        encoded_username = quote_plus(username)
        encoded_password = quote_plus(password) if password else ""
        
        if password:
            encoded_credentials = f"{encoded_username}:{encoded_password}"
        else:
            encoded_credentials = encoded_username
        
        encoded_url = f"{protocol}{encoded_credentials}@{host}"
        return encoded_url
        
    except Exception as e:
        print(f"ERROR: {e}")
        return url

def test_encoding():
    # Test case 1: Email username with special password
    url1 = "mongodb+srv://user@company.com:P@ssw0rd@cluster.mongodb.net/database"
    encoded1 = encode_mongodb_url(url1)
    
    print("Test 1: Email username with special password")
    print(f"  Original:  {url1}")
    print(f"  Encoded:   {encoded1}")
    print(f"  Expected:  mongodb+srv://user%40company.com:P%40ssw0rd@cluster.mongodb.net/database")
    print(f"  Correct?   {encoded1 == 'mongodb+srv://user%40company.com:P%40ssw0rd@cluster.mongodb.net/database'}")
    print()
    
    # Test case 2: Simple credentials
    url2 = "mongodb+srv://admin:password123@cluster.mongodb.net/database"
    encoded2 = encode_mongodb_url(url2)
    
    print("Test 2: Simple credentials (no special chars)")
    print(f"  Original:  {url2}")
    print(f"  Encoded:   {encoded2}")
    print(f"  Same?      {url2 == encoded2}")
    print()
    
    # Test case 3: Complex password
    url3 = "mongodb+srv://user:P@ss!w0rd$@cluster.mongodb.net/database"
    encoded3 = encode_mongodb_url(url3)
    
    print("Test 3: Complex password with multiple special chars")
    print(f"  Original:  {url3}")
    print(f"  Encoded:   {encoded3}")
    print(f"  Expected:  mongodb+srv://user:P%40ss%21w0rd%24@cluster.mongodb.net/database")
    print(f"  Correct?   {encoded3 == 'mongodb+srv://user:P%40ss%21w0rd%24@cluster.mongodb.net/database'}")
    print()

if __name__ == "__main__":
    test_encoding()

