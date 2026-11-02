from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.database import engine, Base, ensure_schema
from app.routers import expenses, auth
from fastapi.middleware.cors import CORSMiddleware

# Create database tables
Base.metadata.create_all(bind=engine)
# Add columns missing from pre-existing app.db files (non-destructive)
ensure_schema()

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0",
    description="A simple expense tracking application with authentication"
)

# Add CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://20.20.20.152:5173", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with /api prefix
app.include_router(auth.router, prefix="/api")
app.include_router(expenses.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to Expense Tracker API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}