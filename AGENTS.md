# Expense Tracker
## Stack
- Backend: Python 3.11+, FastAPI, SQLAlchemy 2.x, SQLite (backend/app.db), Pydantic v2,
  PyJWT, bcrypt (use the bcrypt package directly, NOT passlib)
- Frontend: React + Vite, JavaScript (no TypeScript), react-router-dom, plain fetch.
  No UI library, no Tailwind.
- Tests: pytest + FastAPI TestClient, fresh in-memory SQLite per test
## Layout
backend/app/{main.py,database.py,models.py,schemas.py,auth.py,routers/}
backend/tests/
frontend/src/{api.js,App.jsx,pages/,components/}
API.md   <- source of truth for every endpoint
PLAN.md  <- phase checklist
## Commands
- Backend: cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt && uvicorn app.main:app --port 8100 --reload
- Tests: cd backend && pytest -q
- Frontend: cd frontend && npm install && npm run dev -- --port 5173 --host
## Rules
- Ports 8000, 8001, 3000 and 80 are used by other services. Use only 8100 and 5173.
- All backend routes are prefixed /api. Vite proxies /api to http://127.0.0.1:8100.
- API.md is the contract. Never change an endpoint without updating API.md first.
- Run the tests after every change. A phase is not done until pytest is green.
- Keep files under ~200 lines. One router per resource.
- Do not add dependencies that are not already listed without asking.
- No placeholder, stub or TODO code. Every endpoint must be fully implemented.
