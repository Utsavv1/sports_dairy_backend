from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.schemas import (
    ShopCreate, ShopUpdate, ShopResponse,
    JobCreate, JobUpdate, JobResponse,
    DictionaryCreate, DictionaryUpdate, DictionaryResponse
)

router = APIRouter(tags=["marketplace"])


# ==================== SHOPS ENDPOINTS ====================

@router.get("/shops")
async def get_shops(
    city: Optional[str] = None,
    category: Optional[str] = None,
    shop_type: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get list of sports shops with filters"""
    db = get_database()
    
    query = {"is_active": True}
    
    if city:
        query["city"] = city
    if category:
        query["category"] = category
    if shop_type:
        query["shop_type"] = shop_type
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    # Get total count before limiting
    total_count = await db.shops.count_documents(query)
    
    shops_cursor = db.shops.find(query).skip(skip).limit(limit).sort([("is_featured", -1), ("rating", -1)])
    shops = await shops_cursor.to_list(length=limit)
    
    for shop in shops:
        shop["id"] = str(shop["_id"])
        del shop["_id"]  # Remove ObjectId
    
    return {"shops": shops, "count": total_count}


@router.get("/shops/{shop_id}")
async def get_shop(shop_id: str):
    """Get shop details"""
    db = get_database()
    
    try:
        shop = await db.shops.find_one({"_id": ObjectId(shop_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid shop ID")
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    # Increment enquiry count
    await db.shops.update_one(
        {"_id": ObjectId(shop_id)},
        {"$inc": {"total_enquiries": 1}}
    )
    
    shop["id"] = str(shop["_id"])

    
    del shop["_id"]  # Remove ObjectId
    return shop


@router.post("/shops")
async def create_shop(
    shop_data: ShopCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new shop listing"""
    db = get_database()
    
    shop_dict = shop_data.dict()
    shop_dict["owner_id"] = str(current_user["_id"])
    shop_dict["created_at"] = datetime.utcnow()
    shop_dict["updated_at"] = datetime.utcnow()
    shop_dict["is_active"] = True
    shop_dict["rating"] = 0.0
    shop_dict["total_reviews"] = 0
    shop_dict["total_enquiries"] = 0
    
    result = await db.shops.insert_one(shop_dict)
    created_shop = await db.shops.find_one({"_id": result.inserted_id})
    created_shop["id"] = str(created_shop["_id"])

    del created_shop["_id"]  # Remove ObjectId
    
    return created_shop


@router.put("/shops/{shop_id}")
async def update_shop(
    shop_id: str,
    shop_data: ShopUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update shop"""
    db = get_database()
    
    try:
        shop = await db.shops.find_one({"_id": ObjectId(shop_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid shop ID")
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    # Check ownership
    if str(shop.get("owner_id")) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {k: v for k, v in shop_data.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.shops.update_one(
        {"_id": ObjectId(shop_id)},
        {"$set": update_data}
    )
    
    updated_shop = await db.shops.find_one({"_id": ObjectId(shop_id)})
    updated_shop["id"] = str(updated_shop["_id"])

    del updated_shop["_id"]  # Remove ObjectId
    
    return updated_shop


@router.delete("/shops/{shop_id}")
async def delete_shop(
    shop_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete/deactivate shop"""
    db = get_database()
    
    try:
        shop = await db.shops.find_one({"_id": ObjectId(shop_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid shop ID")
    
    if not shop:
        raise HTTPException(status_code=404, detail="Shop not found")
    
    # Check ownership
    if str(shop.get("owner_id")) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Soft delete
    await db.shops.update_one(
        {"_id": ObjectId(shop_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Shop deleted successfully"}


# ==================== JOBS ENDPOINTS ====================

@router.get("/jobs")
async def get_jobs(
    city: Optional[str] = None,
    job_type: Optional[str] = None,
    sport_type: Optional[str] = None,
    employment_type: Optional[str] = None,
    status: Optional[str] = "active",
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get list of job postings with filters"""
    db = get_database()
    
    query = {}
    
    if status:
        query["status"] = status
    if city:
        query["city"] = city
    if job_type:
        query["job_type"] = job_type
    if sport_type:
        query["sport_type"] = sport_type
    if employment_type:
        query["employment_type"] = employment_type
    if search:
        query["$or"] = [
            {"title": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    # Get total count before limiting
    total_count = await db.jobs.count_documents(query)
    
    jobs_cursor = db.jobs.find(query).skip(skip).limit(limit).sort([("is_featured", -1), ("created_at", -1)])
    jobs = await jobs_cursor.to_list(length=limit)
    
    for job in jobs:
        job["id"] = str(job["_id"])
        del job["_id"]  # Remove ObjectId
    
    return {"jobs": jobs, "count": total_count}


@router.get("/jobs/{job_id}")
async def get_job(job_id: str):
    """Get job details"""
    db = get_database()
    
    try:
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid job ID")
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Increment views count
    await db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$inc": {"views_count": 1}}
    )
    
    job["id"] = str(job["_id"])

    
    del job["_id"]  # Remove ObjectId
    return job


@router.post("/jobs")
async def create_job(
    job_data: JobCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new job posting"""
    db = get_database()
    
    job_dict = job_data.dict()
    job_dict["posted_by"] = str(current_user["_id"])
    job_dict["created_at"] = datetime.utcnow()
    job_dict["updated_at"] = datetime.utcnow()
    job_dict["status"] = "active"
    job_dict["views_count"] = 0
    job_dict["applications_count"] = 0
    
    result = await db.jobs.insert_one(job_dict)
    created_job = await db.jobs.find_one({"_id": result.inserted_id})
    created_job["id"] = str(created_job["_id"])

    del created_job["_id"]  # Remove ObjectId
    
    return created_job


@router.put("/jobs/{job_id}")
async def update_job(
    job_id: str,
    job_data: JobUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update job"""
    db = get_database()
    
    try:
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid job ID")
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check ownership
    if str(job["posted_by"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {k: v for k, v in job_data.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": update_data}
    )
    
    updated_job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    updated_job["id"] = str(updated_job["_id"])

    del updated_job["_id"]  # Remove ObjectId
    
    return updated_job


@router.delete("/jobs/{job_id}")
async def delete_job(
    job_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete job posting"""
    db = get_database()
    
    try:
        job = await db.jobs.find_one({"_id": ObjectId(job_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid job ID")
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check ownership
    if str(job["posted_by"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update status to closed
    await db.jobs.update_one(
        {"_id": ObjectId(job_id)},
        {"$set": {"status": "closed", "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Job posting deleted successfully"}


# ==================== DICTIONARY ENDPOINTS (Sports Academy/Terms) ====================

@router.get("/dictionary")
async def get_dictionary_entries(
    sport: Optional[str] = None,
    category: Optional[str] = None,
    city: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get dictionary entries (sports terms and academies)"""
    db = get_database()
    
    query = {"is_active": True}
    
    if sport:
        query["sport"] = sport
    if category:
        query["category"] = category
    if city:
        query["city"] = city
    if search:
        query["$or"] = [
            {"term": {"$regex": search, "$options": "i"}},
            {"definition": {"$regex": search, "$options": "i"}}
        ]
    
    # Get total count before limiting
    total_count = await db.dictionary.count_documents(query)
    
    entries_cursor = db.dictionary.find(query).skip(skip).limit(limit).sort([("is_featured", -1), ("views_count", -1)])
    entries = await entries_cursor.to_list(length=limit)
    
    for entry in entries:
        entry["id"] = str(entry["_id"])
        del entry["_id"]  # Remove ObjectId
    
    return {"academies": entries, "count": total_count}


@router.get("/dictionary/{entry_id}")
async def get_dictionary_entry(entry_id: str):
    """Get dictionary entry details"""
    db = get_database()
    
    try:
        entry = await db.dictionary.find_one({"_id": ObjectId(entry_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid entry ID")
    
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Increment views count
    await db.dictionary.update_one(
        {"_id": ObjectId(entry_id)},
        {"$inc": {"views_count": 1}}
    )
    
    entry["id"] = str(entry["_id"])

    
    del entry["_id"]  # Remove ObjectId
    return entry


@router.post("/dictionary")
async def create_dictionary_entry(
    entry_data: DictionaryCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create a new dictionary entry"""
    db = get_database()
    
    entry_dict = entry_data.dict()
    entry_dict["created_at"] = datetime.utcnow()
    entry_dict["updated_at"] = datetime.utcnow()
    entry_dict["is_active"] = True
    entry_dict["views_count"] = 0
    entry_dict["helpful_count"] = 0
    
    result = await db.dictionary.insert_one(entry_dict)
    created_entry = await db.dictionary.find_one({"_id": result.inserted_id})
    created_entry["id"] = str(created_entry["_id"])

    del created_entry["_id"]  # Remove ObjectId
    
    return created_entry


@router.put("/dictionary/{entry_id}")
async def update_dictionary_entry(
    entry_id: str,
    entry_data: DictionaryUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update dictionary entry"""
    db = get_database()
    
    try:
        entry = await db.dictionary.find_one({"_id": ObjectId(entry_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid entry ID")
    
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    update_data = {k: v for k, v in entry_data.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.dictionary.update_one(
        {"_id": ObjectId(entry_id)},
        {"$set": update_data}
    )
    
    updated_entry = await db.dictionary.find_one({"_id": ObjectId(entry_id)})
    updated_entry["id"] = str(updated_entry["_id"])

    del updated_entry["_id"]  # Remove ObjectId
    
    return updated_entry


@router.delete("/dictionary/{entry_id}")
async def delete_dictionary_entry(
    entry_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete dictionary entry"""
    db = get_database()
    
    try:
        entry = await db.dictionary.find_one({"_id": ObjectId(entry_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid entry ID")
    
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    # Soft delete
    await db.dictionary.update_one(
        {"_id": ObjectId(entry_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Dictionary entry deleted successfully"}

