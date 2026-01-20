from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from datetime import datetime
from bson import ObjectId

from app.core.database import get_database
from app.core.security import get_current_user
from app.schemas.schemas import (
    TournamentCreate, TournamentUpdate, TournamentResponse,
    TeamCreate, TeamUpdate, TeamResponse,
    TournamentRegistrationCreate, TournamentRegistrationUpdate, TournamentRegistrationResponse
)

router = APIRouter(tags=["tournaments"])


# ==================== TOURNAMENT ENDPOINTS ====================

@router.get("")
async def get_tournaments(
    city: Optional[str] = None,
    sport_type: Optional[str] = None,
    status: Optional[str] = None,
    age_category: Optional[str] = None,
    gender_category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50
):
    """Get list of tournaments with filters"""
    db = get_database()
    
    query = {"is_active": True}
    
    if city:
        query["city"] = city
    if sport_type:
        query["sport_type"] = sport_type
    if status:
        query["status"] = status
    if age_category:
        query["age_category"] = age_category
    if gender_category:
        query["gender_category"] = gender_category
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}}
        ]
    
    # Get total count before limiting
    total_count = await db.tournaments.count_documents(query)
    
    tournaments_cursor = db.tournaments.find(query).skip(skip).limit(limit).sort([("is_featured", -1), ("start_date", 1)])
    tournaments = await tournaments_cursor.to_list(length=limit)
    
    for tournament in tournaments:
        tournament["id"] = str(tournament["_id"])
        del tournament["_id"]  # Remove ObjectId
    
    return {"tournaments": tournaments, "count": total_count}


