"""
Pydantic schemas for Position model.
"""
from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict


class PositionBase(BaseModel):
    """Base position schema."""
    title: str
    code: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None


class PositionCreate(PositionBase):
    """Schema for creating a position."""
    pass


class PositionUpdate(BaseModel):
    """Schema for updating a position."""
    title: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    department_id: Optional[int] = None
    min_salary: Optional[Decimal] = None
    max_salary: Optional[Decimal] = None


class Position(PositionBase):
    """Schema for position response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
