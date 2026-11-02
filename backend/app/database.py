from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create engine for SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_schema():
    """Non-destructive migration for an existing SQLite file.

    Base.metadata.create_all() only creates tables that do not exist yet;
    it never adds columns to tables that already exist. Older app.db files
    were created before the `category` and `expense_date` columns were
    introduced. This adds any missing columns in place, keeping all
    existing user data intact.
    """
    with engine.connect() as conn:
        columns = {row[1] for row in conn.execute(text("PRAGMA table_info(expenses)"))}
        if "category" not in columns:
            conn.execute(text("ALTER TABLE expenses ADD COLUMN category VARCHAR"))
        if "expense_date" not in columns:
            conn.execute(text("ALTER TABLE expenses ADD COLUMN expense_date DATE"))
        conn.commit()