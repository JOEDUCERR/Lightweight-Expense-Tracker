from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date

# Base schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    title: str
    # Expenses must have a positive amount; zero and negative values are rejected
    amount: float = Field(..., gt=0)
    description: Optional[str] = None
    category: Optional[str] = None
    expense_date: Optional[date] = None

class ExpenseCreate(ExpenseBase):
    pass

class Expense(ExpenseBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Response schemas for filtered/expenses with summary
class ExpenseSummary(BaseModel):
    total_count: int
    total_amount: float
    average_amount: float

class ExpensesResponse(BaseModel):
    expenses: List[Expense]
    summary: ExpenseSummary

# Token schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None