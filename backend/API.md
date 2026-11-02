# Expense Tracker API

## Authentication
- `POST /api/auth/register` - Register a new user
  - JSON body: `{ "username": "alice", "email": "alice@example.com", "password": "secret" }`
- `POST /api/auth/login` - Login and get JWT token
  - JSON body: `{ "username": "...", "password": "..." }` — `username` accepts either the **username** or the **registered email address**
  - Response: `{ "access_token": "...", "token_type": "bearer" }`
  - Wrong credentials: `401 { "detail": "Incorrect email, username or password" }`

## Expenses
### List expenses with filters and pagination
- `GET /api/expenses/` - Get all expenses for the current user with filtering, pagination, and summary
  - Query parameters:
    - `skip`: Number of records to skip (default: 0)
    - `limit`: Maximum number of records to return (default: 100)
    - `title`: Filter by title (partial match)
    - `min_amount`: Filter by minimum amount
    - `max_amount`: Filter by maximum amount
    - `description`: Filter by description (partial match)
    - `category`: Filter by category (exact match)
    - `start_date`: Filter by start date (format: YYYY-MM-DD)
    - `end_date`: Filter by end date (format: YYYY-MM-DD)
  - Response:
    ```json
    {
      "expenses": [
        {
          "id": 1,
          "title": "Groceries",
          "amount": 50.0,
          "description": "Weekly groceries",
          "category": "Food",
          "expense_date": "2023-01-15",
          "user_id": 1
        }
      ],
      "summary": {
        "total_count": 1,
        "total_amount": 50.0,
        "average_amount": 50.0
      }
    }
    ```

### Get monthly summary
- `GET /api/expenses/monthly-summary` - Get monthly summary of expenses for the current user
  - Query parameters:
    - `year`: Filter by year (optional)
    - `month`: Filter by month (optional)
  - Response:
    ```json
    {
      "monthly_summary": [
        {
          "year": 2023,
          "month": 1,
          "count": 5,
          "total_amount": 250.0,
          "average_amount": 50.0
        }
      ]
    }
    ```

### Get a specific expense
- `GET /api/expenses/{expense_id}` - Get a specific expense by ID

### Create an expense
- `POST /api/expenses/` - Create a new expense for the current user
  - JSON body: `{ "title": "...", "amount": 20.5, "category": "Food", "expense_date": "2026-11-03", "description": "..." }` (only `title` and `amount` required)
  - `amount` must be **greater than 0** (0 and negative values return 422)
  - Requires the `Authorization: Bearer <token>` header (401 otherwise); the expense is always assigned to the authenticated user

### Update an expense
- `PUT /api/expenses/{expense_id}` - Update a specific expense by ID

### Delete an expense
- `DELETE /api/expenses/{expense_id}` - Delete a specific expense by ID