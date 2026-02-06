"""
Tests for employee endpoints.
"""
import pytest
from datetime import date
from app.config import settings


@pytest.fixture
def test_department(db_session):
    """Create a test department."""
    from app.departments.models import Department
    
    department = Department(
        name="Engineering",
        code="ENG",
        description="Engineering Department"
    )
    db_session.add(department)
    db_session.commit()
    db_session.refresh(department)
    return department


@pytest.fixture
def test_position(db_session, test_department):
    """Create a test position."""
    from app.positions.models import Position
    
    position = Position(
        title="Software Engineer",
        code="SE",
        description="Software Engineer Position",
        department_id=test_department.id,
        min_salary=50000,
        max_salary=100000
    )
    db_session.add(position)
    db_session.commit()
    db_session.refresh(position)
    return position


def test_create_employee(client, auth_headers, test_department, test_position):
    """Test creating an employee."""
    employee_data = {
        "employee_number": "EMP001",
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "hire_date": "2024-01-01",
        "employment_status": "active",
        "employment_type": "full_time",
        "department_id": test_department.id,
        "position_id": test_position.id
    }
    
    response = client.post(
        f"{settings.API_V1_PREFIX}/employees/",
        json=employee_data,
        headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["employee_number"] == "EMP001"
    assert data["first_name"] == "John"
    assert data["last_name"] == "Doe"
    assert "id" in data


def test_list_employees(client, auth_headers, test_department, test_position):
    """Test listing employees."""
    # Create an employee first
    from app.employees.models import Employee
    from app.employees.schemas import EmploymentStatus, EmploymentType
    from tests.conftest import TestingSessionLocal
    
    db = TestingSessionLocal()
    employee = Employee(
        employee_number="EMP002",
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        hire_date=date(2024, 1, 1),
        employment_status=EmploymentStatus.ACTIVE,
        employment_type=EmploymentType.FULL_TIME,
        department_id=test_department.id,
        position_id=test_position.id
    )
    db.add(employee)
    db.commit()
    db.close()
    
    response = client.get(
        f"{settings.API_V1_PREFIX}/employees/",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_employee(client, auth_headers, db_session, test_department, test_position):
    """Test getting an employee by ID."""
    from app.employees.models import Employee
    from app.employees.schemas import EmploymentStatus, EmploymentType
    
    employee = Employee(
        employee_number="EMP003",
        first_name="Bob",
        last_name="Johnson",
        email="bob.johnson@example.com",
        hire_date=date(2024, 1, 1),
        employment_status=EmploymentStatus.ACTIVE,
        employment_type=EmploymentType.FULL_TIME,
        department_id=test_department.id,
        position_id=test_position.id
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    
    response = client.get(
        f"{settings.API_V1_PREFIX}/employees/{employee.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == employee.id
    assert data["employee_number"] == "EMP003"


def test_update_employee(client, auth_headers, db_session, test_department, test_position):
    """Test updating an employee."""
    from app.employees.models import Employee
    from app.employees.schemas import EmploymentStatus, EmploymentType
    
    employee = Employee(
        employee_number="EMP004",
        first_name="Alice",
        last_name="Williams",
        email="alice.williams@example.com",
        hire_date=date(2024, 1, 1),
        employment_status=EmploymentStatus.ACTIVE,
        employment_type=EmploymentType.FULL_TIME,
        department_id=test_department.id,
        position_id=test_position.id
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    
    update_data = {"first_name": "Alicia"}
    response = client.put(
        f"{settings.API_V1_PREFIX}/employees/{employee.id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Alicia"


def test_delete_employee(client, auth_headers, db_session, test_department, test_position):
    """Test deleting an employee."""
    from app.employees.models import Employee
    from app.employees.schemas import EmploymentStatus, EmploymentType
    
    employee = Employee(
        employee_number="EMP005",
        first_name="Charlie",
        last_name="Brown",
        email="charlie.brown@example.com",
        hire_date=date(2024, 1, 1),
        employment_status=EmploymentStatus.ACTIVE,
        employment_type=EmploymentType.FULL_TIME,
        department_id=test_department.id,
        position_id=test_position.id
    )
    db_session.add(employee)
    db_session.commit()
    db_session.refresh(employee)
    
    response = client.delete(
        f"{settings.API_V1_PREFIX}/employees/{employee.id}",
        headers=auth_headers
    )
    assert response.status_code == 204
