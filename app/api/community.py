from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import Optional
from datetime import datetime
from bson import ObjectId
import os
import uuid
import shutil

from app.core.database import get_database
from app.core.security import get_current_user

router = APIRouter(tags=["community"])

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads/community"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("")
async def get_communities(
    sport_type: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get all communities"""
    db = get_database()
    
    query = {"is_active": True}
    if sport_type:
        query["sport_type"] = sport_type
    
    communities_cursor = db.communities.find(query).skip(skip).limit(limit).sort([("members_count", -1)])
    communities = await communities_cursor.to_list(length=limit)
    
    for community in communities:
        community["id"] = str(community["_id"])
        del community["_id"]
    
    return communities


@router.get("/{community_id}")
async def get_community(community_id: str):
    """Get community details"""
    db = get_database()
    
    try:
        community = await db.communities.find_one({"_id": ObjectId(community_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid community ID")
    
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    community["id"] = str(community["_id"])
    del community["_id"]
    
    return community


@router.post("/{community_id}/join")
async def join_community(
    community_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Join a community"""
    db = get_database()
    
    try:
        community = await db.communities.find_one({"_id": ObjectId(community_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid community ID")
    
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    
    # Check if already a member
    existing_member = await db.community_members.find_one({
        "community_id": community_id,
        "user_id": str(current_user["_id"])
    })
    
    if existing_member:
        raise HTTPException(status_code=400, detail="Already a member of this community")
    
    # Add member
    member_dict = {
        "community_id": community_id,
        "user_id": str(current_user["_id"]),
        "user_name": current_user.get("name", "Anonymous"),
        "user_avatar": current_user.get("avatar"),
        "joined_at": datetime.utcnow(),
        "is_active": True
    }
    
    await db.community_members.insert_one(member_dict)
    
    # Update community members count
    await db.communities.update_one(
        {"_id": ObjectId(community_id)},
        {"$inc": {"members_count": 1}}
    )
    
    return {"message": "Successfully joined community"}


@router.post("/{community_id}/leave")
async def leave_community(
    community_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Leave a community"""
    db = get_database()
    
    result = await db.community_members.delete_one({
        "community_id": community_id,
        "user_id": str(current_user["_id"])
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not a member of this community")
    
    # Update community members count
    await db.communities.update_one(
        {"_id": ObjectId(community_id)},
        {"$inc": {"members_count": -1}}
    )
    
    return {"message": "Successfully left community"}


@router.get("/{community_id}/members")
async def get_community_members(
    community_id: str,
    skip: int = 0,
    limit: int = 50
):
    """Get community members"""
    db = get_database()
    
    members_cursor = db.community_members.find({
        "community_id": community_id,
        "is_active": True
    }).skip(skip).limit(limit).sort([("joined_at", -1)])
    
    members = await members_cursor.to_list(length=limit)
    
    for member in members:
        member["id"] = str(member["_id"])
        del member["_id"]
    
    return members


@router.get("/{community_id}/is-member")
async def check_membership(
    community_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Check if user is a member of community"""
    db = get_database()
    
    member = await db.community_members.find_one({
        "community_id": community_id,
        "user_id": str(current_user["_id"]),
        "is_active": True
    })
    
    return {"is_member": member is not None}


@router.post("/{community_id}/posts")
async def create_post(
    community_id: str,
    content: str,
    media_type: Optional[str] = None,
    media_url: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Create a post in community (text, image, or video link)"""
    db = get_database()
    
    # Validate content length (140 characters for text)
    if len(content) > 140:
        raise HTTPException(status_code=400, detail="Content must be 140 characters or less")
    
    # Check if user is a member
    member = await db.community_members.find_one({
        "community_id": community_id,
        "user_id": str(current_user["_id"]),
        "is_active": True
    })
    
    if not member:
        raise HTTPException(status_code=403, detail="Must be a member to post")
    
    # Validate media type
    if media_type and media_type not in ["image", "video"]:
        raise HTTPException(status_code=400, detail="Media type must be 'image' or 'video'")
    
    post_dict = {
        "community_id": community_id,
        "user_id": str(current_user["_id"]),
        "user_name": current_user.get("name", "Anonymous"),
        "user_avatar": current_user.get("avatar"),
        "content": content,
        "media_type": media_type,
        "media_url": media_url,
        "likes_count": 0,
        "comments_count": 0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True
    }
    
    result = await db.community_posts.insert_one(post_dict)
    
    # Update community posts count
    await db.communities.update_one(
        {"_id": ObjectId(community_id)},
        {"$inc": {"posts_count": 1}}
    )
    
    # Return the created post with proper date formatting
    created_post = await db.community_posts.find_one({"_id": result.inserted_id})
    if created_post:
        created_post["id"] = str(created_post["_id"])
        del created_post["_id"]
        
        # Convert datetime to ISO string
        if "created_at" in created_post and created_post["created_at"]:
            created_post["created_at"] = created_post["created_at"].isoformat() + "Z"
        if "updated_at" in created_post and created_post["updated_at"]:
            created_post["updated_at"] = created_post["updated_at"].isoformat() + "Z"
        
        return created_post
    
    return {"message": "Post created successfully", "post_id": str(result.inserted_id)}


@router.get("/{community_id}/posts")
async def get_community_posts(
    community_id: str,
    skip: int = 0,
    limit: int = 20
):
    """Get community posts (sorted oldest to newest for chat)"""
    db = get_database()
    
    posts_cursor = db.community_posts.find({
        "community_id": community_id,
        "is_active": True
    }).skip(skip).limit(limit).sort([("created_at", 1)])
    
    posts = await posts_cursor.to_list(length=limit)
    
    for post in posts:
        post["id"] = str(post["_id"])
        del post["_id"]
        
        # Convert datetime objects to ISO string format for frontend
        if "created_at" in post and post["created_at"]:
            post["created_at"] = post["created_at"].isoformat() + "Z" if hasattr(post["created_at"], 'isoformat') else post["created_at"]
        if "updated_at" in post and post["updated_at"]:
            post["updated_at"] = post["updated_at"].isoformat() + "Z" if hasattr(post["updated_at"], 'isoformat') else post["updated_at"]
    
    return posts


@router.post("/{community_id}/upload-image")
async def upload_community_image(
    community_id: str,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload an image for community chat (max 10MB)"""
    db = get_database()
    
    # Check if user is a member
    member = await db.community_members.find_one({
        "community_id": community_id,
        "user_id": str(current_user["_id"]),
        "is_active": True
    })
    
    if not member:
        raise HTTPException(status_code=403, detail="Must be a member to upload images")
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/gif", "image/webp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed: {', '.join(allowed_types)}"
        )
    
    # Validate file size (10MB = 10 * 1024 * 1024 bytes)
    MAX_SIZE = 10 * 1024 * 1024
    file_size = 0
    
    # Read file content to check size
    contents = await file.read()
    file_size = len(contents)
    
    if file_size > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size is 10MB. Your file is {file_size / (1024 * 1024):.2f}MB"
        )
    
    # Reset file pointer
    await file.seek(0)
    
    # Generate unique filename
    file_extension = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    unique_filename = f"{uuid.uuid4()}.{file_extension}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")
    
    # Return file URL
    file_url = f"/uploads/community/{unique_filename}"
    
    return {
        "url": file_url,
        "filename": unique_filename,
        "size": file_size,
        "content_type": file.content_type
    }

