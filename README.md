# Expense Tracker

A full-stack expense tracking application built with Python FastAPI and React/Vite.

Project made to test local AI system using "Qwen3.8:27B".

## Project Structure

```
Expense_Tracker/
├── backend/                # Python/FastAPI backend
│   ├── app/                # Application code
│   │   ├── main.py         # Main FastAPI app (CORS, router registration)
│   │   ├── database.py     # Database setup + ensure_schema() migration
│   │   ├── models.py       # Database models
│   │   ├── schemas.py      # Pydantic schemas (amount must be > 0)
│   │   ├── auth.py         # Auth logic (bcrypt + JWT, email/username lookup)
│   │   └── routers/        # API route handlers (auth.py, expenses.py)
│   ├── tests/              # pytest suite (isolated in-memory SQLite)
│   ├── API.md              # API documentation (contract)
│   ├── app.db              # SQLite database
│   └── requirements.txt    # Python dependencies
├── frontend/               # React/Vite frontend
│   ├── src/                # Source code
│   │   ├── api.js          # API client (relative /api URLs, error formatting)
│   │   ├── constants.js    # Shared expense category list
│   │   ├── components/     # Header, AddExpenseModal
│   │   └── pages/          # Login/Register/ExpenseList pages
│   └── package.json        # Frontend dependencies
├── backups/                # Timestamped SQLite backups (not in Git)
├── AGENTS.md               # Agent/builder instructions
└── PLAN.md                 # Phase checklist
```

## Features

### Backend
- User authentication: register, login (JWT bearer tokens)
- Login accepts **email or username**
- Passwords hashed with bcrypt
- Expense CRUD with full filtering, pagination and summaries
- Strict user isolation: every expense query/filter is scoped to the authenticated user
- Amount validation (`> 0`) on expense create and update
- Non-destructive SQLite schema migration at startup (`ensure_schema()`)
- 21-test regression suite (auth, expenses, isolation, validation)

### Frontend
- Vite React application with protected routes
- Login (email or username) and registration pages with readable error messages
- **+ Add Expense** modal on the dashboard (see below)
- Expense list with totals, average, monthly summary
- Category and date filtering
- Automatic refresh of list/totals/summaries after adding or deleting

## Development Setup

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8100 --host 0.0.0.0 --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev -- --port 5173 --host
```

The frontend is served at http://localhost:5173 (or http://20.20.20.152:5173 on the LAN) and the Vite dev server proxies all `/api` requests to the backend at `http://127.0.0.1:8100`, so the browser only talks to its own origin.

CORS on the backend is configured for direct (non-proxy) browser calls from `http://20.20.20.152:5173`, `http://localhost:5173` and `http://127.0.0.1:5173` — update `backend/app/main.py` if the server IP changes.

## Database

- SQLite file: `backend/app.db` (configured in `backend/app/database.py`)
- **Startup migration:** `Base.metadata.create_all()` creates missing tables, then `ensure_schema()` adds any columns missing from older databases with `ALTER TABLE` — existing data is never deleted.
- To reset the database: back it up first (see `backups/`), then delete rows from `expenses` (children) before `users` (parents) to respect the foreign key.

## Registration & Login

- Register at `/register` with a **username**, **email**, and password. Passwords are bcrypt-hashed before storage; the model stores both `username` and `email`, both unique.
- Log in at `/login` with either your **email address** or your **username** plus password.
- The backend returns a JWT access token (`{access_token, token_type: "bearer"}`). The frontend stores it in `localStorage` and sends it as an `Authorization: Bearer <token>` header on protected requests.
- Authentication survives navigation; **Logout** in the header removes the token, and protected routes redirect to `/login`.
- Errors are rendered readably: `401` → "Incorrect email, username or password"; validation errors → field-specific messages (e.g. "Username: Field required"); network failures → "Network error: could not reach the server."

## Adding an Expense

1. Log in and open the dashboard (**My Expenses**).
2. Click the green **+ Add Expense** button (top right of the header).
3. Fill in the form:
   - **Title** (required)
   - **Amount** (required; must be greater than 0 — zero/negative amounts are rejected client-side and by the backend with 422)
   - **Category** (dropdown: Food, Transport, Housing, Utilities, Entertainment, Health, Shopping, Education, Travel, Other)
   - **Date** (defaults to today)
   - **Description** (optional notes)
   - *Payment method is not stored — the database model has no such field.*
4. Click **Add Expense**: the modal closes, the expense appears immediately in the list (filters that could hide it are cleared), totals and the monthly summary update, and a success banner is displayed for a few seconds.

## Database Backup

A full backup taken before the authorized 2026-11-03 user-data reset (contains the 10 users and 1 expense that existed at that time):

```
backups/app.db-20261103-020800.bak
```

To restore it: stop the backend, copy the `.bak` over `backend/app.db`, and restart. No backups or live databases are committed to Git.

Note: the reset wiped all accounts; two integration-test accounts created during verification remain (`janedoe1793651991350`, `bobby1793651992538`, `*.example.com`). They do not block any new registration.

## API Documentation

See `backend/API.md` for the complete API contract, including request/response shapes for auth and expenses.

## Testing

Run the backend test suite (uses an isolated in-memory SQLite database; `app.db` is untouched):
```bash
cd backend
source .venv/bin/activate
pytest -q
```

Production build (output in `frontend/dist/`):
```bash
cd frontend
npm run build
```

Both are verified green as of 2026-11-03 (21 backend tests; Vite build succeeds).

## Implementation History

- **2026-11-02:** Fixed CORS preflight (`OPTIONS /api/auth/register 405`) by adding `CORSMiddleware`; switched the frontend to relative `/api` URLs through the Vite proxy (root cause of "NetworkError" in the browser).
- **2026-11-03:** Fixed the login 422 — backend now expects a JSON `{username, password}` body and the frontend sends JSON consistently (it previously sent multipart FormData with a JSON content-type). Login resolves email **or** username. Added readable validation/network error rendering.
- **2026-11-03:** Fixed protected-route `Authorization` stripping (collection paths now match `/api/expenses/`, avoiding a cross-origin 307 redirect); fixed the dashboard 422 caused by empty-string filter query params.
- **2026-11-03:** Repaired the test suite (httpx 0.27.2 pin, JSON login payloads, conftest in-memory `client` fixture with `StaticPool`); added email-login and amount-validation tests — 21 tests green.
- **2026-11-03:** Backed up and reset the user database per user authorization (`backups/app.db-20261103-020800.bak`), preserving the schema.
- **2026-11-03:** Implemented manual expense entry: dashboard **+ Add Expense** modal, shared category list (`constants.js`), instant list/totals/summary refresh, strict user isolation, `amount > 0` validation on both client and server.
- **2026-11-03:** Documented everything in `README.md` and `backend/API.md`.
