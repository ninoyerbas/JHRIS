"""
Position service layer for business logic.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.positions import models, schemas


class PositionService:
    """Service class for position operations."""
    
    @staticmethod
    def get_by_id(db: Session, position_id: int) -> Optional[models.Position]:
        """Get position by ID."""
        return db.query(models.Position).filter(models.Position.id == position_id).first()
    
    @staticmethod
    def get_by_code(db: Session, code: str) -> Optional[models.Position]:
        """Get position by code."""
        return db.query(models.Position).filter(models.Position.code == code).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.Position]:
        """Get all positions with pagination."""
        return db.query(models.Position).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, position: schemas.PositionCreate) -> models.Position:
        """Create a new position."""
        # Check if code already exists
        existing = PositionService.get_by_code(db, position.code)
        if existing:
            raise HTTPException(status_code=400, detail="Position code already exists")
        
        db_position = models.Position(**position.model_dump())
        db.add(db_position)
        db.commit()
        db.refresh(db_position)
        return db_position
    
    @staticmethod
    def update(
        db: Session,
        position_id: int,
        position: schemas.PositionUpdate
    ) -> Optional[models.Position]:
        """Update a position."""
        db_position = PositionService.get_by_id(db, position_id)
        if not db_position:
            return None
        
        update_data = position.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_position, field, value)
        
        db.commit()
        db.refresh(db_position)
        return db_position
    
    @staticmethod
    def delete(db: Session, position_id: int) -> bool:
        """Delete a position."""
        db_position = PositionService.get_by_id(db, position_id)
        if not db_position:
            return False
        
        db.delete(db_position)
        db.commit()
        return True
