# Phase Checklist

## Phase 1: Backend Core with Auth and Expense CRUD

- [x] Create project structure (backend/app/{main.py,database.py,models.py,schemas.py,auth.py,routers/})
- [x] Implement database models (User, Expense)
- [x] Implement authentication (register, login, JWT)
- [x] Implement expense CRUD operations
- [x] Implement user isolation (users can only access their own expenses)
- [x] Create pytest tests for register, login, wrong password, unauthenticated access, CRUD, and cross-user access
- [x] Run pytest and fix failures until green
- [x] All backend functionality working as specified

## Phase 2: Frontend with React/Vite

- [x] Create frontend structure (frontend/src/{api.js,App.jsx,pages/,components/})
- [x] Implement login/register pages
- [x] Implement expense list page
- [x] Implement expense creation/editing forms
- [x] Connect frontend to backend API
- [x] Add responsive design

## Phase 3: Frontend Implementation (Complete)

- [x] Vite React frontend with login, registration, token storage
- [x] Protected routes that require authentication
- [x] Expense list page using endpoints from API.md
- [x] Frontend builds successfully with npm run build

## Phase 4: Enhanced Features

- [x] Add category and date filters to expense listing
- [x] Implement monthly summary view 
- [x] Add error messages for failed requests
- [x] Create README with start commands