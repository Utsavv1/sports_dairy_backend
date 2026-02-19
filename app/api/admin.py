from fastapi import APIRouter, Depends, HTTPException, status
from app.core.database import get_database
from app.core.security import get_current_user

router = APIRouter(tags=["admin"])

@router.get("/stats")
async def get_admin_stats(current_user: dict = Depends(get_current_user)):
    """Get system statistics (super admin only)"""
    
    # Check if user is super admin
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        # Count all collections
        users_count = await db.users.count_documents({})
        tournaments_count = await db.tournaments.count_documents({})
        venues_count = await db.venues.count_documents({})
        shops_count = await db.shops.count_documents({})
        jobs_count = await db.jobs.count_documents({})
        communities_count = await db.communities.count_documents({})
        posts_count = await db.community_posts.count_documents({})
        
        return {
            "total_users": users_count,
            "total_tournaments": tournaments_count,
            "total_venues": venues_count,
            "total_shops": shops_count,
            "total_jobs": jobs_count,
            "total_communities": communities_count,
            "total_posts": posts_count
        }
    except Exception as e:
        print(f"Error getting stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get statistics"
        )

@router.get("/users")
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all users (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        users_cursor = db.users.find({}).skip(skip).limit(limit).sort([("created_at", -1)])
        users = await users_cursor.to_list(length=limit)
        
        for user in users:
            user["id"] = str(user["_id"])
            del user["_id"]
        
        total = await db.users.count_documents({})
        
        return {
            "users": users,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        print(f"Error getting users: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get users"
        )

@router.get("/tournaments")
async def get_all_tournaments(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all tournaments (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        tournaments_cursor = db.tournaments.find({}).skip(skip).limit(limit).sort([("created_at", -1)])
        tournaments = await tournaments_cursor.to_list(length=limit)
        
        for tournament in tournaments:
            tournament["id"] = str(tournament["_id"])
            del tournament["_id"]
        
        total = await db.tournaments.count_documents({})
        
        return {
            "tournaments": tournaments,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        print(f"Error getting tournaments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get tournaments"
        )

@router.get("/venues")
async def get_all_venues(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all venues (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        venues_cursor = db.venues.find({}).skip(skip).limit(limit).sort([("created_at", -1)])
        venues = await venues_cursor.to_list(length=limit)
        
        for venue in venues:
            venue["id"] = str(venue["_id"])
            del venue["_id"]
        
        total = await db.venues.count_documents({})
        
        return {
            "venues": venues,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        print(f"Error getting venues: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get venues"
        )

@router.get("/shops")
async def get_all_shops(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all shops (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        shops_cursor = db.shops.find({}).skip(skip).limit(limit).sort([("created_at", -1)])
        shops = await shops_cursor.to_list(length=limit)
        
        for shop in shops:
            shop["id"] = str(shop["_id"])
            del shop["_id"]
        
        total = await db.shops.count_documents({})
        
        return {
            "shops": shops,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        print(f"Error getting shops: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get shops"
        )

@router.get("/jobs")
async def get_all_jobs(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all jobs (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        jobs_cursor = db.jobs.find({}).skip(skip).limit(limit).sort([("created_at", -1)])
        jobs = await jobs_cursor.to_list(length=limit)
        
        for job in jobs:
            job["id"] = str(job["_id"])
            del job["_id"]
        
        total = await db.jobs.count_documents({})
        
        return {
            "jobs": jobs,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        print(f"Error getting jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get jobs"
        )

@router.get("/communities")
async def get_all_communities(
    skip: int = 0,
    limit: int = 100,
    current_user: dict = Depends(get_current_user)
):
    """Get all communities (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        communities_cursor = db.communities.find({}).skip(skip).limit(limit).sort([("created_at", -1)])
        communities = await communities_cursor.to_list(length=limit)
        
        for community in communities:
            community["id"] = str(community["_id"])
            del community["_id"]
        
        total = await db.communities.count_documents({})
        
        return {
            "communities": communities,
            "total": total,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        print(f"Error getting communities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get communities"
        )

# DELETE ENDPOINTS

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a user (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        from bson import ObjectId
        result = await db.users.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return {"message": "User deleted successfully", "deleted_id": user_id}
    except Exception as e:
        print(f"Error deleting user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user"
        )

@router.delete("/tournaments/{tournament_id}")
async def delete_tournament(tournament_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a tournament (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        from bson import ObjectId
        result = await db.tournaments.delete_one({"_id": ObjectId(tournament_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tournament not found"
            )
        
        return {"message": "Tournament deleted successfully", "deleted_id": tournament_id}
    except Exception as e:
        print(f"Error deleting tournament: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete tournament"
        )

@router.delete("/venues/{venue_id}")
async def delete_venue(venue_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a venue (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        from bson import ObjectId
        result = await db.venues.delete_one({"_id": ObjectId(venue_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Venue not found"
            )
        
        return {"message": "Venue deleted successfully", "deleted_id": venue_id}
    except Exception as e:
        print(f"Error deleting venue: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete venue"
        )

@router.delete("/shops/{shop_id}")
async def delete_shop(shop_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a shop (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        from bson import ObjectId
        result = await db.shops.delete_one({"_id": ObjectId(shop_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Shop not found"
            )
        
        return {"message": "Shop deleted successfully", "deleted_id": shop_id}
    except Exception as e:
        print(f"Error deleting shop: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete shop"
        )

@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a job (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        from bson import ObjectId
        result = await db.jobs.delete_one({"_id": ObjectId(job_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found"
            )
        
        return {"message": "Job deleted successfully", "deleted_id": job_id}
    except Exception as e:
        print(f"Error deleting job: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete job"
        )

@router.delete("/communities/{community_id}")
async def delete_community(community_id: str, current_user: dict = Depends(get_current_user)):
    """Delete a community (super admin only)"""
    
    if current_user.get("role") != "super_admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only super admins can access this endpoint"
        )
    
    db = get_database()
    
    try:
        from bson import ObjectId
        result = await db.communities.delete_one({"_id": ObjectId(community_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Community not found"
            )
        
        return {"message": "Community deleted successfully", "deleted_id": community_id}
    except Exception as e:
        print(f"Error deleting community: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete community"
        )
