"""
SQLAlchemy Employee model.
"""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class EmploymentStatus(str, enum.Enum):
    """Employment status enum."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    TERMINATED = "terminated"
    ON_LEAVE = "on_leave"


class EmploymentType(str, enum.Enum):
    """Employment type enum."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERN = "intern"


class Gender(str, enum.Enum):
    """Gender enum."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class MaritalStatus(str, enum.Enum):
    """Marital status enum."""
    SINGLE = "single"
    MARRIED = "married"
    DIVORCED = "divorced"
    WIDOWED = "widowed"


class Employee(Base):
    """Employee model."""
    
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    employee_number = Column(String(50), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    gender = Column(SQLEnum(Gender), nullable=True)
    marital_status = Column(SQLEnum(MaritalStatus), nullable=True)
    nationality = Column(String(100), nullable=True)
    
    # Contact Information
    email = Column(String(255), nullable=False)
    personal_email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Address
    address = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    postal_code = Column(String(20), nullable=True)
    country = Column(String(100), nullable=True)
    
    # Employment Information
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=True)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    hire_date = Column(Date, nullable=False)
    employment_status = Column(SQLEnum(EmploymentStatus), nullable=False, default=EmploymentStatus.ACTIVE)
    employment_type = Column(SQLEnum(EmploymentType), nullable=False, default=EmploymentType.FULL_TIME)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = relationship("User", backref="employee")
    department = relationship("Department", foreign_keys=[department_id], back_populates="employees")
    position = relationship("Position", back_populates="employees")
    manager = relationship("Employee", remote_side=[id], backref="subordinates")
