from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationship with expenses
    expenses = relationship("Expense", back_populates="owner")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String)
    category = Column(String, index=True)
    expense_date = Column(Date, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship with user
    owner = relationship("User", back_populates="expenses")