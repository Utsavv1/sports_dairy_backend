# Install MongoDB on Windows

## Method 1: Official Installer (Recommended)

### Step 1: Download
1. Visit: https://www.mongodb.com/try/download/community
2. Select:
   - Version: 7.0 or latest
   - Platform: Windows
   - Package: MSI
3. Click "Download"

### Step 2: Install
1. Run the downloaded `.msi` file
2. Choose "Complete" installation
3. **✅ IMPORTANT: Check "Install MongoDB as a Service"**
4. Leave default paths (C:\Program Files\MongoDB\)
5. Click Install

### Step 3: Verify Installation
Open PowerShell as Administrator and run:
```powershell
net start MongoDB
```

### Step 4: Test Connection
```powershell
mongosh
```

You should see MongoDB shell connect successfully.

---

## Method 2: Chocolatey (Quick Install)

If you have Chocolatey package manager:

```powershell
# Run as Administrator
choco install mongodb

# Start MongoDB service
net start MongoDB
```

---

## Method 3: Portable (No Installation)

1. Download MongoDB ZIP from: https://www.mongodb.com/try/download/community
2. Extract to: `C:\mongodb`
3. Create data directory: `C:\mongodb\data`
4. Start MongoDB manually:
```powershell
cd C:\mongodb\bin
.\mongod.exe --dbpath C:\mongodb\data
```

---

## Verify MongoDB is Running

```powershell
# Check service status
Get-Service -Name MongoDB

# Test connection
mongosh --eval "db.runCommand({ ping: 1 })"
```

---

## Configure MongoDB (Optional)

Default settings work fine, but you can customize:

**Config file location:** `C:\Program Files\MongoDB\Server\7.0\bin\mongod.cfg`

```yaml
storage:
  dbPath: C:\data\db
net:
  port: 27017
  bindIp: 127.0.0.1
```

---

## Troubleshooting

### Issue: "Service not found"
**Solution:** MongoDB wasn't installed as a service. Use Method 3 (Portable) or reinstall with "Install as Service" checked.

### Issue: "Access denied"
**Solution:** Run PowerShell as Administrator to start/stop services.

### Issue: "Port 27017 already in use"
**Solution:** Another instance is running. Check Task Manager for `mongod.exe`.

---

## After Installation

1. ✅ MongoDB is running on `localhost:27017`
2. ✅ Seed your database:
   ```powershell
   cd backend
   python seed_mongodb.py
   ```
3. ✅ Start your backend:
   ```powershell
   python run.py
   ```

---

## Quick Commands Reference

```powershell
# Start MongoDB
net start MongoDB

# Stop MongoDB
net stop MongoDB

# Check status
Get-Service MongoDB

# Access MongoDB Shell
mongosh

# View databases
mongosh --eval "show dbs"

# View collections in sports_diary
mongosh sports_diary --eval "show collections"
```

---

**Need help?** Check the official docs: https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/

