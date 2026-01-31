# JHRIS - Human Resources Information System

A comprehensive Human Resources Information System (HRIS) built with Python FastAPI and MySQL, featuring employee management, department organization, position tracking, and JWT-based authentication.

## 🚀 Features

### Core Modules
- **Authentication & Authorization**: JWT token-based authentication with bcrypt password hashing
- **Employee Management**: Complete employee lifecycle management with personal and employment information
- **Department Management**: Hierarchical department structure with manager assignments
- **Position Management**: Job position tracking with salary ranges and department associations
- **User Management**: User accounts with role-based access control

### Technical Highlights
- RESTful API with FastAPI
- Auto-generated API documentation (Swagger/OpenAPI)
- SQLAlchemy 2.0 ORM with MySQL 8.0
- Alembic database migrations
- Docker Compose for local development
- Comprehensive test suite with pytest
- Type hints throughout codebase
- Input validation with Pydantic v2

## 📋 Prerequisites

- Python 3.11 or higher
- Docker and Docker Compose (for containerized setup)
- MySQL 8.0 (for local setup without Docker)
- Redis (optional, for future caching)

## 🛠️ Installation

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/ninoyerbas/JHRIS.git
cd JHRIS
```

2. **Copy environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Start the application**
```bash
docker-compose up -d
```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Alternative Documentation: http://localhost:8000/redoc

### Option 2: Local Development

1. **Clone the repository**
```bash
git clone https://github.com/ninoyerbas/JHRIS.git
cd JHRIS
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your database configuration
```

5. **Set up MySQL database**
```bash
# Create database
mysql -u root -p
CREATE DATABASE jhris_db;
CREATE USER 'jhris_user'@'localhost' IDENTIFIED BY 'jhris_password';
GRANT ALL PRIVILEGES ON jhris_db.* TO 'jhris_user'@'localhost';
FLUSH PRIVILEGES;
```

6. **Run database migrations**
```bash
alembic upgrade head
```

7. **Start the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🗄️ Database Schema

### Users Table
- Authentication and user management
- Fields: id, email, hashed_password, is_active, is_superuser, timestamps

### Employees Table
- Comprehensive employee information
- Personal details, contact information, employment details
- Supports self-referential manager relationships

### Departments Table
- Hierarchical department structure
- Fields: id, name, code, description, parent_department_id, manager_id, timestamps

### Positions Table
- Job positions with salary ranges
- Fields: id, title, code, description, department_id, min_salary, max_salary, timestamps

## 🔌 API Endpoints

### Authentication (`/api/v1/auth`)
- `POST /register` - Register new user
- `POST /login` - Login and get JWT token
- `POST /refresh` - Refresh access token
- `GET /me` - Get current user info

### Employees (`/api/v1/employees`)
- `GET /` - List all employees (paginated, filterable)
- `POST /` - Create new employee
- `GET /{id}` - Get employee by ID
- `PUT /{id}` - Update employee
- `DELETE /{id}` - Delete employee
- `GET /{id}/subordinates` - Get direct reports

### Departments (`/api/v1/departments`)
- `GET /` - List all departments
- `POST /` - Create department
- `GET /{id}` - Get department by ID
- `PUT /{id}` - Update department
- `DELETE /{id}` - Delete department

### Positions (`/api/v1/positions`)
- `GET /` - List all positions
- `POST /` - Create position
- `GET /{id}` - Get position by ID
- `PUT /{id}` - Update position
- `DELETE /{id}` - Delete position

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## 📚 Project Structure

```
JHRIS/
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   ├── database.py                # Database connection setup
│   ├── dependencies.py            # Dependency injection
│   │
│   ├── auth/                      # Authentication module
│   │   ├── __init__.py
│   │   ├── router.py              # Auth API routes
│   │   ├── schemas.py             # Pydantic models
│   │   ├── service.py             # Business logic
│   │   └── utils.py               # JWT utilities
│   │
│   ├── users/                     # User management
│   ├── employees/                 # Employee management
│   ├── departments/               # Department management
│   └── positions/                 # Position management
│
├── alembic/                       # Database migrations
├── tests/                         # Test suite
├── docker-compose.yml             # Docker services
├── Dockerfile                     # Application container
├── requirements.txt               # Dependencies
└── README.md                      # This file
```

## 🔐 Security Features

- **Password Hashing**: bcrypt with passlib
- **JWT Authentication**: Secure token-based authentication
- **CORS Configuration**: Configurable cross-origin resource sharing
- **Role-Based Access**: Superuser and regular user roles
- **SQL Injection Protection**: SQLAlchemy ORM with parameterized queries
- **Input Validation**: Pydantic models for all inputs

## 🔧 Configuration

Environment variables can be configured in `.env` file:

```bash
# Application
APP_NAME=JHRIS
DEBUG=True
ENVIRONMENT=development

# Security
SECRET_KEY=your-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database
DATABASE_URL=mysql+pymysql://user:pass@localhost:3306/jhris_db

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

## 🚦 Health Check

Check application health:
```bash
curl http://localhost:8000/health
```

## 📖 API Documentation

Once the application is running, access the interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🗺️ Future Roadmap

- [ ] Leave Management Module
- [ ] Payroll Management
- [ ] Performance Reviews
- [ ] Training & Development
- [ ] Attendance Tracking
- [ ] Document Management
- [ ] Reporting & Analytics Dashboard
- [ ] Email Notifications
- [ ] Two-Factor Authentication
- [ ] Audit Logging

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- **JHRIS Team** - Initial work

## 🙏 Acknowledgments

- FastAPI framework
- SQLAlchemy ORM
- Pydantic for data validation
- All contributors to the open-source libraries used

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.
A comprehensive web-based HRIS (Human Resources Information System) for managing employees, attendance, and leave requests.

## Quick Start

### Backend
```bash
cd backend
npm install
npm start
```

### Frontend
```bash
cd frontend/public
# Open index.html in your browser or use:
python -m http.server 8000
```

## Features

- 👥 **Employee Management**: Add, view, edit employee records
- ⏰ **Attendance Tracking**: Clock in/out, attendance reports
- 🏖️ **Leave Management**: Leave requests, approvals, balance tracking
- 🔐 **User Authentication**: Role-based access control (Admin, HR, Manager, Employee)

## Documentation

See [docs/README.md](docs/README.md) for complete documentation including:
- Installation instructions
- API documentation
- Database schema
- Usage guide

## Technology Stack

- **Backend**: Node.js, Express, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **Authentication**: JWT

## License

ISC
