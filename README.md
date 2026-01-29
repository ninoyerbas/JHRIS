# JHRIS - Human Resources Information System

A lightweight and easy-to-use Human Resources Information System built with Python and SQLite.

## Features

- **Employee Management**
  - Add, view, update, and remove employee records
  - Search employees by name or email
  - Track employee status (active/inactive)
  - Store comprehensive employee information (name, email, phone, position, salary, hire date)

- **Department Management**
  - Create and manage departments
  - View all departments
  - Assign employees to departments
  - View employees by department
  - Prevent deletion of departments with active employees

- **Reports**
  - View total employees and departments
  - See active vs inactive employee counts
  - Department-wise employee distribution

## Requirements

- Python 3.6 or higher
- tabulate library (for formatted table output)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ninoyerbas/JHRIS.git
cd JHRIS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python jhris.py
```

The application will:
1. Initialize the database automatically on first run
2. Display the main menu with options for:
   - Employee Management
   - Department Management
   - Reports
   - Exit

## Database

JHRIS uses SQLite for data storage. The database file (`jhris.db`) is created automatically in the application directory when you first run the program.

### Database Schema

**Departments Table:**
- id (Primary Key)
- name (Unique)
- description
- created_at

**Employees Table:**
- id (Primary Key)
- first_name
- last_name
- email (Unique)
- phone
- department_id (Foreign Key)
- position
- salary
- hire_date
- status (active/inactive)
- created_at

## Example Workflow

1. **Add a Department:**
   - Navigate to Department Management > Add New Department
   - Enter department name and description

2. **Add an Employee:**
   - Navigate to Employee Management > Add New Employee
   - Fill in employee details (name, email, phone, etc.)
   - Select a department from the list

3. **View Employees:**
   - Navigate to Employee Management > View All Employees
   - See all employee records in a formatted table

4. **Generate Reports:**
   - Navigate to Reports from the main menu
   - View summary statistics and department-wise distribution

## File Structure

```
JHRIS/
├── jhris.py          # Main application entry point
├── database.py       # Database connection and operations
├── employee.py       # Employee management module
├── department.py     # Department management module
├── requirements.txt  # Python dependencies
├── .gitignore       # Git ignore rules
└── README.md        # This file
```

## Data Validation

- Email addresses must be unique per employee
- Department names must be unique
- Employees can only be "soft deleted" (marked as inactive)
- Departments with active employees cannot be deleted

## Contributing

This is a basic HRIS system. Feel free to fork and extend it with additional features such as:
- Leave management
- Attendance tracking
- Payroll integration
- Performance reviews
- Document management
- Web-based interface

## License

Open source - feel free to use and modify as needed.
