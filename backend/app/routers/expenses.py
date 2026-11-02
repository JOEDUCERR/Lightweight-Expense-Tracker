from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from typing import List, Optional
from app import models, schemas
from app.database import get_db
from app.auth import get_current_user
import datetime

router = APIRouter(
    prefix="/expenses",
    tags=["expenses"],
)

@router.post("/", response_model=schemas.Expense)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Create a new expense for the current user"""
    db_expense = models.Expense(**expense.model_dump(), user_id=current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.get("/", response_model=schemas.ExpensesResponse)
def read_expenses(
    skip: int = 0, 
    limit: int = 100,
    title: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    description: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[datetime.date] = None,
    end_date: Optional[datetime.date] = None,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Get all expenses for the current user with filtering, pagination, and summary"""
    # Start building the query
    query = db.query(models.Expense).filter(models.Expense.user_id == current_user.id)
    
    # Apply filters
    if title:
        query = query.filter(models.Expense.title.contains(title))
    if min_amount is not None:
        query = query.filter(models.Expense.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(models.Expense.amount <= max_amount)
    if description:
        query = query.filter(models.Expense.description.contains(description))
    if category:
        query = query.filter(models.Expense.category == category)
    if start_date:
        query = query.filter(models.Expense.expense_date >= start_date)
    if end_date:
        query = query.filter(models.Expense.expense_date <= end_date)
    
    # Get expenses with pagination
    expenses = query.offset(skip).limit(limit).all()
    
    # Calculate summary statistics
    summary_query = db.query(
        func.count(models.Expense.id).label("total_count"),
        func.sum(models.Expense.amount).label("total_amount"),
        func.avg(models.Expense.amount).label("average_amount")
    ).filter(models.Expense.user_id == current_user.id)
    
    # Apply same filters to summary query
    if title:
        summary_query = summary_query.filter(models.Expense.title.contains(title))
    if min_amount is not None:
        summary_query = summary_query.filter(models.Expense.amount >= min_amount)
    if max_amount is not None:
        summary_query = summary_query.filter(models.Expense.amount <= max_amount)
    if description:
        summary_query = summary_query.filter(models.Expense.description.contains(description))
    if category:
        summary_query = summary_query.filter(models.Expense.category == category)
    if start_date:
        summary_query = summary_query.filter(models.Expense.expense_date >= start_date)
    if end_date:
        summary_query = summary_query.filter(models.Expense.expense_date <= end_date)
    
    summary_result = summary_query.first()
    
    # Prepare summary data
    summary = schemas.ExpenseSummary(
        total_count=summary_result.total_count if summary_result.total_count else 0,
        total_amount=summary_result.total_amount if summary_result.total_amount else 0.0,
        average_amount=summary_result.average_amount if summary_result.average_amount else 0.0
    )
    
    return schemas.ExpensesResponse(expenses=expenses, summary=summary)

@router.get("/monthly-summary", response_model=dict)
def read_monthly_summary(
    year: Optional[int] = None,
    month: Optional[int] = None,
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """Get monthly summary of expenses for the current user"""
    # Start building the query
    query = db.query(
        func.extract('month', models.Expense.expense_date).label('month'),
        func.extract('year', models.Expense.expense_date).label('year'),
        func.count(models.Expense.id).label('count'),
        func.sum(models.Expense.amount).label('total_amount'),
        func.avg(models.Expense.amount).label('average_amount')
    ).filter(models.Expense.user_id == current_user.id)
    
    # Apply year/month filters if provided
    if year:
        query = query.filter(func.extract('year', models.Expense.expense_date) == year)
    if month:
        query = query.filter(func.extract('month', models.Expense.expense_date) == month)
    
    # Group by month and year
    query = query.group_by(func.extract('month', models.Expense.expense_date), func.extract('year', models.Expense.expense_date))
    
    # Order by year and month
    query = query.order_by(func.extract('year', models.Expense.expense_date), func.extract('month', models.Expense.expense_date))
    
    results = query.all()
    
    # Format the response
    monthly_summary = []
    for result in results:
        monthly_summary.append({
            'year': int(result.year),
            'month': int(result.month),
            'count': result.count,
            'total_amount': float(result.total_amount) if result.total_amount else 0.0,
            'average_amount': float(result.average_amount) if result.average_amount else 0.0
        })
    
    return {"monthly_summary": monthly_summary}

@router.get("/{expense_id}", response_model=schemas.Expense)
def read_expense(expense_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Get a specific expense by ID for the current user"""
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == current_user.id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense

@router.put("/{expense_id}", response_model=schemas.Expense)
def update_expense(expense_id: int, expense: schemas.ExpenseCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Update a specific expense by ID for the current user"""
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == current_user.id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    # Update expense fields
    for key, value in expense.model_dump().items():
        setattr(db_expense, key, value)
    
    db.commit()
    db.refresh(db_expense)
    return db_expense

@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """Delete a specific expense by ID for the current user"""
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == current_user.id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    
    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}