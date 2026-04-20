from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.transaction import Transaction
from app.models.category import Category

def get_spending_by_category(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    results = db.query(
        Category.name,
        func.sum(Transaction.amount).label("total")
    ).join(
        Transaction, Transaction.category_id == Category.id
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == "OUT",
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).group_by(Category.name).all()
    
    total_spending = sum(r.total for r in results)
    return [
        {
            "category_name": r.name,
            "total_amount": round(r.total, 2),
            "percentage": round((r.total / total_spending * 100), 2) if total_spending > 0 else 0
        }
        for r in results
    ]

def get_income_by_source(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    results = db.query(
        Category.name,
        func.sum(Transaction.amount).label("total")
    ).join(
        Transaction, Transaction.category_id == Category.id
    ).filter(
        Transaction.user_id == user_id,
        Transaction.type == "IN",
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).group_by(Category.name).all()

    total_income = sum(r.total for r in results)
    return [
        {
            "category_name": r.name,
            "total_amount": round(r.total, 2),
            "percentage": round((r.total / total_income * 100), 2) if total_income > 0 else 0
        }
        for r in results
    ]

def get_cashflow(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    results = db.query(
        func.date_trunc("month", Transaction.date).label("month"),
        Transaction.type,
        func.sum(Transaction.amount).label("total")
    ).filter(
        Transaction.user_id == user_id,
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).group_by("month", Transaction.type).order_by("month").all()

    cashflow = {}
    for r in results:
        month_str = r.month.strftime("%Y-%m")
        if month_str not in cashflow:
            cashflow[month_str] = {"date": month_str, "income": 0, "expenses": 0, "net": 0}
        if r.type == "IN":
            cashflow[month_str]["income"] = round(r.total, 2)
        else:
            cashflow[month_str]["expenses"] = round(r.total, 2)

    for month in cashflow.values():
        month["net"] = round(month["income"] - month["expenses"], 2)

    return list(cashflow.values())

def get_monthly_summary(db: Session, user_id: int, year: int, month: int):
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)

    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "IN",
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).scalar() or 0

    expenses = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id,
        Transaction.type == "OUT",
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).scalar() or 0

    savings = income - expenses
    savings_rate = round((savings / income * 100), 2) if income > 0 else 0

    return {
        "month": f"{year}-{str(month).zfill(2)}",
        "total_income": round(income, 2),
        "total_expenses": round(expenses, 2),
        "net_savings": round(savings, 2),
        "savings_rate": savings_rate
    }