"""
Position API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user
from app.positions import schemas, service
from app.users.schemas import User

router = APIRouter(prefix="/positions", tags=["positions"])


@router.get("/", response_model=List[schemas.Position])
async def list_positions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all positions with pagination."""
    positions = service.PositionService.get_all(db, skip=skip, limit=limit)
    return positions


@router.post("/", response_model=schemas.Position, status_code=status.HTTP_201_CREATED)
async def create_position(
    position: schemas.PositionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new position."""
    return service.PositionService.create(db, position)


@router.get("/{position_id}", response_model=schemas.Position)
async def get_position(
    position_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get position by ID."""
    position = service.PositionService.get_by_id(db, position_id)
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position


@router.put("/{position_id}", response_model=schemas.Position)
async def update_position(
    position_id: int,
    position: schemas.PositionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a position."""
    updated_position = service.PositionService.update(db, position_id, position)
    if not updated_position:
        raise HTTPException(status_code=404, detail="Position not found")
    return updated_position


@router.delete("/{position_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_position(
    position_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a position."""
    success = service.PositionService.delete(db, position_id)
    if not success:
        raise HTTPException(status_code=404, detail="Position not found")
