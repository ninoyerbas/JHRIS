"""
Department API routes.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user
from app.departments import schemas, service
from app.users.schemas import User

router = APIRouter(prefix="/departments", tags=["departments"])


@router.get("/", response_model=List[schemas.Department])
async def list_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """List all departments with pagination."""
    departments = service.DepartmentService.get_all(db, skip=skip, limit=limit)
    return departments


@router.post("/", response_model=schemas.Department, status_code=status.HTTP_201_CREATED)
async def create_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new department."""
    return service.DepartmentService.create(db, department)


@router.get("/{department_id}", response_model=schemas.Department)
async def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get department by ID."""
    department = service.DepartmentService.get_by_id(db, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department


@router.put("/{department_id}", response_model=schemas.Department)
async def update_department(
    department_id: int,
    department: schemas.DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update a department."""
    updated_department = service.DepartmentService.update(db, department_id, department)
    if not updated_department:
        raise HTTPException(status_code=404, detail="Department not found")
    return updated_department


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete a department."""
    success = service.DepartmentService.delete(db, department_id)
    if not success:
        raise HTTPException(status_code=404, detail="Department not found")
