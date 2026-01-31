# Quick Start Guide for JHRIS

## Getting Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python jhris.py
```

### 3. Try the Demo (Optional)
```bash
python demo.py
```

## Your First Steps

After running `python jhris.py`, you'll see the main menu:

### Add Your First Department
1. Select `2` for Department Management
2. Select `1` to Add New Department
3. Enter department name (e.g., "Engineering")
4. Enter description (e.g., "Software development team")
5. Go back to main menu (select `6`)

### Add Your First Employee
1. Select `1` for Employee Management
2. Select `1` to Add New Employee
3. Fill in employee details:
   - First Name: John
   - Last Name: Doe
   - Email: john.doe@company.com
   - Phone: 555-0001
   - Department ID: (select from list)
   - Position: Software Engineer
   - Salary: 75000
   - Hire Date: 2024-01-15

### View Your Data
1. From Employee Management menu, select `2` to View All Employees
2. From Department Management menu, select `2` to View All Departments

### Generate Reports
1. From main menu, select `3` for Reports
2. View statistics and department-wise employee distribution

## Common Tasks

### Search for an Employee
- Go to Employee Management > Search Employee
- Enter keyword (name or email)

### Update Employee Information
- Go to Employee Management > Update Employee
- Enter employee ID
- Update fields as needed (press Enter to skip)

### View Department Employees
- Go to Department Management > View Department Employees
- Enter department ID

### Remove an Employee
- Go to Employee Management > Remove Employee
- Enter employee ID
- Confirm the action
- Note: This marks employee as "inactive" (soft delete)

## Testing

Run the test suite to verify functionality:
```bash
python test_jhris.py
```

## Demo Mode

See the system in action with sample data:
```bash
python demo.py
```

This creates a demo database with sample departments and employees, then shows all major features.

## Tips

- The database file `jhris.db` is created automatically on first run
- All dates should be in YYYY-MM-DD format
- Email addresses must be unique per employee
- Departments with active employees cannot be deleted
- Employees are soft-deleted (marked as inactive) to maintain history
- Use Ctrl+C to exit the application at any time

## Next Steps

- Customize the system for your organization
- Add more departments and employees
- Use the search feature to find specific employees
- Generate reports to analyze your workforce
- Keep track of salary information and hiring dates

Enjoy using JHRIS!
