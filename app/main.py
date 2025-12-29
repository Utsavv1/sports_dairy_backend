from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, venues, marketplace, tournaments, nearby

app = FastAPI(title="Sports Diary - Professional Sports ERP System")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(venues.router, prefix="/api", tags=["Venues & Bookings"])
app.include_router(marketplace.router, prefix="/api", tags=["Marketplace"])
app.include_router(tournaments.router, prefix="/api", tags=["Tournaments"])
app.include_router(nearby.router, prefix="/api/nearby", tags=["Nearby & Location"])

@app.get("/")
async def root():
    return {
        "message": "Sports Diary API - Professional Sports ERP System",
        "version": "3.0.0",
        "features": [
            "Venues & Bookings",
            "Tournaments & Teams",
            "Sports Marketplace (Shops & Equipment)",
            "Jobs Portal (Coaches, Umpires, Trainers)",
            "Sports Dictionary & Learning",
            "Split Payment System",
            "Reviews & Ratings"
        ],
        "status": "active"
    }

