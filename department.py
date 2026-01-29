"""Department module for JHRIS - Handles department-related operations."""

from datetime import datetime
from database import Database


class Department:
    """Department management class."""
    
    def __init__(self):
        """Initialize department manager."""
        self.db = Database()
        
    def add_department(self, name, description=''):
        """
        Add a new department to the system.
        
        Args:
            name: Department name
            description: Department description (optional)
            
        Returns:
            Department ID if successful, None otherwise
        """
        query = '''
            INSERT INTO departments (name, description, created_at)
            VALUES (?, ?, ?)
        '''
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        params = (name, description, created_at)
        
        dept_id = self.db.execute_insert(query, params)
        if dept_id:
            print(f"Department '{name}' added successfully with ID: {dept_id}")
            return dept_id
        else:
            print("Failed to add department.")
            return None
            
    def get_department_by_id(self, dept_id):
        """
        Get department details by ID.
        
        Args:
            dept_id: Department's ID
            
        Returns:
            Department record or None
        """
        query = "SELECT * FROM departments WHERE id = ?"
        result = self.db.execute_query(query, (dept_id,))
        return result[0] if result else None
        
    def get_all_departments(self):
        """
        Get all departments.
        
        Returns:
            List of department records
        """
        query = "SELECT * FROM departments ORDER BY name"
        return self.db.execute_query(query)
        
    def update_department(self, dept_id, name=None, description=None):
        """
        Update department information.
        
        Args:
            dept_id: Department's ID
            name: New department name (optional)
            description: New department description (optional)
            
        Returns:
            True if successful, False otherwise
        """
        update_fields = []
        params = []
        
        if name:
            update_fields.append("name = ?")
            params.append(name)
        if description is not None:
            update_fields.append("description = ?")
            params.append(description)
            
        if not update_fields:
            print("No fields to update.")
            return False
            
        params.append(dept_id)
        query = f"UPDATE departments SET {', '.join(update_fields)} WHERE id = ?"
        
        result = self.db.execute_query(query, tuple(params))
        if result is not None:
            print(f"Department ID {dept_id} updated successfully.")
            return True
        return False
        
    def delete_department(self, dept_id):
        """
        Delete a department.
        
        Args:
            dept_id: Department's ID
            
        Returns:
            True if successful, False otherwise
        """
        # Check if department has employees
        check_query = "SELECT COUNT(*) FROM employees WHERE department_id = ? AND status = 'active'"
        result = self.db.execute_query(check_query, (dept_id,))
        
        if result and result[0][0] > 0:
            print(f"Cannot delete department. It has {result[0][0]} active employee(s).")
            return False
            
        query = "DELETE FROM departments WHERE id = ?"
        result = self.db.execute_query(query, (dept_id,))
        if result is not None:
            print(f"Department ID {dept_id} deleted successfully.")
            return True
        return False
        
    def get_department_employees(self, dept_id):
        """
        Get all employees in a department.
        
        Args:
            dept_id: Department's ID
            
        Returns:
            List of employee records in the department
        """
        query = '''
            SELECT e.id, e.first_name, e.last_name, e.email, e.position, e.status
            FROM employees e
            WHERE e.department_id = ?
            ORDER BY e.last_name, e.first_name
        '''
        return self.db.execute_query(query, (dept_id,))
