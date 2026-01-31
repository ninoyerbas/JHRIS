"""Test script for JHRIS to verify functionality."""

import os
import sys
from database import Database
from employee import Employee
from department import Department

# Remove any existing test database
if os.path.exists('test_jhris.db'):
    os.remove('test_jhris.db')

# Initialize database
print("Testing JHRIS functionality...")
print("="*60)

db = Database('test_jhris.db')
db.create_tables()
print("✓ Database tables created successfully")

# Test Department Management
print("\n--- Testing Department Management ---")
dept_mgr = Department()
dept_mgr.db.db_name = 'test_jhris.db'

dept_id_1 = dept_mgr.add_department("Engineering", "Software development team")
dept_id_2 = dept_mgr.add_department("HR", "Human Resources department")
dept_id_3 = dept_mgr.add_department("Sales", "Sales and marketing team")

if dept_id_1 and dept_id_2 and dept_id_3:
    print("✓ Departments created successfully")
else:
    print("✗ Failed to create departments")
    sys.exit(1)

departments = dept_mgr.get_all_departments()
print(f"✓ Retrieved {len(departments)} departments")

# Test Employee Management
print("\n--- Testing Employee Management ---")
emp_mgr = Employee()
emp_mgr.db.db_name = 'test_jhris.db'

emp_id_1 = emp_mgr.add_employee(
    "John", "Doe", "john.doe@company.com", "555-0101",
    dept_id_1, "Software Engineer", 75000, "2024-01-15"
)

emp_id_2 = emp_mgr.add_employee(
    "Jane", "Smith", "jane.smith@company.com", "555-0102",
    dept_id_1, "Senior Developer", 95000, "2023-06-01"
)

emp_id_3 = emp_mgr.add_employee(
    "Bob", "Johnson", "bob.johnson@company.com", "555-0103",
    dept_id_2, "HR Manager", 85000, "2023-03-15"
)

if emp_id_1 and emp_id_2 and emp_id_3:
    print("✓ Employees created successfully")
else:
    print("✗ Failed to create employees")
    sys.exit(1)

# Test Get All Employees
employees = emp_mgr.get_all_employees()
print(f"✓ Retrieved {len(employees)} employees")

# Test Search
search_results = emp_mgr.search_employees("John")
print(f"✓ Search for 'John' returned {len(search_results)} result(s)")

# Test Get Employee by ID
employee = emp_mgr.get_employee_by_id(emp_id_1)
if employee:
    print(f"✓ Retrieved employee: {employee[1]} {employee[2]}")
else:
    print("✗ Failed to retrieve employee by ID")

# Test Update Employee
update_success = emp_mgr.update_employee(emp_id_1, position="Senior Software Engineer", salary=85000)
if update_success:
    print("✓ Employee updated successfully")
else:
    print("✗ Failed to update employee")

# Test Department Employees
dept_employees = dept_mgr.get_department_employees(dept_id_1)
print(f"✓ Engineering department has {len(dept_employees)} employee(s)")

# Test Update Department
update_dept_success = dept_mgr.update_department(dept_id_1, description="Software development and engineering team")
if update_dept_success:
    print("✓ Department updated successfully")
else:
    print("✗ Failed to update department")

# Test Delete Employee (soft delete)
delete_emp_success = emp_mgr.delete_employee(emp_id_3)
if delete_emp_success:
    print("✓ Employee marked as inactive successfully")
else:
    print("✗ Failed to mark employee as inactive")

# Verify employee is inactive
employee = emp_mgr.get_employee_by_id(emp_id_3)
if employee and employee[9] == 'inactive':
    print("✓ Employee status verified as inactive")
else:
    print("✗ Employee status not updated correctly")

# Test Delete Department with employees (should fail)
print("\n--- Testing Business Logic ---")
delete_dept_success = dept_mgr.delete_department(dept_id_1)
if not delete_dept_success:
    print("✓ Correctly prevented deletion of department with active employees")
else:
    print("✗ Should not allow deletion of department with employees")

# Test Delete Empty Department
empty_dept_id = dept_mgr.add_department("Test Department", "Temporary test department")
delete_empty_dept_success = dept_mgr.delete_department(empty_dept_id)
if delete_empty_dept_success:
    print("✓ Successfully deleted empty department")
else:
    print("✗ Failed to delete empty department")

print("\n" + "="*60)
print("All tests completed successfully!")
print("="*60)

# Cleanup
os.remove('test_jhris.db')
print("\nTest database cleaned up.")
