# Expense Tracker Backend

## Setup Instructions

1. Create virtual environment:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Run the application:
```bash
uvicorn app.main:app --port 8100 --reload
```

3. Run tests:
```bash
pytest -q
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get access token

### Expenses
- `GET /api/expenses` - Get all expenses for current user
- `POST /api/expenses` - Create a new expense
- `GET /api/expenses/{id}` - Get a specific expense
- `PUT /api/expenses/{id}` - Update an expense
- `DELETE /api/expenses/{id}` - Delete an expense

## Features Implemented
1. User authentication (registration and login)
2. Expense CRUD operations
3. User isolation (users can only access their own expenses)
4. JWT-based authentication
5. Database models with SQLAlchemy
6. Pydantic validation schemas
7. Comprehensive test coverage