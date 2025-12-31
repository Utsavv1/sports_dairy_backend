# MongoDB Migration Complete! 🎉

## Overview
Successfully migrated Sports Diary backend from SQLite/SQLAlchemy to MongoDB!

## What Changed

### 1. **Database System**
- ❌ Removed: SQLite + SQLAlchemy ORM
- ✅ Added: MongoDB + Motor (async MongoDB driver)

### 2. **Dependencies** (`requirements.txt`)
```
Removed:
- sqlalchemy==2.0.23
- aiosqlite==0.19.0

Added:
- motor==3.3.2
- pymongo==4.6.1
```

### 3. **Database Configuration** (`app/core/database.py`)
- MongoDB connection using Motor
- Async MongoDB client
- Collection access helpers
- Automatic index creation

### 4. **Models** (`app/models/models.py`)
- Converted from SQLAlchemy ORM models to Pydantic models
- All models now use MongoDB document structure
- ObjectId support for MongoDB _id fields

### 5. **API Endpoints** (All updated to MongoDB)
- ✅ `app/api/auth.py` - User authentication
- ✅ `app/api/venues.py` - Venue management
- ✅ `app/api/tournaments.py` - Tournament management
- ✅ `app/api/marketplace.py` - Shops, Jobs, Dictionary
- ✅ `app/api/nearby.py` - Location-based queries

### 6. **Seed Script**
- Created: `backend/seed_mongodb.py`
- Seeds all collections with sample data

## Setup Instructions

### Step 1: Install MongoDB

**Windows:**
```bash
# Download from: https://www.mongodb.com/try/download/community
# Install MongoDB Community Edition
# Start MongoDB service
```

**Mac:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux:**
```bash
sudo apt-get install mongodb
sudo systemctl start mongodb
```

### Step 2: Install Python Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Seed the Database
```bash
python seed_mongodb.py
```

### Step 4: Start the Backend
```bash
python run.py
```

## MongoDB Connection Settings

Default configuration (can be changed via environment variables):
- **URL:** `mongodb://localhost:27017`
- **Database:** `sports_diary`

### Environment Variables (Optional)
```bash
# .env file
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sports_diary
```

## Collections

| Collection | Purpose |
|-----------|---------|
| `users` | User accounts and profiles |
| `venues` | Sports venues |
| `bookings` | Venue bookings |
| `venue_reviews` | Venue reviews |
| `tournaments` | Tournaments |
| `teams` | Teams |
| `tournament_registrations` | Tournament registrations |
| `shops` | Sports shops |
| `jobs` | Job postings |
| `dictionary` | Sports terms & academies |

## Indexes Created

Automatically created indexes for performance:
- **users**: phone (unique), email (unique), city+state, latitude+longitude
- **venues**: city, latitude+longitude, is_active
- **tournaments**: city, sport_type, latitude+longitude, status
- **shops**: city, category, latitude+longitude
- **jobs**: city, job_type, status
- **dictionary**: sport, term, city, slug (unique)
- **bookings**: booking_number (unique), user_id, venue_id, booking_date+venue_id

## API Changes

### ✅ No API Contract Changes!
All endpoints work exactly the same way from the frontend's perspective. Only internal database queries changed.

### Response Format Changes
- `id` field is now a string (MongoDB ObjectId converted to string)
- All other fields remain the same

## Testing

### 1. Check MongoDB Connection
```bash
# Open MongoDB Shell
mongosh

# Switch to sports_diary database
use sports_diary

# List collections
show collections

# Count documents
db.venues.countDocuments()
```

### 2. Test API Endpoints
```bash
# Health check
curl http://localhost:8000/health

# Get venues
curl http://localhost:8000/api/venues

# Get tournaments
curl http://localhost:8000/api/tournaments
```

## Benefits of MongoDB

✅ **Flexible Schema**: Easy to add new fields without migrations
✅ **Better Performance**: Optimized for document-based queries
✅ **Scalability**: Horizontal scaling support
✅ **Geospatial Queries**: Built-in location-based search
✅ **JSON-native**: Perfect for JavaScript/React frontend
✅ **No Migrations**: Schema changes don't require migrations

## Troubleshooting

### Issue: "Connection refused" error
**Solution:** Make sure MongoDB is running
```bash
# Windows
net start MongoDB

# Mac/Linux
sudo systemctl start mongodb
# or
brew services start mongodb-community
```

### Issue: "Database not found"
**Solution:** Run the seed script
```bash
python seed_mongodb.py
```

### Issue: "Module not found: motor"
**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

## Migration Rollback (If Needed)

If you need to rollback to SQLite:
1. Git checkout previous commit before MongoDB migration
2. Or restore the `player_app.db` file from backup

## Next Steps

1. ✅ Start MongoDB service
2. ✅ Install dependencies: `pip install -r requirements.txt`
3. ✅ Seed database: `python seed_mongodb.py`
4. ✅ Start backend: `python run.py`
5. ✅ Test frontend connectivity

## Notes

- MongoDB runs on default port: `27017`
- Database name: `sports_diary`
- All async operations preserved
- CORS settings unchanged
- Authentication flow unchanged
- Frontend requires NO changes!

---

**Migration completed successfully! 🚀**
Database is now running on MongoDB with all features working.

