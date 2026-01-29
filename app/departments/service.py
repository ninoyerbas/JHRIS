"""
Department service layer for business logic.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.departments import models, schemas


class DepartmentService:
    """Service class for department operations."""
    
    @staticmethod
    def get_by_id(db: Session, department_id: int) -> Optional[models.Department]:
        """Get department by ID."""
        return db.query(models.Department).filter(models.Department.id == department_id).first()
    
    @staticmethod
    def get_by_code(db: Session, code: str) -> Optional[models.Department]:
        """Get department by code."""
        return db.query(models.Department).filter(models.Department.code == code).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100) -> List[models.Department]:
        """Get all departments with pagination."""
        return db.query(models.Department).offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, department: schemas.DepartmentCreate) -> models.Department:
        """Create a new department."""
        # Check if code already exists
        existing = DepartmentService.get_by_code(db, department.code)
        if existing:
            raise HTTPException(status_code=400, detail="Department code already exists")
        
        db_department = models.Department(**department.model_dump())
        db.add(db_department)
        db.commit()
        db.refresh(db_department)
        return db_department
    
    @staticmethod
    def update(
        db: Session,
        department_id: int,
        department: schemas.DepartmentUpdate
    ) -> Optional[models.Department]:
        """Update a department."""
        db_department = DepartmentService.get_by_id(db, department_id)
        if not db_department:
            return None
        
        update_data = department.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_department, field, value)
        
        db.commit()
        db.refresh(db_department)
        return db_department
    
    @staticmethod
    def delete(db: Session, department_id: int) -> bool:
        """Delete a department."""
        db_department = DepartmentService.get_by_id(db, department_id)
        if not db_department:
            return False
        
        db.delete(db_department)
        db.commit()
        return True
