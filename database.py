"""Database module for JHRIS - Handles database operations."""

import sqlite3
from datetime import datetime
from constants import STATUS_ACTIVE


class Database:
    """Database manager for JHRIS."""
    
    def __init__(self, db_name='jhris.db'):
        """Initialize database connection."""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        
    def connect(self):
        """Establish database connection."""
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        
    def close(self):
        """Close database connection."""
        if self.connection:
            self.connection.close()
            
    def create_tables(self):
        """Create necessary database tables."""
        self.connect()
        
        # Departments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Employees table
        self.cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                phone TEXT,
                department_id INTEGER,
                position TEXT,
                salary REAL,
                hire_date TEXT NOT NULL,
                status TEXT DEFAULT '{STATUS_ACTIVE}',
                created_at TEXT NOT NULL,
                FOREIGN KEY (department_id) REFERENCES departments (id)
            )
        ''')
        
        self.connection.commit()
        self.close()
        
    def execute_query(self, query, params=None):
        """Execute a query and return results."""
        self.connect()
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.close()
            
    def execute_insert(self, query, params):
        """Execute an insert query and return the last row id."""
        self.connect()
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
            last_id = self.cursor.lastrowid
            return last_id
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return None
        finally:
            self.close()
