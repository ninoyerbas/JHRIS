# Quick Start Guide for JHRIS

## Prerequisites
- Python 3.11+
- Docker & Docker Compose (recommended) OR MySQL 8.0

## Quick Start with Docker (Recommended)

1. **Clone and setup**
```bash
git clone https://github.com/ninoyerbas/JHRIS.git
cd JHRIS
cp .env.example .env
```

2. **Start services**
```bash
docker-compose up -d
```

3. **Access the application**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Quick Start without Docker

1. **Clone and setup**
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
```

4. **Setup database**
```bash
# Create MySQL database
mysql -u root -p -e "CREATE DATABASE jhris_db;"
mysql -u root -p -e "CREATE USER 'jhris_user'@'localhost' IDENTIFIED BY 'jhris_password';"
mysql -u root -p -e "GRANT ALL PRIVILEGES ON jhris_db.* TO 'jhris_user'@'localhost';"
```

5. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your database credentials
```

6. **Run migrations**
```bash
alembic upgrade head
```

7. **Start the application**
```bash
uvicorn app.main:app --reload
```

## First Steps with the API

### 1. Register a User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "secure_password"}'
```

### 2. Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=secure_password"
```

Save the `access_token` from the response.

### 3. Create a Department
```bash
curl -X POST http://localhost:8000/api/v1/departments/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Engineering", "code": "ENG", "description": "Engineering Department"}'
```

### 4. Create a Position
```bash
curl -X POST http://localhost:8000/api/v1/positions/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Software Engineer",
    "code": "SE",
    "description": "Software Engineer Position",
    "department_id": 1,
    "min_salary": 50000,
    "max_salary": 100000
  }'
```

### 5. Create an Employee
```bash
curl -X POST http://localhost:8000/api/v1/employees/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "employee_number": "EMP001",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@company.com",
    "hire_date": "2024-01-01",
    "department_id": 1,
    "position_id": 1,
    "employment_status": "active",
    "employment_type": "full_time"
  }'
```

### 6. List Employees
```bash
curl http://localhost:8000/api/v1/employees/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Interactive API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI where you can:
- Explore all available endpoints
- Test API calls directly from the browser
- View request/response schemas
- See authentication requirements

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_auth.py
```

## Development Tips

1. **Enable debug mode**: Set `DEBUG=True` in `.env`
2. **Check logs**: Application logs will show detailed information
3. **Database migrations**: After model changes, run:
   ```bash
   alembic revision --autogenerate -m "Description"
   alembic upgrade head
   ```

## Troubleshooting

### Port already in use
```bash
# Change port in docker-compose.yml or when running uvicorn:
uvicorn app.main:app --port 8001
```

### Database connection failed
- Verify MySQL is running
- Check credentials in `.env`
- Ensure database exists

### Import errors
- Activate virtual environment
- Reinstall dependencies: `pip install -r requirements.txt`

## Next Steps

- Customize employee fields in `app/employees/models.py`
- Add role-based permissions
- Configure email notifications
- Set up production environment
- Deploy to cloud (AWS, GCP, Azure)

For more details, see the [full README.md](README.md)