@router.get("/{tournament_id}")
async def get_tournament(tournament_id: str):
    """Get tournament details"""
    db = get_database()
    
    try:
        tournament = await db.tournaments.find_one({"_id": ObjectId(tournament_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid tournament ID")
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    # Increment views count
    await db.tournaments.update_one(
        {"_id": ObjectId(tournament_id)},
        {"$inc": {"views_count": 1}}
    )
    
    tournament["id"] = str(tournament["_id"])
    
    # Fetch organizer details
    organizer_id = tournament.get("organizer_id")
    if organizer_id:
        try:
            organizer = await db.users.find_one({"_id": ObjectId(organizer_id)})
            if organizer:
                tournament["organizer"] = {
                    "id": str(organizer["_id"]),
                    "name": organizer.get("name", "Anonymous"),
                    "role": organizer.get("role"),
                    "professional_type": organizer.get("professional_type"),
                    "city": organizer.get("city"),
                    "state": organizer.get("state"),
                    "bio": organizer.get("bio"),
                    "avatar": organizer.get("avatar"),
                    "is_verified": organizer.get("is_verified", False)
                }
        except:
            # If organizer fetch fails, just continue without organizer data
            pass
    
    del tournament["_id"]  # Remove ObjectId
    return tournament


@router.post("")
async def create_tournament(
    tournament_data: TournamentCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create new tournament (organizers and their managers)"""
    db = get_database()
    
    user_id = str(current_user["_id"])
    organizer_id = user_id
    created_by_manager = False
    
    # Check if user is organizer or manager with permission
    if current_user.get("role") != "organizer":
        # Check if user is a manager
        manager = await db.organizer_managers.find_one({
            "manager_user_id": user_id,
            "is_active": True
        })
        
        if not manager:
            raise HTTPException(status_code=403, detail="Only organizers or their managers can create tournaments")
        
        # Check permission
        permissions = manager.get("permissions", [])
        if "create_tournament" not in permissions:
            raise HTTPException(status_code=403, detail="You don't have permission to create tournaments")
        
        organizer_id = str(manager["organizer_id"])
        created_by_manager = True
    
    tournament_dict = tournament_data.dict()
    tournament_dict["organizer_id"] = organizer_id
    tournament_dict["created_by"] = user_id
    tournament_dict["created_by_manager"] = created_by_manager
    tournament_dict["created_at"] = datetime.utcnow()
    tournament_dict["updated_at"] = datetime.utcnow()
    tournament_dict["current_teams"] = 0
    tournament_dict["views_count"] = 0
    tournament_dict["is_active"] = True
    tournament_dict["status"] = "upcoming"
    
    result = await db.tournaments.insert_one(tournament_dict)
    created_tournament = await db.tournaments.find_one({"_id": result.inserted_id})
    created_tournament["id"] = str(created_tournament["_id"])

    del created_tournament["_id"]  # Remove ObjectId
    
    return created_tournament


@router.put("/{tournament_id}")
async def update_tournament(
    tournament_id: str,
    tournament_data: TournamentUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update tournament (organizers and their managers)"""
    db = get_database()
    
    try:
        tournament = await db.tournaments.find_one({"_id": ObjectId(tournament_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid tournament ID")
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    user_id = str(current_user["_id"])
    
    # Check if user is the organizer
    if str(tournament["organizer_id"]) == user_id:
        # Organizer has full access
        pass
    else:
        # Check if user is a manager with permission
        manager = await db.organizer_managers.find_one({
            "manager_user_id": user_id,
            "organizer_id": str(tournament["organizer_id"]),
            "is_active": True
        })
        
        if not manager:
            raise HTTPException(status_code=403, detail="Not authorized to edit this tournament")
        
        # Check permission
        permissions = manager.get("permissions", [])
        if "edit_tournament" not in permissions:
            raise HTTPException(status_code=403, detail="You don't have permission to edit tournaments")
    
    update_data = {k: v for k, v in tournament_data.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    await db.tournaments.update_one(
        {"_id": ObjectId(tournament_id)},
        {"$set": update_data}
    )
    
    updated_tournament = await db.tournaments.find_one({"_id": ObjectId(tournament_id)})
    updated_tournament["id"] = str(updated_tournament["_id"])

    del updated_tournament["_id"]  # Remove ObjectId
    
    return updated_tournament


@router.delete("/{tournament_id}")
async def delete_tournament(
    tournament_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete/deactivate tournament (organizers and their managers)"""
    db = get_database()
    
    try:
        tournament = await db.tournaments.find_one({"_id": ObjectId(tournament_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid tournament ID")
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    user_id = str(current_user["_id"])
    
    # Check if user is the organizer
    if str(tournament["organizer_id"]) == user_id:
        # Organizer has full access
        pass
    else:
        # Check if user is a manager with permission
        manager = await db.organizer_managers.find_one({
            "manager_user_id": user_id,
            "organizer_id": str(tournament["organizer_id"]),
            "is_active": True
        })
        
        if not manager:
            raise HTTPException(status_code=403, detail="Not authorized to delete this tournament")
        
        # Check permission
        permissions = manager.get("permissions", [])
        if "edit_tournament" not in permissions:  # Using edit permission for delete
            raise HTTPException(status_code=403, detail="You don't have permission to delete tournaments")
    
    # Soft delete
    await db.tournaments.update_one(
        {"_id": ObjectId(tournament_id)},
        {"$set": {"is_active": False, "updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Tournament deleted successfully"}


# ==================== TEAM ENDPOINTS ====================

@router.post("/teams")
async def create_team(
    team_data: TeamCreate,
    current_user: dict = Depends(get_current_user)
):
    """Create new team"""
    db = get_database()
    
    team_dict = team_data.dict()
    team_dict["captain_id"] = str(current_user["_id"])
    team_dict["created_at"] = datetime.utcnow()
    team_dict["updated_at"] = datetime.utcnow()
    team_dict["total_players"] = len(team_dict.get("players", []))
    team_dict["is_active"] = True
    team_dict["is_verified"] = False
    
    result = await db.teams.insert_one(team_dict)
    created_team = await db.teams.find_one({"_id": result.inserted_id})
    created_team["id"] = str(created_team["_id"])

    del created_team["_id"]  # Remove ObjectId
    
    return created_team


@router.get("/teams")
async def get_user_teams(
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 50
):
    """Get user's teams"""
    db = get_database()
    
    teams_cursor = db.teams.find({"captain_id": str(current_user["_id"])}).skip(skip).limit(limit)
    teams = await teams_cursor.to_list(length=limit)
    
    for team in teams:
        team["id"] = str(team["_id"])

        del team["_id"]  # Remove ObjectId
    
    return teams


@router.get("/teams/{team_id}")
async def get_team(team_id: str):
    """Get team details"""
    db = get_database()
    
    try:
        team = await db.teams.find_one({"_id": ObjectId(team_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid team ID")
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    team["id"] = str(team["_id"])

    
    del team["_id"]  # Remove ObjectId
    return team


@router.put("/teams/{team_id}")
async def update_team(
    team_id: str,
    team_data: TeamUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update team"""
    db = get_database()
    
    try:
        team = await db.teams.find_one({"_id": ObjectId(team_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid team ID")
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is captain
    if str(team["captain_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Not authorized")
    
    update_data = {k: v for k, v in team_data.dict(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    # Update total_players if players list is updated
    if "players" in update_data:
        update_data["total_players"] = len(update_data["players"])
    
    await db.teams.update_one(
        {"_id": ObjectId(team_id)},
        {"$set": update_data}
    )
    
    updated_team = await db.teams.find_one({"_id": ObjectId(team_id)})
    updated_team["id"] = str(updated_team["_id"])

    del updated_team["_id"]  # Remove ObjectId
    
    return updated_team


# ==================== TOURNAMENT REGISTRATION ENDPOINTS ====================

@router.post("/{tournament_id}/register")
async def register_team(
    tournament_id: str,
    registration_data: TournamentRegistrationCreate,
    current_user: dict = Depends(get_current_user)
):
    """Register team for tournament"""
    db = get_database()
    
    # Verify tournament exists
    try:
        tournament = await db.tournaments.find_one({"_id": ObjectId(tournament_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid tournament ID")
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    # Check if tournament is accepting registrations
    if tournament["current_teams"] >= tournament["max_teams"]:
        raise HTTPException(status_code=400, detail="Tournament is full")
    
    # Verify team exists
    try:
        team = await db.teams.find_one({"_id": ObjectId(registration_data.team_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid team ID")
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    # Check if user is team captain
    if str(team["captain_id"]) != str(current_user["_id"]):
        raise HTTPException(status_code=403, detail="Only team captain can register")
    
    # Check if team already registered
    existing_registration = await db.tournament_registrations.find_one({
        "tournament_id": tournament_id,
        "team_id": registration_data.team_id
    })
    
    if existing_registration:
        raise HTTPException(status_code=400, detail="Team already registered for this tournament")
    
    # Generate registration number
    reg_count = await db.tournament_registrations.count_documents({})
    registration_number = f"REG-TOUR{tournament_id[-3:]}-TEAM{reg_count + 1:04d}"
    
    registration_dict = registration_data.dict()
    registration_dict["tournament_id"] = tournament_id
    registration_dict["registered_by"] = str(current_user["_id"])
    registration_dict["registration_number"] = registration_number
    registration_dict["registration_date"] = datetime.utcnow()
    registration_dict["created_at"] = datetime.utcnow()
    registration_dict["updated_at"] = datetime.utcnow()
    registration_dict["status"] = "pending"
    registration_dict["payment_status"] = "pending"
    
    result = await db.tournament_registrations.insert_one(registration_dict)
    
    # Increment tournament's current_teams count
    await db.tournaments.update_one(
        {"_id": ObjectId(tournament_id)},
        {"$inc": {"current_teams": 1}}
    )
    
    created_registration = await db.tournament_registrations.find_one({"_id": result.inserted_id})
    created_registration["id"] = str(created_registration["_id"])

    del created_registration["_id"]  # Remove ObjectId
    
    return created_registration


@router.get("/{tournament_id}/registrations")
async def get_tournament_registrations(
    tournament_id: str,
    skip: int = 0,
    limit: int = 50
):
    """Get tournament registrations"""
    db = get_database()
    
    registrations_cursor = db.tournament_registrations.find({"tournament_id": tournament_id}).skip(skip).limit(limit)
    registrations = await registrations_cursor.to_list(length=limit)
    
    for registration in registrations:
        registration["id"] = str(registration["_id"])

        del registration["_id"]  # Remove ObjectId
    
    return registrations


@router.get("/registrations/{registration_id}")
async def get_registration(
    registration_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get registration details"""
    db = get_database()
    
    try:
        registration = await db.tournament_registrations.find_one({"_id": ObjectId(registration_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid registration ID")
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    registration["id"] = str(registration["_id"])

    
    del registration["_id"]  # Remove ObjectId
    return registration

