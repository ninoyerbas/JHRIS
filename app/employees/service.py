"""
Employee service layer for business logic.
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.employees import models, schemas


class EmployeeService:
    """Service class for employee operations."""
    
    @staticmethod
    def get_by_id(db: Session, employee_id: int) -> Optional[models.Employee]:
        """Get employee by ID."""
        return db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    
    @staticmethod
    def get_by_employee_number(db: Session, employee_number: str) -> Optional[models.Employee]:
        """Get employee by employee number."""
        return db.query(models.Employee).filter(
            models.Employee.employee_number == employee_number
        ).first()
    
    @staticmethod
    def get_all(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        department_id: Optional[int] = None,
        employment_status: Optional[str] = None
    ) -> List[models.Employee]:
        """Get all employees with pagination and filtering."""
        query = db.query(models.Employee)
        
        if department_id:
            query = query.filter(models.Employee.department_id == department_id)
        
        if employment_status:
            query = query.filter(models.Employee.employment_status == employment_status)
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_subordinates(db: Session, manager_id: int) -> List[models.Employee]:
        """Get direct reports for a manager."""
        return db.query(models.Employee).filter(
            models.Employee.manager_id == manager_id
        ).all()
    
    @staticmethod
    def create(db: Session, employee: schemas.EmployeeCreate) -> models.Employee:
        """Create a new employee."""
        # Check if employee number already exists
        existing = EmployeeService.get_by_employee_number(db, employee.employee_number)
        if existing:
            raise HTTPException(status_code=400, detail="Employee number already exists")
        
        db_employee = models.Employee(**employee.model_dump())
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def update(
        db: Session,
        employee_id: int,
        employee: schemas.EmployeeUpdate
    ) -> Optional[models.Employee]:
        """Update an employee."""
        db_employee = EmployeeService.get_by_id(db, employee_id)
        if not db_employee:
            return None
        
        update_data = employee.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_employee, field, value)
        
        db.commit()
        db.refresh(db_employee)
        return db_employee
    
    @staticmethod
    def delete(db: Session, employee_id: int) -> bool:
        """Delete an employee."""
        db_employee = EmployeeService.get_by_id(db, employee_id)
        if not db_employee:
            return False
        
        db.delete(db_employee)
        db.commit()
        return True
