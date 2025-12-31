# MongoDB Connection Guide

## 🔗 Default Connection

Your backend is **already configured** to connect to:
```
mongodb://localhost:27017
```

**Database Name:** `sports_diary`

---

## ✅ How It Works

### 1. Configuration (backend/app/core/database.py)

```python
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "sports_diary")
```

- ✅ Uses `localhost:27017` by default
- ✅ Database: `sports_diary`
- ✅ Can be customized via environment variables

### 2. Connection Process

When you run `python run.py`:

1. Backend starts
2. Connects to MongoDB at `localhost:27017`
3. Creates/uses database `sports_diary`
4. Creates indexes automatically
5. API is ready! 🚀

---

## 🧪 Test Your Connection

Run this command to verify MongoDB is accessible:

```powershell
cd backend
python test_mongodb_connection.py
```

**Expected Output (Success):**
```
================================================================
  🔍 Testing MongoDB Connection
================================================================

📡 Connecting to: mongodb://localhost:27017
📊 Database: sports_diary

⏳ Pinging MongoDB server...
✅ SUCCESS! MongoDB is running and accessible!

📂 Collections in 'sports_diary' database:
   • venues: 25 documents
   • tournaments: 2 documents
   • shops: 1 documents
   ...

================================================================
  ✅ MongoDB Connection Test PASSED!
================================================================

💡 Your backend will connect successfully!
   Run: python run.py
```

**Expected Output (Failure):**
```
❌ CONNECTION FAILED!
   Error: [Errno 111] Connection refused

⚠️  MongoDB is NOT running or not installed
```

---

## 🔧 Customize Connection (Optional)

### Method 1: Environment Variables

Create a `.env` file in `backend/` folder:

```bash
# .env file
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sports_diary
```

### Method 2: Different Port

If MongoDB is running on a different port:

```bash
MONGODB_URL=mongodb://localhost:27018
```

### Method 3: Remote MongoDB

For MongoDB Atlas or remote server:

```bash
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
DATABASE_NAME=sports_diary
```

### Method 4: With Authentication

If your MongoDB has authentication:

```bash
MONGODB_URL=mongodb://username:password@localhost:27017
```

---

## 🚀 Quick Start Steps

### 1. Check if MongoDB is Running

```powershell
# Check service status
Get-Service MongoDB

# Should show: Status = Running
```

### 2. Test Connection

```powershell
cd backend
python test_mongodb_connection.py
```

### 3. Seed Database (First Time Only)

```powershell
python seed_mongodb.py
```

### 4. Start Backend

```powershell
python run.py
```

You should see:
```
============================================================
  🚀 BACKEND API WITH MONGODB READY
============================================================

  ->  Local:   http://localhost:8000/
  ->  Docs:    http://localhost:8000/docs

============================================================
  💾 Database: MongoDB @ localhost:27017
  📊 Database Name: sports_diary
============================================================

✅ Connected to MongoDB at mongodb://localhost:27017
✅ Using database: sports_diary
✅ Database indexes created
```

---

## 📊 View Your Data

### Using MongoDB Shell

```powershell
# Connect to MongoDB
mongosh

# Switch to sports_diary database
use sports_diary

# List collections
show collections

# Count documents
db.venues.countDocuments()
db.users.countDocuments()

# View sample data
db.venues.findOne()
db.users.find().limit(5)
```

### Using MongoDB Compass (GUI)

1. Download: https://www.mongodb.com/products/compass
2. Connect to: `mongodb://localhost:27017`
3. Browse database: `sports_diary`
4. View collections visually

---

## ❌ Troubleshooting

### Issue: "Connection timeout" or "Connection refused"

**Problem:** MongoDB is not running

**Solution:**
```powershell
# Start MongoDB service
net start MongoDB

# Verify it's running
Get-Service MongoDB
```

### Issue: "No module named 'motor'"

**Problem:** Dependencies not installed

**Solution:**
```powershell
cd backend
pip install -r requirements.txt
```

### Issue: "Database is empty"

**Problem:** Database hasn't been seeded

**Solution:**
```powershell
python seed_mongodb.py
```

### Issue: "Port 27017 already in use"

**Problem:** Another process is using port 27017

**Solution:**
```powershell
# Check what's using the port
netstat -ano | findstr :27017

# Stop MongoDB and restart
net stop MongoDB
net start MongoDB
```

### Issue: "Authentication failed"

**Problem:** Your MongoDB requires authentication

**Solution:** Add credentials to MONGODB_URL:
```bash
MONGODB_URL=mongodb://username:password@localhost:27017
```

---

## 🔒 Production Configuration

For production deployment:

```bash
# Use MongoDB Atlas or managed MongoDB
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority

# Or self-hosted with authentication
MONGODB_URL=mongodb://admin:securepassword@production-server:27017

# Different database for production
DATABASE_NAME=sports_diary_production

# Enable SSL/TLS
MONGODB_URL=mongodb://localhost:27017/?tls=true&tlsCAFile=/path/to/ca.pem
```

---

## 📚 Additional Resources

- **MongoDB Docs:** https://www.mongodb.com/docs/
- **Motor (Async Driver):** https://motor.readthedocs.io/
- **Connection String Format:** https://www.mongodb.com/docs/manual/reference/connection-string/

---

## 💡 Quick Commands Reference

```powershell
# Test connection
python test_mongodb_connection.py

# Seed database
python seed_mongodb.py

# Start backend
python run.py

# MongoDB Shell
mongosh

# Check service
Get-Service MongoDB

# Start service
net start MongoDB

# Stop service
net stop MongoDB
```

---

**Your connection is already configured! Just make sure MongoDB is running.** 🚀

