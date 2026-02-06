"""
Pydantic schemas for Employee model.
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum


class EmploymentStatus(str, Enum):
    """Employment status enum."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"


class EmploymentType(str, Enum):
    """Employment type enum."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"


class Gender(str, Enum):
    """Gender enum."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class MaritalStatus(str, Enum):
    """Marital status enum."""
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class EmployeeBase(BaseModel):
    """Base employee schema."""
    employee_number: str
    user_id: Optional[int] = None
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    nationality: Optional[str] = None
    email: EmailStr
    personal_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    hire_date: date
    employment_status: EmploymentStatus = EmploymentStatus.ACTIVE
    employment_type: EmploymentType = EmploymentType.FULL_TIME


class EmployeeCreate(EmployeeBase):
    """Schema for creating an employee."""
    pass


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee."""
    employee_number: Optional[str] = None
    user_id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[Gender] = None
    marital_status: Optional[MaritalStatus] = None
    nationality: Optional[str] = None
    email: Optional[EmailStr] = None
    personal_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    department_id: Optional[int] = None
    position_id: Optional[int] = None
    manager_id: Optional[int] = None
    hire_date: Optional[date] = None
    employment_status: Optional[EmploymentStatus] = None
    employment_type: Optional[EmploymentType] = None


class Employee(EmployeeBase):
    """Schema for employee response."""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
