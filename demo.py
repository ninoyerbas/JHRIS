"""Demo script for JHRIS - Demonstrates the system capabilities."""

import os
from database import Database
from employee import Employee
from department import Department
from tabulate import tabulate

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

# Remove any existing demo database
if os.path.exists('demo_jhris.db'):
    os.remove('demo_jhris.db')

print_section("JHRIS Demo - Human Resource Information System")

# Initialize database
print("Initializing JHRIS database...")
db = Database('demo_jhris.db')
db.create_tables()
print("✓ Database initialized successfully!\n")

# Initialize managers
dept_mgr = Department()
dept_mgr.db.db_name = 'demo_jhris.db'
emp_mgr = Employee()
emp_mgr.db.db_name = 'demo_jhris.db'

# Demo 1: Add Departments
print_section("Demo 1: Creating Departments")
dept_id_eng = dept_mgr.add_department("Engineering", "Software development and IT")
dept_id_hr = dept_mgr.add_department("Human Resources", "HR and recruitment")
dept_id_sales = dept_mgr.add_department("Sales", "Sales and customer relations")
dept_id_marketing = dept_mgr.add_department("Marketing", "Marketing and branding")
print()

# Display all departments
departments = dept_mgr.get_all_departments()
headers = ["ID", "Name", "Description", "Created At"]
print("Current Departments:")
print(tabulate(departments, headers=headers, tablefmt="grid"))

# Demo 2: Add Employees
print_section("Demo 2: Adding Employees")

# Engineering employees
emp_mgr.add_employee("Alice", "Johnson", "alice.johnson@company.com", "555-1001", 
                     dept_id_eng, "Senior Software Engineer", 95000, "2022-03-15")
emp_mgr.add_employee("Bob", "Smith", "bob.smith@company.com", "555-1002", 
                     dept_id_eng, "Software Engineer", 75000, "2023-01-10")
emp_mgr.add_employee("Charlie", "Brown", "charlie.brown@company.com", "555-1003", 
                     dept_id_eng, "DevOps Engineer", 85000, "2023-06-20")

# HR employees
emp_mgr.add_employee("Diana", "Prince", "diana.prince@company.com", "555-2001", 
                     dept_id_hr, "HR Manager", 80000, "2021-09-01")
emp_mgr.add_employee("Eve", "Williams", "eve.williams@company.com", "555-2002", 
                     dept_id_hr, "Recruiter", 60000, "2023-04-12")

# Sales employees
emp_mgr.add_employee("Frank", "Miller", "frank.miller@company.com", "555-3001", 
                     dept_id_sales, "Sales Manager", 90000, "2022-02-15")
emp_mgr.add_employee("Grace", "Lee", "grace.lee@company.com", "555-3002", 
                     dept_id_sales, "Sales Representative", 65000, "2023-08-01")

# Marketing employees
emp_mgr.add_employee("Henry", "Davis", "henry.davis@company.com", "555-4001", 
                     dept_id_marketing, "Marketing Director", 100000, "2021-05-10")

print("\n✓ All employees added successfully!")

# Demo 3: View All Employees
print_section("Demo 3: Viewing All Employees")
employees = emp_mgr.get_all_employees()
headers = ["ID", "First Name", "Last Name", "Email", "Phone", 
          "Department", "Position", "Salary", "Hire Date", "Status"]
print(tabulate(employees, headers=headers, tablefmt="grid"))

# Demo 4: Search Employees
print_section("Demo 4: Searching Employees")
print("Searching for employees with 'Smith' in their name...")
search_results = emp_mgr.search_employees("Smith")
print(tabulate(search_results, headers=headers, tablefmt="grid"))

# Demo 5: Department-wise Employee View
print_section("Demo 5: Viewing Employees by Department")
print("Engineering Department Employees:")
eng_employees = dept_mgr.get_department_employees(dept_id_eng)
if eng_employees:
    dept_headers = ["ID", "First Name", "Last Name", "Email", "Position", "Status"]
    print(tabulate(eng_employees, headers=dept_headers, tablefmt="grid"))

# Demo 6: Update Employee
print_section("Demo 6: Updating Employee Information")
print("Promoting Bob Smith to Senior Software Engineer with salary increase...")
emp_mgr.update_employee(2, position="Senior Software Engineer", salary=85000)
print("\nUpdated Employee Record:")
updated_emp = emp_mgr.get_employee_by_id(2)
print(tabulate([updated_emp], headers=headers, tablefmt="grid"))

# Demo 7: Reports
print_section("Demo 7: HR Reports and Statistics")

employees = emp_mgr.get_all_employees()
total_employees = len(employees) if employees else 0
active_employees = len([e for e in employees if e[9] == 'active']) if employees else 0

departments = dept_mgr.get_all_departments()
total_departments = len(departments) if departments else 0

print(f"📊 Total Employees: {total_employees}")
print(f"✓ Active Employees: {active_employees}")
print(f"✗ Inactive Employees: {total_employees - active_employees}")
print(f"🏢 Total Departments: {total_departments}\n")

# Department-wise employee count
print("Employees by Department:")
dept_data = []
for dept in departments:
    dept_employees = dept_mgr.get_department_employees(dept[0])
    count = len(dept_employees) if dept_employees else 0
    dept_data.append([dept[0], dept[1], count])
    
dept_headers = ["Dept ID", "Department Name", "Employee Count"]
print(tabulate(dept_data, headers=dept_headers, tablefmt="grid"))

# Salary statistics
print("\nSalary Statistics:")
if employees:
    salaries = [e[7] for e in employees if e[7] is not None]
    if salaries:
        avg_salary = sum(salaries) / len(salaries)
        min_salary = min(salaries)
        max_salary = max(salaries)
        print(f"Average Salary: ${avg_salary:,.2f}")
        print(f"Minimum Salary: ${min_salary:,.2f}")
        print(f"Maximum Salary: ${max_salary:,.2f}")

# Demo 8: Employee Lifecycle
print_section("Demo 8: Employee Lifecycle (Mark as Inactive)")
print("Marking employee 'Eve Williams' as inactive (resignation/termination)...")
emp_mgr.delete_employee(5)
print("\nCurrent Active Employees:")
active_emps = [e for e in emp_mgr.get_all_employees() if e[9] == 'active']
print(tabulate(active_emps, headers=headers, tablefmt="grid"))

print_section("Demo Complete!")
print("The JHRIS system has successfully demonstrated:")
print("  ✓ Department Management")
print("  ✓ Employee Management")
print("  ✓ Search Functionality")
print("  ✓ Updates and Modifications")
print("  ✓ Reports and Statistics")
print("  ✓ Employee Status Management")
print("\nDemo database: demo_jhris.db")
print("Run 'python jhris.py' to use the interactive CLI interface!")
print("="*70 + "\n")
