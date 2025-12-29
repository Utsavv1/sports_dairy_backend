from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from datetime import datetime
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Tournament, Team, TournamentRegistration, User
from app.schemas.schemas import (
    TournamentCreate, TournamentUpdate, TournamentResponse,
    TeamCreate, TeamUpdate, TeamResponse,
    TournamentRegistrationCreate, TournamentRegistrationUpdate, TournamentRegistrationResponse
)

router = APIRouter(prefix="/tournaments", tags=["tournaments"])


# ==================== TOURNAMENT ENDPOINTS ====================

@router.get("", response_model=List[TournamentResponse])
async def get_tournaments(
    city: Optional[str] = None,
    sport_type: Optional[str] = None,
    status: Optional[str] = None,
    age_category: Optional[str] = None,
    gender_category: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get list of tournaments with filters"""
    query = select(Tournament).where(Tournament.is_active == True)
    
    if city:
        query = query.where(Tournament.city == city)
    if sport_type:
        query = query.where(Tournament.sport_type == sport_type)
    if status:
        query = query.where(Tournament.status == status)
    if age_category:
        query = query.where(Tournament.age_category == age_category)
    if gender_category:
        query = query.where(Tournament.gender_category == gender_category)
    if search:
        query = query.where(
            (Tournament.name.ilike(f"%{search}%")) |
            (Tournament.description.ilike(f"%{search}%"))
        )
    
    # Order by featured first, then by start date
    query = query.order_by(Tournament.is_featured.desc(), Tournament.start_date.asc())
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    tournaments = result.scalars().all()
    return tournaments


@router.get("/{tournament_id}", response_model=TournamentResponse)
async def get_tournament(tournament_id: int, db: AsyncSession = Depends(get_db)):
    """Get tournament details"""
    result = await db.execute(select(Tournament).where(Tournament.id == tournament_id))
    tournament = result.scalar_one_or_none()
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    # Increment views count
    tournament.views_count += 1
    await db.commit()
    
    return tournament


@router.post("", response_model=TournamentResponse)
async def create_tournament(
    tournament_data: TournamentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new tournament"""
    new_tournament = Tournament(
        **tournament_data.model_dump(),
        organizer_id=current_user.id
    )
    
    db.add(new_tournament)
    await db.commit()
    await db.refresh(new_tournament)
    return new_tournament


@router.put("/{tournament_id}", response_model=TournamentResponse)
async def update_tournament(
    tournament_id: int,
    tournament_data: TournamentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update tournament details"""
    result = await db.execute(select(Tournament).where(Tournament.id == tournament_id))
    tournament = result.scalar_one_or_none()
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    if tournament.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    for field, value in tournament_data.model_dump(exclude_unset=True).items():
        setattr(tournament, field, value)
    
    await db.commit()
    await db.refresh(tournament)
    return tournament


@router.delete("/{tournament_id}")
async def delete_tournament(
    tournament_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete/deactivate tournament"""
    result = await db.execute(select(Tournament).where(Tournament.id == tournament_id))
    tournament = result.scalar_one_or_none()
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    if tournament.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    tournament.is_active = False
    await db.commit()
    
    return {"message": "Tournament deleted successfully"}


# ==================== TEAM ENDPOINTS ====================

@router.get("/teams/list", response_model=List[TeamResponse])
async def get_teams(
    city: Optional[str] = None,
    sport_type: Optional[str] = None,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db)
):
    """Get list of teams"""
    query = select(Team).where(Team.is_active == True)
    
    if city:
        query = query.where(Team.city == city)
    if sport_type:
        query = query.where(Team.sport_type == sport_type)
    if search:
        query = query.where(
            (Team.name.ilike(f"%{search}%")) |
            (Team.description.ilike(f"%{search}%"))
        )
    
    query = query.order_by(Team.created_at.desc())
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    teams = result.scalars().all()
    return teams


@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    """Get team details"""
    result = await db.execute(select(Team).where(Team.id == team_id))
    team = result.scalar_one_or_none()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    return team


@router.post("/teams", response_model=TeamResponse)
async def create_team(
    team_data: TeamCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new team"""
    new_team = Team(
        **team_data.model_dump(),
        captain_id=current_user.id,
        total_players=len(team_data.players) if team_data.players else 0
    )
    
    db.add(new_team)
    await db.commit()
    await db.refresh(new_team)
    return new_team


@router.put("/teams/{team_id}", response_model=TeamResponse)
async def update_team(
    team_id: int,
    team_data: TeamUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update team details"""
    result = await db.execute(select(Team).where(Team.id == team_id))
    team = result.scalar_one_or_none()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    if team.captain_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    for field, value in team_data.model_dump(exclude_unset=True).items():
        setattr(team, field, value)
    
    # Update total_players if players list is updated
    if team_data.players is not None:
        team.total_players = len(team_data.players)
    
    await db.commit()
    await db.refresh(team)
    return team


@router.get("/teams/my-teams/list", response_model=List[TeamResponse])
async def get_my_teams(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get teams where current user is captain"""
    result = await db.execute(
        select(Team).where(Team.captain_id == current_user.id, Team.is_active == True)
    )
    teams = result.scalars().all()
    return teams


# ==================== TOURNAMENT REGISTRATION ENDPOINTS ====================

@router.post("/{tournament_id}/register", response_model=TournamentRegistrationResponse)
async def register_team(
    tournament_id: int,
    registration_data: TournamentRegistrationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Register a team for a tournament"""
    # Verify tournament exists
    tournament_result = await db.execute(select(Tournament).where(Tournament.id == tournament_id))
    tournament = tournament_result.scalar_one_or_none()
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    # Check registration deadline
    if datetime.utcnow() > tournament.registration_deadline:
        raise HTTPException(status_code=400, detail="Registration deadline has passed")
    
    # Check if tournament is full
    if tournament.current_teams >= tournament.max_teams:
        raise HTTPException(status_code=400, detail="Tournament is full")
    
    # Verify team exists and user is captain
    team_result = await db.execute(select(Team).where(Team.id == registration_data.team_id))
    team = team_result.scalar_one_or_none()
    
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    
    if team.captain_id != current_user.id:
        raise HTTPException(status_code=403, detail="Only team captain can register")
    
    # Check if team is already registered
    existing_reg = await db.execute(
        select(TournamentRegistration).where(
            TournamentRegistration.tournament_id == tournament_id,
            TournamentRegistration.team_id == registration_data.team_id
        )
    )
    if existing_reg.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Team already registered for this tournament")
    
    # Generate registration number
    reg_number = f"REG-TOUR{tournament_id:03d}-TEAM{registration_data.team_id:03d}"
    
    # Create registration
    new_registration = TournamentRegistration(
        **registration_data.model_dump(),
        registration_number=reg_number,
        registered_by=current_user.id,
        entry_fee=tournament.entry_fee
    )
    
    db.add(new_registration)
    
    # Update tournament team count
    tournament.current_teams += 1
    
    await db.commit()
    await db.refresh(new_registration)
    return new_registration


@router.get("/{tournament_id}/registrations", response_model=List[TournamentRegistrationResponse])
async def get_tournament_registrations(
    tournament_id: int,
    status: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all registrations for a tournament"""
    # Verify tournament exists and user is organizer
    tournament_result = await db.execute(select(Tournament).where(Tournament.id == tournament_id))
    tournament = tournament_result.scalar_one_or_none()
    
    if not tournament:
        raise HTTPException(status_code=404, detail="Tournament not found")
    
    query = select(TournamentRegistration).where(TournamentRegistration.tournament_id == tournament_id)
    
    if status:
        query = query.where(TournamentRegistration.status == status)
    
    result = await db.execute(query)
    registrations = result.scalars().all()
    return registrations


@router.put("/registrations/{registration_id}", response_model=TournamentRegistrationResponse)
async def update_registration(
    registration_id: int,
    registration_data: TournamentRegistrationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update registration status (organizer only)"""
    result = await db.execute(select(TournamentRegistration).where(TournamentRegistration.id == registration_id))
    registration = result.scalar_one_or_none()
    
    if not registration:
        raise HTTPException(status_code=404, detail="Registration not found")
    
    # Verify user is tournament organizer
    tournament_result = await db.execute(select(Tournament).where(Tournament.id == registration.tournament_id))
    tournament = tournament_result.scalar_one_or_none()
    
    if tournament.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    # Update fields
    for field, value in registration_data.model_dump(exclude_unset=True).items():
        setattr(registration, field, value)
    
    if registration_data.status == "approved":
        registration.approval_date = datetime.utcnow()
        registration.approved_by = current_user.id
    
    await db.commit()
    await db.refresh(registration)
    return registration


@router.get("/registrations/my-registrations/list", response_model=List[TournamentRegistrationResponse])
async def get_my_registrations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's tournament registrations"""
    result = await db.execute(
        select(TournamentRegistration).where(TournamentRegistration.registered_by == current_user.id)
    )
    registrations = result.scalars().all()
    return registrations

