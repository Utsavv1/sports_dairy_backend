from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, Float
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(15), unique=True, index=True, nullable=False)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    age = Column(Integer)
    gender = Column(String(20))
    
    # Role-based fields
    role = Column(String(50))  # Player, Parent, Professional
    professional_type = Column(String(50))  # Umpire, Coach, Trainer, Venue Owner, etc.
    
    # Location
    city = Column(String(50))
    state = Column(String(50), default="Gujarat")
    latitude = Column(Float)  # User's current/preferred latitude
    longitude = Column(Float)  # User's current/preferred longitude
    
    # Profile
    bio = Column(String(500))
    avatar = Column(String(255))
    
    # Sports preferences (stored as JSON array)
    sports_interests = Column(JSON)  # ["Cricket", "Football", "Badminton"]
    
    # Player-specific fields
    player_position = Column(String(50))  # For sports like Football, Cricket
    playing_style = Column(String(100))
    
    # Professional-specific fields
    certification = Column(String(200))
    experience_years = Column(Integer)
    
    # Parent-specific fields
    children_count = Column(Integer)
    
    # System fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    onboarding_completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SportsStats(Base):
    __tablename__ = "sports_stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, nullable=False)
    sport_type = Column(String(50), nullable=False)  # Cricket, Football, etc.
    
    # Universal stats
    matches_played = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    
    # Sport-specific stats (stored as JSON for flexibility)
    detailed_stats = Column(JSON)  # Cricket: runs, wickets, etc. | Football: goals, assists
    
    # Performance metrics
    rating = Column(Float, default=0.0)
    achievements = Column(JSON)  # Array of achievement objects
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Venue(Base):
    __tablename__ = "venues"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, index=True)  # User ID of venue owner
    
    # Basic Info
    name = Column(String(200), nullable=False)
    description = Column(String(1000))
    venue_type = Column(String(50))  # Turf, Court, Ground, Stadium
    
    # Sports & Facilities
    sports_available = Column(JSON)  # ["Cricket", "Football", "Tennis"]
    amenities = Column(JSON)  # ["Parking", "Changing Room", "Cafeteria", "First Aid"]
    
    # Location
    city = Column(String(50), nullable=False, index=True)
    state = Column(String(50), default="Gujarat")
    address = Column(String(500))
    landmark = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Pricing & Availability
    price_per_hour = Column(Float, nullable=False)
    weekend_price = Column(Float)  # Different pricing for weekends
    peak_hour_price = Column(Float)  # Evening pricing
    currency = Column(String(10), default="INR")
    
    # Operating Hours
    opening_time = Column(String(10))  # "06:00"
    closing_time = Column(String(10))  # "23:00"
    operating_days = Column(JSON)  # ["Monday", "Tuesday", ...]
    
    # Venue Details
    capacity = Column(Integer)  # Max players
    surface_type = Column(String(50))  # Turf, Concrete, Wooden, etc.
    indoor_outdoor = Column(String(20))  # Indoor/Outdoor/Both
    images = Column(JSON)  # Array of image URLs
    
    # Contact & Social
    contact_number = Column(String(15))
    email = Column(String(100))
    website = Column(String(200))
    
    # Ratings & Reviews
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    
    # Business Metrics
    total_bookings = Column(Integer, default=0)
    is_verified = Column(Boolean, default=False)
    is_featured = Column(Boolean, default=False)
    
    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Booking(Base):
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    booking_number = Column(String(50), unique=True, index=True)  # BK-20250101-001
    
    # Relationships
    user_id = Column(Integer, index=True, nullable=False)
    venue_id = Column(Integer, index=True, nullable=False)
    
    # Booking Details
    sport_type = Column(String(50))
    booking_date = Column(String(20), nullable=False)  # "2025-01-15"
    start_time = Column(String(10), nullable=False)  # "18:00"
    end_time = Column(String(10), nullable=False)  # "19:00"
    duration_hours = Column(Float)
    
    # Players & Team
    player_count = Column(Integer)
    team_name = Column(String(100))
    contact_person = Column(String(100))
    contact_number = Column(String(15))
    
    # Pricing
    base_price = Column(Float, nullable=False)
    additional_charges = Column(JSON)  # [{"item": "Equipment", "amount": 200}]
    discount_amount = Column(Float, default=0.0)
    total_amount = Column(Float, nullable=False)
    
    # Payment
    payment_status = Column(String(20), default="pending")  # pending, partial, paid, refunded
    payment_method = Column(String(50))  # UPI, Card, Cash, Split
    paid_amount = Column(Float, default=0.0)
    payment_date = Column(DateTime)
    transaction_id = Column(String(100))
    
    # Split Pay
    is_split_payment = Column(Boolean, default=False)
    split_payment_data = Column(JSON)  # [{"user": "name", "amount": 500, "status": "paid"}]
    split_payment_link = Column(String(200))
    
    # Status & Lifecycle
    status = Column(String(20), default="confirmed")  # pending, confirmed, completed, cancelled
    booking_source = Column(String(50), default="app")  # app, web, phone
    
    # Notes & Special Requests
    special_requests = Column(String(500))
    admin_notes = Column(String(500))
    cancellation_reason = Column(String(500))
    cancelled_at = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VenueReview(Base):
    __tablename__ = "venue_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, index=True, nullable=False)
    user_id = Column(Integer, index=True, nullable=False)
    booking_id = Column(Integer)
    
    rating = Column(Integer, nullable=False)  # 1-5
    review_text = Column(String(1000))
    images = Column(JSON)  # Review images
    
    # Detailed Ratings
    cleanliness_rating = Column(Integer)
    facilities_rating = Column(Integer)
    staff_rating = Column(Integer)
    value_rating = Column(Integer)
    
    is_verified = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class VenueSlot(Base):
    __tablename__ = "venue_slots"
    
    id = Column(Integer, primary_key=True, index=True)
    venue_id = Column(Integer, index=True, nullable=False)
    
    date = Column(String(20), nullable=False, index=True)  # "2025-01-15"
    start_time = Column(String(10), nullable=False)  # "18:00"
    end_time = Column(String(10), nullable=False)  # "19:00"
    
    is_available = Column(Boolean, default=True)
    booking_id = Column(Integer)  # If booked
    
    price = Column(Float)  # Dynamic pricing for this slot
    blocked_reason = Column(String(200))  # Maintenance, Private Event, etc.
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Shop(Base):
    __tablename__ = "shops"
    
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, index=True)  # User ID of shop owner
    
    # Basic Info
    name = Column(String(200), nullable=False)
    description = Column(String(1000))
    shop_type = Column(String(50))  # Retail, Wholesale, Online, Manufacturer
    category = Column(String(50))  # Equipment, Jerseys, Nutrition, Accessories
    
    # Products & Services
    products = Column(JSON)  # [{"name": "Cricket Bat", "price": 2500, "image": "url"}]
    specialization = Column(JSON)  # ["Cricket Equipment", "Custom Jerseys"]
    brands_available = Column(JSON)  # ["Nike", "Adidas", "SG", "MRF"]
    
    # Location
    city = Column(String(50), nullable=False, index=True)
    state = Column(String(50), default="Gujarat")
    address = Column(String(500))
    landmark = Column(String(200))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Contact & Business
    contact_number = Column(String(15), nullable=False)
    whatsapp_number = Column(String(15))
    email = Column(String(100))
    website = Column(String(200))
    
    # Business Details
    established_year = Column(Integer)
    gst_number = Column(String(50))
    license_number = Column(String(50))
    
    # Operating Hours
    opening_time = Column(String(10))
    closing_time = Column(String(10))
    operating_days = Column(JSON)
    
    # Media
    logo = Column(String(255))
    images = Column(JSON)  # Shop photos
    catalogue_pdf = Column(String(255))
    
    # Ratings & Stats
    rating = Column(Float, default=0.0)
    total_reviews = Column(Integer, default=0)
    total_enquiries = Column(Integer, default=0)
    
    # Features
    home_delivery = Column(Boolean, default=False)
    online_payment = Column(Boolean, default=False)
    bulk_orders = Column(Boolean, default=False)
    custom_manufacturing = Column(Boolean, default=False)
    
    # Listing
    is_featured = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    posted_by = Column(Integer, index=True, nullable=False)  # User ID
    
    # Job Details
    title = Column(String(200), nullable=False)
    job_type = Column(String(50), nullable=False)  # Umpire, Coach, Scorer, Physio, Trainer, Manager
    description = Column(String(2000), nullable=False)
    sport_type = Column(String(50))  # Cricket, Football, Tennis, All
    
    # Employment Type
    employment_type = Column(String(50))  # Full-time, Part-time, Freelance, Contract, Per Match
    experience_required = Column(String(100))  # 0-2 years, 2-5 years, 5+ years
    certification_required = Column(JSON)  # ["Level 1 Umpire", "B License Coach"]
    
    # Location
    city = Column(String(50), nullable=False, index=True)
    state = Column(String(50), default="Gujarat")
    location_type = Column(String(50))  # On-site, Remote, Hybrid
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Compensation
    salary_min = Column(Float)
    salary_max = Column(Float)
    salary_type = Column(String(50))  # Per Month, Per Match, Per Hour, Per Session
    currency = Column(String(10), default="INR")
    other_benefits = Column(JSON)  # ["Travel Allowance", "Accommodation"]
    
    # Requirements
    skills_required = Column(JSON)  # ["Match Management", "Player Development"]
    language_required = Column(JSON)  # ["English", "Gujarati", "Hindi"]
    min_age = Column(Integer)
    max_age = Column(Integer)
    
    # Application
    application_deadline = Column(DateTime)
    how_to_apply = Column(String(500))
    application_email = Column(String(100))
    application_phone = Column(String(15))
    application_url = Column(String(255))
    
    # Stats
    views_count = Column(Integer, default=0)
    applications_count = Column(Integer, default=0)
    
    # Status
    status = Column(String(20), default="active")  # active, filled, closed, expired
    is_featured = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime)


