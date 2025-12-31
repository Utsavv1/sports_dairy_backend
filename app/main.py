from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api import auth, tournaments, venues, marketplace, nearby, reviews, community
from app.core.database import connect_to_mongo, close_mongo_connection
import os

# Create FastAPI app
app = FastAPI(
    title="Sports Diary API",
    description="API for Sports Diary Application",
    version="1.0.0"
)

# CORS configuration - Allow all origins for development
# For production, set CORS_ORIGINS environment variable with specific domains
origins = os.getenv("CORS_ORIGINS", "*").split(",") if os.getenv("CORS_ORIGINS") != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# MongoDB startup/shutdown events
@app.on_event("startup")
async def startup():
    await connect_to_mongo()
    print("✅ MongoDB connected and ready!")

@app.on_event("shutdown")
async def shutdown():
    await close_mongo_connection()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "sports-diary-api", "database": "mongodb"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Sports Diary API",
        "version": "1.0.0",
        "database": "MongoDB",
        "docs": "/docs"
    }

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tournaments.router, prefix="/api/tournaments", tags=["Tournaments"])
app.include_router(venues.router, prefix="/api/venues", tags=["Venues"])
app.include_router(marketplace.router, prefix="/api/marketplace", tags=["Marketplace"])
app.include_router(nearby.router, prefix="/api/nearby", tags=["Nearby"])
app.include_router(reviews.router, prefix="/api/reviews", tags=["Reviews"])
app.include_router(community.router, prefix="/api/community", tags=["Community"])

# Mount static files for uploads
if not os.path.exists("uploads"):
    os.makedirs("uploads")
if not os.path.exists("uploads/community"):
    os.makedirs("uploads/community")
    
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
