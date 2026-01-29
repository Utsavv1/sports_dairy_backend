#!/usr/bin/env python3
"""
Simple script to encode MongoDB credentials for RFC 3986 compliance.
Use this if you want to pre-encode your MongoDB URL before setting it in Render.
"""

from urllib.parse import quote_plus
import sys

def encode_url(url: str) -> str:
    """Encode MongoDB URL credentials"""
    if not url or "@" not in url:
        return url
    
    # Determine protocol
    if url.startswith("mongodb+srv://"):
        protocol = "mongodb+srv://"
        rest = url[14:]
    elif url.startswith("mongodb://"):
        protocol = "mongodb://"
        rest = url[10:]
    else:
        return url
    
    # Split credentials from host
    at_index = rest.find("@")
    if at_index == -1:
        return url
    
    credentials = rest[:at_index]
    host = rest[at_index + 1:]
    
    # Split username and password
    colon_index = credentials.find(":")
    if colon_index == -1:
        username = credentials
        password = ""
    else:
        username = credentials[:colon_index]
        password = credentials[colon_index + 1:]
    
    # Encode
    encoded_username = quote_plus(username)
    encoded_password = quote_plus(password) if password else ""
    
    # Reconstruct
    if password:
        encoded_credentials = f"{encoded_username}:{encoded_password}"
    else:
        encoded_credentials = encoded_username
    
    return f"{protocol}{encoded_credentials}@{host}"

def main():
    print("=" * 70)
    print("MongoDB URL Encoder")
    print("=" * 70)
    
    if len(sys.argv) > 1:
        # URL provided as argument
        url = sys.argv[1]
    else:
        # Prompt for URL
        print("\nEnter your MongoDB connection URL:")
        print("Example: mongodb+srv://user@company.com:P@ssw0rd@cluster.mongodb.net/db")
        print()
        url = input("MongoDB URL: ").strip()
    
    if not url:
        print("❌ No URL provided")
        return
    
    print(f"\n📝 Original URL:")
    print(f"   {url}")
    
    encoded = encode_url(url)
    
    print(f"\n✅ Encoded URL:")
    print(f"   {encoded}")
    
    if url == encoded:
        print(f"\n✅ No encoding needed (no special characters)")
    else:
        print(f"\n✅ Encoding applied!")
        print(f"\n📋 Copy the encoded URL above and set it as MONGODB_URL in Render")
    
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
