# Expense Tracker Frontend

This is the React/Vite frontend for the Expense Tracker application, implementing Phase 3 of the project.

## Features Implemented

- Vite React application with modern ES6+ features
- Login and registration pages with form validation
- Token storage using localStorage
- Protected routes that require authentication
- Expense list page showing expenses with summary statistics
- API integration with backend endpoints as documented in API.md

## Project Structure

```
frontend/
├── src/
│   ├── api.js              # API client for backend communication
│   ├── App.jsx             # Main application component with routing
│   ├── main.jsx            # Entry point
│   ├── index.css           # Global styles
│   ├── components/
│   │   └── Header.jsx      # Header component with logout functionality
│   └── pages/
│       ├── LoginPage.jsx   # Login page
│       ├── RegisterPage.jsx# Registration page
│       └── ExpenseListPage.jsx # Expense list page
├── index.html              # HTML template
├── package.json            # Dependencies and scripts
└── vite.config.js          # Vite configuration
```

## API Endpoints Used

All frontend components communicate with the backend using these endpoints:

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and get JWT token

### Expenses
- `GET /api/expenses/` - Get all expenses for current user with filtering, pagination, and summary
- `GET /api/expenses/{id}` - Get specific expense by ID
- `POST /api/expenses/` - Create new expense
- `PUT /api/expenses/{id}` - Update expense
- `DELETE /api/expenses/{id}` - Delete expense

## Development

To run the development server:

```bash
cd frontend
npm install
npm run dev
```

To build for production:

```bash
cd frontend
npm install
npm run build
```

The frontend is configured to proxy API requests to `http://127.0.0.1:8100/api` using Vite's development server.