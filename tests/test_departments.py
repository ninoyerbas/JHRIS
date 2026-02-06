"""
Tests for department endpoints.
"""
import pytest
from app.config import settings


def test_create_department(client, auth_headers):
    """Test creating a department."""
    department_data = {
        "name": "Human Resources",
        "code": "HR",
        "description": "Human Resources Department"
    }
    
    response = client.post(
        f"{settings.API_V1_PREFIX}/departments/",
        json=department_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Human Resources"
    assert data["code"] == "HR"
    assert "id" in data


def test_create_duplicate_department_code(client, auth_headers, db_session):
    """Test creating a department with duplicate code."""
    from app.departments.models import Department
    
    # Create first department
    dept = Department(name="IT", code="IT", description="IT Department")
    db_session.add(dept)
    db_session.commit()
    
    # Try to create another with same code
    department_data = {
        "name": "Information Technology",
        "code": "IT",
        "description": "Another IT Department"
    }
    
    response = client.post(
        f"{settings.API_V1_PREFIX}/departments/",
        json=department_data,
        headers=auth_headers
    )
    assert response.status_code == 400


def test_list_departments(client, auth_headers, db_session):
    """Test listing departments."""
    from app.departments.models import Department
    
    # Create some departments
    dept1 = Department(name="Sales", code="SALES", description="Sales Department")
    dept2 = Department(name="Marketing", code="MKT", description="Marketing Department")
    db_session.add_all([dept1, dept2])
    db_session.commit()
    
    response = client.get(
        f"{settings.API_V1_PREFIX}/departments/",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_department(client, auth_headers, db_session):
    """Test getting a department by ID."""
    from app.departments.models import Department
    
    department = Department(name="Finance", code="FIN", description="Finance Department")
    db_session.add(department)
    db_session.commit()
    db_session.refresh(department)
    
    response = client.get(
        f"{settings.API_V1_PREFIX}/departments/{department.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == department.id
    assert data["name"] == "Finance"


def test_update_department(client, auth_headers, db_session):
    """Test updating a department."""
    from app.departments.models import Department
    
    department = Department(name="Operations", code="OPS", description="Operations Department")
    db_session.add(department)
    db_session.commit()
    db_session.refresh(department)
    
    update_data = {"description": "Updated Operations Department"}
    response = client.put(
        f"{settings.API_V1_PREFIX}/departments/{department.id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Updated Operations Department"


def test_delete_department(client, auth_headers, db_session):
    """Test deleting a department."""
    from app.departments.models import Department
    
    department = Department(name="Legal", code="LEG", description="Legal Department")
    db_session.add(department)
    db_session.commit()
    db_session.refresh(department)
    
    response = client.delete(
        f"{settings.API_V1_PREFIX}/departments/{department.id}",
        headers=auth_headers
    )
    assert response.status_code == 204
