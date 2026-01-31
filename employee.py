"""Employee module for JHRIS - Handles employee-related operations."""

from datetime import datetime
from database import Database
from constants import STATUS_ACTIVE, STATUS_INACTIVE
from validation import validate_email, validate_date, validate_salary, validate_status


class Employee:
    """Employee management class."""
    
    def __init__(self):
        """Initialize employee manager."""
        self.db = Database()
        
    def add_employee(self, first_name, last_name, email, phone, department_id, position, salary, hire_date):
        """
        Add a new employee to the system.
        
        Args:
            first_name: Employee's first name
            last_name: Employee's last name
            email: Employee's email address
            phone: Employee's phone number
            department_id: Department ID the employee belongs to
            position: Employee's job position
            salary: Employee's salary
            hire_date: Employee's hire date (YYYY-MM-DD)
            
        Returns:
            Employee ID if successful, None otherwise
        """
        # Validate email
        email_valid, email_error = validate_email(email)
        if not email_valid:
            print(f"Failed to add employee: {email_error}")
            return None
        
        # Validate hire date
        date_valid, date_error = validate_date(hire_date)
        if not date_valid:
            print(f"Failed to add employee: {date_error}")
            return None
        
        # Validate salary
        salary_valid, salary_error = validate_salary(salary)
        if not salary_valid:
            print(f"Failed to add employee: {salary_error}")
            return None
        
        query = '''
            INSERT INTO employees 
            (first_name, last_name, email, phone, department_id, position, salary, hire_date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = (first_name, last_name, email, phone, department_id, position, salary, hire_date, created_at)
        
        employee_id = self.db.execute_insert(query, params)
        if employee_id:
            print(f"Employee {first_name} {last_name} added successfully with ID: {employee_id}")
            return employee_id
        else:
            print("Failed to add employee. Email may already exist.")
            return None
            
    def get_employee_by_id(self, employee_id):
        """
        Get employee details by ID.
        
        Args:
            employee_id: Employee's ID
            
        Returns:
            Employee record or None
        """
        query = '''
            SELECT e.id, e.first_name, e.last_name, e.email, e.phone, 
                   d.name as department, e.position, e.salary, e.hire_date, e.status
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.id = ?
        '''
        result = self.db.execute_query(query, (employee_id,))
        return result[0] if result else None
        
    def get_all_employees(self):
        """
        Get all employees.
        
        Returns:
            List of employee records
        """
        query = '''
            SELECT e.id, e.first_name, e.last_name, e.email, e.phone, 
                   d.name as department, e.position, e.salary, e.hire_date, e.status
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            ORDER BY e.last_name, e.first_name
        '''
        return self.db.execute_query(query)
        
    def update_employee(self, employee_id, **kwargs):
        """
        Update employee information.
        
        Args:
            employee_id: Employee's ID
            **kwargs: Fields to update (first_name, last_name, email, phone, 
                     department_id, position, salary, status)
                     
        Returns:
            True if successful, False otherwise
        """
        allowed_fields = ['first_name', 'last_name', 'email', 'phone', 
                         'department_id', 'position', 'salary', 'status']
        
        update_fields = []
        params = []
        
        for field, value in kwargs.items():
            if field not in allowed_fields:
                continue
            
            # Validate specific fields
            if field == 'email':
                email_valid, email_error = validate_email(value)
                if not email_valid:
                    print(f"Validation error: {email_error}")
                    return False
            elif field == 'salary':
                salary_valid, salary_error = validate_salary(value)
                if not salary_valid:
                    print(f"Validation error: {salary_error}")
                    return False
            elif field == 'status':
                status_valid, status_error = validate_status(value)
                if not status_valid:
                    print(f"Validation error: {status_error}")
                    return False
            
            update_fields.append(f"{field} = ?")
            params.append(value)
                
        if not update_fields:
            print("No valid fields to update.")
            return False
            
        params.append(employee_id)
        query = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = ?"
        
        result = self.db.execute_query(query, tuple(params))
        if result is not None:
            print(f"Employee ID {employee_id} updated successfully.")
            return True
        return False
        
    def delete_employee(self, employee_id):
        """
        Delete an employee (soft delete by setting status to inactive).
        
        Args:
            employee_id: Employee's ID
            
        Returns:
            True if successful, False otherwise
        """
        query = f"UPDATE employees SET status = ? WHERE id = ?"
        result = self.db.execute_query(query, (STATUS_INACTIVE, employee_id))
        if result is not None:
            print(f"Employee ID {employee_id} marked as inactive.")
            return True
        return False
        
    def search_employees(self, keyword):
        """
        Search employees by name or email.
        
        Args:
            keyword: Search keyword
            
        Returns:
            List of matching employee records
        """
        query = '''
            SELECT e.id, e.first_name, e.last_name, e.email, e.phone, 
                   d.name as department, e.position, e.salary, e.hire_date, e.status
            FROM employees e
            LEFT JOIN departments d ON e.department_id = d.id
            WHERE e.first_name LIKE ? OR e.last_name LIKE ? OR e.email LIKE ?
            ORDER BY e.last_name, e.first_name
        '''
        search_term = f"%{keyword}%"
        return self.db.execute_query(query, (search_term, search_term, search_term))
