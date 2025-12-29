from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Shop, Job, Dictionary, User
from app.schemas.schemas import (
    ShopCreate, ShopUpdate, ShopResponse,
    JobCreate, JobUpdate, JobResponse,
    DictionaryCreate, DictionaryUpdate, DictionaryResponse
)

router = APIRouter(prefix="/marketplace", tags=["marketplace"])


# ==================== SHOPS ENDPOINTS ====================

@router.get("/shops", response_model=List[ShopResponse])
async def get_shops(
    city: Optional[str] = None,
    category: Optional[str] = None,
    shop_type: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get list of sports shops with filters"""
    query = select(Shop).where(Shop.is_active == True)
    
    if city:
        query = query.where(Shop.city == city)
    if category:
        query = query.where(Shop.category == category)
    if shop_type:
        query = query.where(Shop.shop_type == shop_type)
    if search:
        query = query.where(
            (Shop.name.ilike(f"%{search}%")) |
            (Shop.description.ilike(f"%{search}%"))
        )
    
    # Order by featured first, then by rating
    query = query.order_by(Shop.is_featured.desc(), Shop.rating.desc())
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    shops = result.scalars().all()
    return shops


@router.get("/shops/{shop_id}", response_model=ShopResponse)
async def get_shop(shop_id: int, db: AsyncSession = Depends(get_db)):
    """Get shop details"""
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    # Increment enquiry count
    shop.total_enquiries += 1
    await db.commit()
    
    return shop


@router.post("/shops", response_model=ShopResponse)
async def create_shop(
    shop_data: ShopCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new shop listing"""
    new_shop = Shop(
        **shop_data.model_dump(),
        owner_id=current_user.id
    )
    
    db.add(new_shop)
    await db.commit()
    await db.refresh(new_shop)
    return new_shop


@router.put("/shops/{shop_id}", response_model=ShopResponse)
async def update_shop(
    shop_id: int,
    shop_data: ShopUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update shop listing"""
    result = await db.execute(select(Shop).where(Shop.id == shop_id))
    shop = result.scalar_one_or_none()
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    if shop.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    for field, value in shop_data.model_dump(exclude_unset=True).items():
        setattr(shop, field, value)
    
    await db.commit()
    await db.refresh(shop)
    return shop


# ==================== JOBS ENDPOINTS ====================

@router.get("/jobs", response_model=List[JobResponse])
async def get_jobs(
    city: Optional[str] = None,
    job_type: Optional[str] = None,
    sport_type: Optional[str] = None,
    employment_type: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get list of sports jobs with filters"""
    query = select(Job).where(Job.status == "active")
    
    if city:
        query = query.where(Job.city == city)
    if job_type:
        query = query.where(Job.job_type == job_type)
    if sport_type:
        query = query.where(Job.sport_type == sport_type)
    if employment_type:
        query = query.where(Job.employment_type == employment_type)
    if search:
        query = query.where(
            (Job.title.ilike(f"%{search}%")) |
            (Job.description.ilike(f"%{search}%"))
        )
    
    # Order by featured first, then by creation date
    query = query.order_by(Job.is_featured.desc(), Job.created_at.desc())
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    jobs = result.scalars().all()
    return jobs


@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db)):
    """Get job details"""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Increment views count
    job.views_count += 1
    await db.commit()
    
    return job


@router.post("/jobs", response_model=JobResponse)
async def create_job(
    job_data: JobCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Post a new job"""
    new_job = Job(
        **job_data.model_dump(),
        posted_by=current_user.id
    )
    
    db.add(new_job)
    await db.commit()
    await db.refresh(new_job)
    return new_job


@router.put("/jobs/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: int,
    job_data: JobUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update job posting"""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.posted_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    for field, value in job_data.model_dump(exclude_unset=True).items():
        setattr(job, field, value)
    
    await db.commit()
    await db.refresh(job)
    return job


# ==================== DICTIONARY ENDPOINTS ====================

@router.get("/dictionary", response_model=List[DictionaryResponse])
async def get_dictionary_terms(
    sport: Optional[str] = None,
    category: Optional[str] = None,
    difficulty_level: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get sports dictionary terms with filters"""
    query = select(Dictionary).where(Dictionary.is_active == True)
    
    if sport:
        query = query.where(Dictionary.sport == sport)
    if category:
        query = query.where(Dictionary.category == category)
    if difficulty_level:
        query = query.where(Dictionary.difficulty_level == difficulty_level)
    if search:
        query = query.where(
            (Dictionary.term.ilike(f"%{search}%")) |
            (Dictionary.definition.ilike(f"%{search}%"))
        )
    
    # Order by featured first, then alphabetically
    query = query.order_by(Dictionary.is_featured.desc(), Dictionary.term.asc())
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    terms = result.scalars().all()
    return terms


@router.get("/dictionary/{term_id}", response_model=DictionaryResponse)
async def get_dictionary_term(term_id: int, db: AsyncSession = Depends(get_db)):
    """Get dictionary term details"""
    result = await db.execute(select(Dictionary).where(Dictionary.id == term_id))
    term = result.scalar_one_or_none()
    
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    # Increment views count
    term.views_count += 1
    await db.commit()
    
    return term


@router.get("/dictionary/slug/{slug}", response_model=DictionaryResponse)
async def get_dictionary_by_slug(slug: str, db: AsyncSession = Depends(get_db)):
    """Get dictionary term by slug"""
    result = await db.execute(select(Dictionary).where(Dictionary.slug == slug))
    term = result.scalar_one_or_none()
    
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    # Increment views count
    term.views_count += 1
    await db.commit()
    
    return term


@router.post("/dictionary", response_model=DictionaryResponse)
async def create_dictionary_term(
    term_data: DictionaryCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new dictionary term (admin only)"""
    # Generate slug from term
    slug = term_data.term.lower().replace(" ", "-").replace("/", "-")
    
    new_term = Dictionary(
        **term_data.model_dump(),
        slug=slug
    )
    
    db.add(new_term)
    await db.commit()
    await db.refresh(new_term)
    return new_term


@router.put("/dictionary/{term_id}/helpful")
async def mark_helpful(
    term_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Mark a dictionary term as helpful"""
    result = await db.execute(select(Dictionary).where(Dictionary.id == term_id))
    term = result.scalar_one_or_none()
    
    if not term:
        raise HTTPException(status_code=404, detail="Term not found")
    
    term.helpful_count += 1
    await db.commit()
    
    return {"message": "Marked as helpful", "helpful_count": term.helpful_count}


# ==================== STATS ENDPOINTS ====================

@router.get("/stats")
async def get_marketplace_stats(db: AsyncSession = Depends(get_db)):
    """Get marketplace statistics"""
    shops_count = await db.execute(select(func.count(Shop.id)).where(Shop.is_active == True))
    jobs_count = await db.execute(select(func.count(Job.id)).where(Job.status == "active"))
    terms_count = await db.execute(select(func.count(Dictionary.id)).where(Dictionary.is_active == True))
    
    return {
        "total_shops": shops_count.scalar(),
        "total_jobs": jobs_count.scalar(),
        "total_dictionary_terms": terms_count.scalar()
    }

