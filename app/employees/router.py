"""
Employee API routes.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_active_user
from app.employees import schemas, service
from app.users.schemas import User

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[schemas.Employee])
async def list_employees(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    department_id: Optional[int] = Query(None),
    employment_status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """
    List all employees with pagination and filtering.
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        department_id: Filter by department ID
        employment_status: Filter by employment status
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        List of employees
    """
    employees = service.EmployeeService.get_all(
        db,
        skip=skip,
        limit=limit,
        department_id=department_id,
        employment_status=employment_status
    )
    return employees


@router.post("/", response_model=schemas.Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Create a new employee."""
    return service.EmployeeService.create(db, employee)


@router.get("/{employee_id}", response_model=schemas.Employee)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get employee by ID."""
    employee = service.EmployeeService.get_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@router.put("/{employee_id}", response_model=schemas.Employee)
async def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Update an employee."""
    updated_employee = service.EmployeeService.update(db, employee_id, employee)
    if not updated_employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return updated_employee


@router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Delete an employee."""
    success = service.EmployeeService.delete(db, employee_id)
    if not success:
        raise HTTPException(status_code=404, detail="Employee not found")


@router.get("/{employee_id}/subordinates", response_model=List[schemas.Employee])
async def get_employee_subordinates(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """Get direct reports for an employee (manager)."""
    # First check if employee exists
    employee = service.EmployeeService.get_by_id(db, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    subordinates = service.EmployeeService.get_subordinates(db, employee_id)
    return subordinates