class Dictionary(Base):
    __tablename__ = "dictionary"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Content
    term = Column(String(200), nullable=False, index=True)
    sport = Column(String(50), nullable=False, index=True)  # Cricket, Football, Tennis, etc.
    category = Column(String(50))  # Rules, Terminology, Technique, Equipment, Academy
    
    # Location (for Academies)
    city = Column(String(50), index=True)
    state = Column(String(50))
    address = Column(String(500))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Contact (for Academies)
    contact_number = Column(String(15))
    contact_email = Column(String(100))
    
    # Details
    definition = Column(String(2000), nullable=False)
    explanation = Column(String(5000))  # Detailed explanation
    examples = Column(JSON)  # Array of example sentences/scenarios
    
    # Media
    images = Column(JSON)  # Illustration images
    video_url = Column(String(255))  # Tutorial video
    diagram_url = Column(String(255))  # Diagram/infographic
    
    # Related Content
    related_terms = Column(JSON)  # Array of related term IDs
    tags = Column(JSON)  # ["beginner", "advanced", "rule", "technique"]
    
    # Multilingual Support
    gujarati_term = Column(String(200))
    hindi_term = Column(String(200))
    
    # Stats
    views_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    
    # SEO & Organization
    slug = Column(String(255), unique=True, index=True)
    difficulty_level = Column(String(20))  # Beginner, Intermediate, Advanced
    
    is_featured = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Tournament(Base):
    __tablename__ = "tournaments"
    
    id = Column(Integer, primary_key=True, index=True)
    organizer_id = Column(Integer, index=True, nullable=False)  # User ID
    
    # Basic Info
    name = Column(String(200), nullable=False)
    description = Column(String(2000))
    sport_type = Column(String(50), nullable=False)  # Cricket, Football, etc.
    tournament_type = Column(String(50))  # League, Knockout, Round-Robin, Mixed
    
    # Format Details
    format = Column(String(100))  # T20, ODI, 5-a-side, 11-a-side, etc.
    team_size = Column(Integer)  # Players per team
    max_teams = Column(Integer, nullable=False)
    min_teams = Column(Integer)
    current_teams = Column(Integer, default=0)
    
    # Categories
    age_category = Column(String(50))  # U-14, U-16, U-19, Open, Senior
    gender_category = Column(String(20))  # Men, Women, Mixed
    skill_level = Column(String(50))  # Beginner, Intermediate, Professional
    
    # Location
    city = Column(String(50), nullable=False, index=True)
    state = Column(String(50), default="Gujarat")
    venue_name = Column(String(200))
    venue_address = Column(String(500))
    venue_id = Column(Integer)  # Link to Venue if available
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Schedule
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    registration_start = Column(DateTime)
    registration_deadline = Column(DateTime, nullable=False)
    
    # Fees & Prizes
    entry_fee = Column(Float, default=0)
    currency = Column(String(10), default="INR")
    prize_pool = Column(Float)
    prize_distribution = Column(JSON)  # [{"position": "Winner", "prize": 50000}]
    
    # Registration Requirements
    documents_required = Column(JSON)  # ["ID Proof", "Age Certificate"]
    team_composition_rules = Column(JSON)  # Min/max players, substitutes
    
    # Rules & Regulations
    rules = Column(String(5000))
    match_rules = Column(JSON)  # Specific match rules
    ball_type = Column(String(50))  # Tennis ball, Leather, etc.
    
    # Media & Branding
    banner_image = Column(String(255))
    logo = Column(String(255))
    images = Column(JSON)
    
    # Contact
    contact_person = Column(String(100))
    contact_number = Column(String(15))
    contact_email = Column(String(100))
    
    # Features
    live_scoring = Column(Boolean, default=False)
    live_streaming = Column(Boolean, default=False)
    certificates_provided = Column(Boolean, default=False)
    
    # Stats
    views_count = Column(Integer, default=0)
    
    # Status
    status = Column(String(20), default="upcoming")  # upcoming, ongoing, completed, cancelled
    is_featured = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    captain_id = Column(Integer, index=True, nullable=False)  # User ID
    tournament_id = Column(Integer, index=True)  # If registered for tournament
    
    # Team Details
    name = Column(String(200), nullable=False)
    short_name = Column(String(50))
    description = Column(String(1000))
    sport_type = Column(String(50), nullable=False)
    
    # Location
    city = Column(String(50), nullable=False)
    state = Column(String(50), default="Gujarat")
    home_ground = Column(String(200))
    
    # Team Info
    logo = Column(String(255))
    jersey_color = Column(String(50))
    founded_year = Column(Integer)
    team_type = Column(String(50))  # Club, Corporate, College, Friends
    
    # Players (JSON array of player objects)
    players = Column(JSON)  # [{"user_id": 1, "name": "Player 1", "role": "Batsman", "jersey_no": 10}]
    total_players = Column(Integer, default=0)
    
    # Management
    coach_name = Column(String(100))
    manager_name = Column(String(100))
    manager_contact = Column(String(15))
    
    # Stats
    matches_played = Column(Integer, default=0)
    matches_won = Column(Integer, default=0)
    matches_lost = Column(Integer, default=0)
    matches_drawn = Column(Integer, default=0)
    
    # Documents (for tournament registration)
    documents = Column(JSON)  # [{"type": "ID Proof", "url": "...", "status": "verified"}]
    
    # Status
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TournamentRegistration(Base):
    __tablename__ = "tournament_registrations"
    
    id = Column(Integer, primary_key=True, index=True)
    registration_number = Column(String(50), unique=True, index=True)  # REG-TOUR001-TEAM001
    
    # Relationships
    tournament_id = Column(Integer, index=True, nullable=False)
    team_id = Column(Integer, index=True, nullable=False)
    registered_by = Column(Integer, nullable=False)  # User ID (captain)
    
    # Registration Details
    registration_date = Column(DateTime, default=datetime.utcnow)
    
    # Team Roster for this tournament
    team_roster = Column(JSON)  # Snapshot of players at registration time
    captain_name = Column(String(100))
    captain_contact = Column(String(15))
    vice_captain_name = Column(String(100))
    
    # Payment
    entry_fee = Column(Float, default=0)
    payment_status = Column(String(20), default="pending")  # pending, paid, refunded
    payment_method = Column(String(50))
    payment_date = Column(DateTime)
    transaction_id = Column(String(100))
    
    # Documents Submission
    documents_submitted = Column(JSON)  # [{"type": "...", "url": "...", "verified": true}]
    documents_verified = Column(Boolean, default=False)
    
    # Status
    status = Column(String(20), default="pending")  # pending, approved, rejected, withdrawn
    approval_date = Column(DateTime)
    approved_by = Column(Integer)  # Admin user ID
    rejection_reason = Column(String(500))
    
    # Notes
    special_requests = Column(String(500))
    admin_notes = Column(String(500))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

