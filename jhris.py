"""Main CLI interface for JHRIS - Human Resource Information System."""

import sys
from tabulate import tabulate
from database import Database
from employee import Employee
from department import Department


class JHRIS:
    """Main JHRIS application class."""
    
    def __init__(self):
        """Initialize JHRIS application."""
        self.db = Database()
        self.employee_mgr = Employee()
        self.department_mgr = Department()
        
    def initialize_database(self):
        """Initialize the database with required tables."""
        print("Initializing JHRIS database...")
        self.db.create_tables()
        print("Database initialized successfully!")
        
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("    JHRIS - Human Resource Information System")
        print("="*60)
        print("\n=== Main Menu ===")
        print("1. Employee Management")
        print("2. Department Management")
        print("3. Reports")
        print("4. Exit")
        print()
        
    def display_employee_menu(self):
        """Display employee management menu."""
        print("\n=== Employee Management ===")
        print("1. Add New Employee")
        print("2. View All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Remove Employee")
        print("6. Back to Main Menu")
        print()
        
    def display_department_menu(self):
        """Display department management menu."""
        print("\n=== Department Management ===")
        print("1. Add New Department")
        print("2. View All Departments")
        print("3. View Department Employees")
        print("4. Update Department")
        print("5. Delete Department")
        print("6. Back to Main Menu")
        print()
        
    def add_employee_interactive(self):
        """Add a new employee interactively."""
        print("\n--- Add New Employee ---")
        
        first_name = input("First Name: ").strip()
        last_name = input("Last Name: ").strip()
        email = input("Email: ").strip()
        phone = input("Phone: ").strip()
        
        # Show departments
        departments = self.department_mgr.get_all_departments()
        if departments:
            print("\nAvailable Departments:")
            for dept in departments:
                print(f"  {dept[0]}. {dept[1]}")
            dept_id = input("Department ID (or 0 for none): ").strip()
            dept_id = int(dept_id) if dept_id and dept_id != '0' else None
        else:
            print("No departments available. Create a department first.")
            dept_id = None
            
        position = input("Position: ").strip()
        salary = input("Salary: ").strip()
        salary = float(salary) if salary else 0.0
        hire_date = input("Hire Date (YYYY-MM-DD): ").strip()
        
        if first_name and last_name and email and hire_date:
            self.employee_mgr.add_employee(
                first_name, last_name, email, phone, 
                dept_id, position, salary, hire_date
            )
        else:
            print("Error: First name, last name, email, and hire date are required.")
            
    def view_all_employees(self):
        """View all employees."""
        print("\n--- All Employees ---")
        employees = self.employee_mgr.get_all_employees()
        
        if employees:
            headers = ["ID", "First Name", "Last Name", "Email", "Phone", 
                      "Department", "Position", "Salary", "Hire Date", "Status"]
            print(tabulate(employees, headers=headers, tablefmt="grid"))
        else:
            print("No employees found.")
            
    def search_employee_interactive(self):
        """Search for employees interactively."""
        print("\n--- Search Employee ---")
        keyword = input("Enter search keyword (name or email): ").strip()
        
        if keyword:
            employees = self.employee_mgr.search_employees(keyword)
            if employees:
                headers = ["ID", "First Name", "Last Name", "Email", "Phone", 
                          "Department", "Position", "Salary", "Hire Date", "Status"]
                print(tabulate(employees, headers=headers, tablefmt="grid"))
            else:
                print("No employees found matching the search criteria.")
        else:
            print("Please enter a search keyword.")
            
    def update_employee_interactive(self):
        """Update an employee interactively."""
        print("\n--- Update Employee ---")
        emp_id = input("Enter Employee ID: ").strip()
        
        if not emp_id:
            print("Employee ID is required.")
            return
            
        emp_id = int(emp_id)
        employee = self.employee_mgr.get_employee_by_id(emp_id)
        
        if not employee:
            print(f"Employee with ID {emp_id} not found.")
            return
            
        print("\nCurrent Employee Details:")
        headers = ["ID", "First Name", "Last Name", "Email", "Phone", 
                  "Department", "Position", "Salary", "Hire Date", "Status"]
        print(tabulate([employee], headers=headers, tablefmt="grid"))
        
        print("\nEnter new values (press Enter to skip):")
        updates = {}
        
        first_name = input("First Name: ").strip()
        if first_name:
            updates['first_name'] = first_name
            
        last_name = input("Last Name: ").strip()
        if last_name:
            updates['last_name'] = last_name
            
        email = input("Email: ").strip()
        if email:
            updates['email'] = email
            
        phone = input("Phone: ").strip()
        if phone:
            updates['phone'] = phone
            
        position = input("Position: ").strip()
        if position:
            updates['position'] = position
            
        salary = input("Salary: ").strip()
        if salary:
            updates['salary'] = float(salary)
            
        status = input("Status (active/inactive): ").strip()
        if status:
            updates['status'] = status
            
        if updates:
            self.employee_mgr.update_employee(emp_id, **updates)
        else:
            print("No changes made.")
            
    def remove_employee_interactive(self):
        """Remove an employee interactively."""
        print("\n--- Remove Employee ---")
        emp_id = input("Enter Employee ID to remove: ").strip()
        
        if not emp_id:
            print("Employee ID is required.")
            return
            
        emp_id = int(emp_id)
        confirm = input(f"Are you sure you want to remove employee {emp_id}? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            self.employee_mgr.delete_employee(emp_id)
        else:
            print("Operation cancelled.")
            
    def add_department_interactive(self):
        """Add a new department interactively."""
        print("\n--- Add New Department ---")
        
        name = input("Department Name: ").strip()
        description = input("Description (optional): ").strip()
        
        if name:
            self.department_mgr.add_department(name, description)
        else:
            print("Error: Department name is required.")
            
    def view_all_departments(self):
        """View all departments."""
        print("\n--- All Departments ---")
        departments = self.department_mgr.get_all_departments()
        
        if departments:
            headers = ["ID", "Name", "Description", "Created At"]
            print(tabulate(departments, headers=headers, tablefmt="grid"))
        else:
            print("No departments found.")
            
    def view_department_employees_interactive(self):
        """View employees in a department interactively."""
        print("\n--- View Department Employees ---")
        dept_id = input("Enter Department ID: ").strip()
        
        if not dept_id:
            print("Department ID is required.")
            return
            
        dept_id = int(dept_id)
        employees = self.department_mgr.get_department_employees(dept_id)
        
        if employees:
            headers = ["ID", "First Name", "Last Name", "Email", "Position", "Status"]
            print(tabulate(employees, headers=headers, tablefmt="grid"))
        else:
            print("No employees found in this department.")
            
    def update_department_interactive(self):
        """Update a department interactively."""
        print("\n--- Update Department ---")
        dept_id = input("Enter Department ID: ").strip()
        
        if not dept_id:
            print("Department ID is required.")
            return
            
        dept_id = int(dept_id)
        department = self.department_mgr.get_department_by_id(dept_id)
        
        if not department:
            print(f"Department with ID {dept_id} not found.")
            return
            
        print("\nCurrent Department Details:")
        headers = ["ID", "Name", "Description", "Created At"]
        print(tabulate([department], headers=headers, tablefmt="grid"))
        
        print("\nEnter new values (press Enter to skip):")
        name = input("Name: ").strip()
        description = input("Description: ").strip()
        
        if name or description:
            kwargs = {}
            if name:
                kwargs['name'] = name
            if description:
                kwargs['description'] = description
            self.department_mgr.update_department(dept_id, **kwargs)
        else:
            print("No changes made.")
            
    def delete_department_interactive(self):
        """Delete a department interactively."""
        print("\n--- Delete Department ---")
        dept_id = input("Enter Department ID to delete: ").strip()
        
        if not dept_id:
            print("Department ID is required.")
            return
            
        dept_id = int(dept_id)
        confirm = input(f"Are you sure you want to delete department {dept_id}? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            self.department_mgr.delete_department(dept_id)
        else:
            print("Operation cancelled.")
            
    def show_reports(self):
        """Show HR reports."""
        print("\n--- HR Reports ---")
        
        # Total employees
        employees = self.employee_mgr.get_all_employees()
        total_employees = len(employees) if employees else 0
        active_employees = len([e for e in employees if e[9] == 'active']) if employees else 0
        
        # Total departments
        departments = self.department_mgr.get_all_departments()
        total_departments = len(departments) if departments else 0
        
        print(f"\nTotal Employees: {total_employees}")
        print(f"Active Employees: {active_employees}")
        print(f"Inactive Employees: {total_employees - active_employees}")
        print(f"Total Departments: {total_departments}")
        
        # Department-wise employee count
        if departments:
            print("\n--- Employees by Department ---")
            dept_data = []
            for dept in departments:
                dept_employees = self.department_mgr.get_department_employees(dept[0])
                dept_data.append([dept[0], dept[1], len(dept_employees) if dept_employees else 0])
            headers = ["Dept ID", "Department Name", "Employee Count"]
            print(tabulate(dept_data, headers=headers, tablefmt="grid"))
            
    def run_employee_management(self):
        """Run employee management menu."""
        while True:
            self.display_employee_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.add_employee_interactive()
            elif choice == '2':
                self.view_all_employees()
            elif choice == '3':
                self.search_employee_interactive()
            elif choice == '4':
                self.update_employee_interactive()
            elif choice == '5':
                self.remove_employee_interactive()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def run_department_management(self):
        """Run department management menu."""
        while True:
            self.display_department_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.add_department_interactive()
            elif choice == '2':
                self.view_all_departments()
            elif choice == '3':
                self.view_department_employees_interactive()
            elif choice == '4':
                self.update_department_interactive()
            elif choice == '5':
                self.delete_department_interactive()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
                
    def run(self):
        """Run the main application."""
        print("\nWelcome to JHRIS!")
        self.initialize_database()
        
        while True:
            self.display_menu()
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.run_employee_management()
            elif choice == '2':
                self.run_department_management()
            elif choice == '3':
                self.show_reports()
            elif choice == '4':
                print("\nThank you for using JHRIS. Goodbye!")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")


def main():
    """Main entry point."""
    try:
        app = JHRIS()
        app.run()
    except KeyboardInterrupt:
        print("\n\nApplication interrupted. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
