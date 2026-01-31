# JHRIS - Human Resources Information System

A comprehensive web-based HRIS (Human Resources Information System) for managing employees, attendance, and leave requests.

## Features

### Core Functionality

1. **Employee Management**
   - Add, view, edit, and manage employee records
   - Track employee information (personal details, department, position)
   - Employee status management (active/inactive)

2. **Attendance Tracking**
   - Clock in/out functionality
   - Daily attendance marking
   - Attendance reports and filtering
   - View attendance history by employee

3. **Leave Management**
   - Multiple leave types (Annual, Sick, Personal, Maternity, Paternity)
   - Leave request submission
   - Approval/rejection workflow
   - Leave balance tracking

4. **User Authentication & Authorization**
   - Role-based access control (Admin, HR, Manager, Employee)
   - Secure login and registration
   - JWT-based authentication

## Technology Stack

### Backend
- **Node.js** with Express.js
- **SQLite** database
- **JWT** for authentication
- **bcryptjs** for password hashing

### Frontend
- **HTML5/CSS3/JavaScript**
- Responsive design
- Modern UI with gradient styling

## Installation & Setup

### Prerequisites
- Node.js (v14 or higher)
- npm (v6 or higher)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
   - Edit `.env` file and update the JWT_SECRET

4. Start the backend server:
```bash
npm start
```

For development with auto-reload:
```bash
npm run dev
```

The API will be available at `http://localhost:3001`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Open `public/index.html` in a web browser, or serve it using a simple HTTP server:
```bash
# Using Python
python -m http.server 8000 -d public

# Or using Node.js
npx http-server public -p 8000
```

The application will be available at `http://localhost:8000`

## Usage

### Initial Setup

1. **Register an Admin User:**
   - Open the application
   - Click "Register here"
   - Fill in the form and select "Admin" as role
   - Login with the created credentials

2. **Create Employees:**
   - Navigate to the Employees section
   - Click "Add Employee"
   - Fill in employee details

3. **Initialize Leave Balances:**
   - Use the API to initialize leave balances for employees
   - See API documentation below

### Daily Operations

#### For Employees:
- Clock in/out using the Dashboard quick actions
- Submit leave requests
- View attendance history

#### For HR/Managers:
- Approve/reject leave requests
- Mark attendance for employees
- View all attendance records
- Manage employee records

#### For Admins:
- Full access to all features
- Add/edit/delete employees
- Configure system settings

## API Documentation

### Authentication

#### Register User
```
POST /api/auth/register
Body: { username, email, password, role }
```

#### Login
```
POST /api/auth/login
Body: { username, password }
Returns: { token, user }
```

#### Get Current User
```
GET /api/auth/me
Headers: Authorization: Bearer <token>
```

### Employees

#### Get All Employees
```
GET /api/employees
Query params: status, department
```

#### Get Employee by ID
```
GET /api/employees/:id
```

#### Create Employee
```
POST /api/employees
Body: { first_name, last_name, employee_id, department, position, hire_date, phone, address }
```

#### Update Employee
```
PUT /api/employees/:id
Body: { first_name, last_name, department, position, phone, address, status }
```

#### Delete Employee (Soft Delete)
```
DELETE /api/employees/:id
```

### Attendance

#### Clock In
```
POST /api/attendance/clock-in
Body: { employee_id }
```

#### Clock Out
```
POST /api/attendance/clock-out
Body: { employee_id }
```

#### Mark Attendance
```
POST /api/attendance/mark
Body: { employee_id, date, status, notes }
```

#### Get All Attendance
```
GET /api/attendance
Query params: date, status
```

#### Get Attendance by Employee
```
GET /api/attendance/employee/:employee_id
Query params: start_date, end_date
```

### Leave Management

#### Get Leave Types
```
GET /api/leave/types
```

#### Create Leave Request
```
POST /api/leave/requests
Body: { employee_id, leave_type_id, start_date, end_date, days, reason }
```

#### Get All Leave Requests
```
GET /api/leave/requests
Query params: status, employee_id
```

#### Get Leave Request by ID
```
GET /api/leave/requests/:id
```

#### Approve/Reject Leave Request
```
PUT /api/leave/requests/:id
Body: { status: 'approved' | 'rejected' }
```

#### Get Leave Balance
```
GET /api/leave/balance/:employee_id
Query params: year
```

#### Initialize Leave Balance
```
POST /api/leave/balance
Body: { employee_id, leave_type_id, total_days, year }
```

## Database Schema

### Users
- id, username, password, email, role, created_at, updated_at

### Employees
- id, user_id, first_name, last_name, employee_id, department, position, hire_date, phone, address, status, created_at, updated_at

### Attendance
- id, employee_id, date, clock_in, clock_out, status, notes, created_at, updated_at

### Leave Types
- id, name, description, max_days, created_at

### Leave Balances
- id, employee_id, leave_type_id, total_days, used_days, remaining_days, year, created_at, updated_at

### Leave Requests
- id, employee_id, leave_type_id, start_date, end_date, days, reason, status, approved_by, approved_at, created_at, updated_at

## Security Features

- Password hashing using bcryptjs
- JWT-based authentication
- Role-based access control (RBAC)
- Protected API endpoints
- Input validation

## Future Enhancements

- Payroll management
- Performance appraisals
- Training and development tracking
- Document management
- Email notifications
- Advanced reporting and analytics
- Mobile application
- Integration with biometric devices

## License

ISC

## Contributing

Feel free to submit issues and enhancement requests!

## Support

For support, please contact the development team or create an issue in the repository.
