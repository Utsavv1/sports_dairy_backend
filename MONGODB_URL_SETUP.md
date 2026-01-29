# MongoDB URL Setup Guide

## Problem: "Username and password must be escaped according to RFC 3986"

This error occurs when your MongoDB connection URL contains special characters in the username or password that haven't been URL-encoded.

## Solution

### Step 1: Identify Your MongoDB URL

Your MongoDB URL should look like one of these:

**Local MongoDB:**
```
mongodb://localhost:27017
```

**MongoDB Atlas (Cloud):**
```
mongodb+srv://username:password@cluster.mongodb.net/database
```

### Step 2: Check for Special Characters

Special characters that need encoding include:
- `@` → `%40`
- `:` → `%3A`
- `/` → `%2F`
- `?` → `%3F`
- `#` → `%23`
- `[` → `%5B`
- `]` → `%5D`
- `!` → `%21`
- `$` → `%24`
- `&` → `%26`
- `'` → `%27`
- `(` → `%28`
- `)` → `%29`
- `*` → `%2A`
- `+` → `%2B`
- `,` → `%2C`
- `;` → `%3B`
- `=` → `%3D`

### Step 3: Encode Your Credentials

**Option A: Use the verification script**

```bash
# Set your MongoDB URL
export MONGODB_URL="mongodb+srv://user@email.com:p@ssw0rd@cluster.mongodb.net/database"

# Run the verification script
python backend/verify_mongodb_url.py
```

The script will show you the properly encoded URL.

**Option B: Manual encoding**

If your username is `user@email.com` and password is `p@ssw0rd`:

1. Encode username: `user@email.com` → `user%40email.com`
2. Encode password: `p@ssw0rd` → `p%40ssw0rd`
3. Result: `mongodb+srv://user%40email.com:p%40ssw0rd@cluster.mongodb.net/database`

### Step 4: Set Environment Variable

**For local development (.env file):**
```
MONGODB_URL=mongodb+srv://user%40email.com:p%40ssw0rd@cluster.mongodb.net/database
```

**For Render deployment:**
1. Go to your Render service dashboard
2. Click "Environment"
3. Set `MONGODB_URL` to your encoded URL
4. Redeploy

### Step 5: Verify Connection

The application will automatically encode the URL at startup. You should see:

```
🔗 Connecting to MongoDB...
✅ MongoDB URL was encoded (special characters detected)
✅ Connected to MongoDB successfully
✅ Using database: sports_diary
✅ Database indexes created
```

## Common Issues

### Issue: Still getting "Username and password must be escaped" error

**Solution:** The encoding function runs automatically, but if you're still getting the error:

1. Check that your MONGODB_URL environment variable is set correctly
2. Run `python backend/verify_mongodb_url.py` to verify encoding
3. Make sure you're using the encoded URL in your environment variable
4. Restart the application after changing the environment variable

### Issue: Connection timeout

**Solution:** 
- Check that your MongoDB cluster allows connections from your IP
- For MongoDB Atlas, add your IP to the IP Whitelist
- For local MongoDB, ensure the service is running

### Issue: "Authentication failed"

**Solution:**
- Verify username and password are correct
- Make sure special characters are properly encoded
- Check that the database name is correct

## How It Works

The application automatically encodes your MongoDB URL at startup:

1. Reads `MONGODB_URL` environment variable
2. Detects if credentials contain special characters
3. Encodes username and password using `urllib.parse.quote_plus()`
4. Connects to MongoDB with the encoded URL

This happens transparently - you don't need to do anything special.

## Testing

To test your MongoDB connection:

```bash
# From the backend directory
python -c "
import asyncio
from app.core.database import connect_to_mongo, close_mongo_connection

async def test():
    await connect_to_mongo()
    await close_mongo_connection()

asyncio.run(test())
"
```

## References

- [RFC 3986 - URI Syntax](https://tools.ietf.org/html/rfc3986)
- [MongoDB Connection String URI Format](https://docs.mongodb.com/manual/reference/connection-string/)
- [Python urllib.parse.quote_plus](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.quote_plus)
