"""
SQLAlchemy Department model.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Department(Base):
    """Department model."""
    
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    parent_department = relationship("Department", remote_side=[id], backref="subdepartments")
    manager = relationship("Employee", foreign_keys=[manager_id], backref="managed_departments")
    employees = relationship("Employee", foreign_keys="Employee.department_id", back_populates="department")
    positions = relationship("Position", back_populates="department")
