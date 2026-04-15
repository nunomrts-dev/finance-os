from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.models.budget import Budget
from app.models.transaction import Transaction
from app.schemas.budget import BudgetCreate, BudgetUpdate

def get_budgets_by_user(db: Session, user_id: int):
    return db.query(Budget).filter(Budget.user_id == user_id).all()

def get_budget_by_id(db: Session, budget_id: int, user_id: int):
    return db.query(Budget).filter(
        Budget.id == budget_id,
        Budget.user_id == user_id
    ).first()

def create_budget(db: Session, budget: BudgetCreate, user_id: int):
    db_budget = Budget(
        user_id=user_id,
        category_id=budget.category_id,
        amount_limit=budget.amount_limit,
        period=budget.period,
        start_date=budget.start_date,
        end_date=budget.end_date,
        alert_at_percent=budget.alert_at_percent
    )
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def update_budget(db: Session, budget_id: int, user_id: int, updates: BudgetUpdate):
    db_budget = get_budget_by_id(db, budget_id, user_id)
    if not db_budget:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_budget, key, value)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def delete_budget(db: Session, budget_id: int, user_id: int):
    db_budget = get_budget_by_id(db, budget_id, user_id)
    if not db_budget:
        return None
    db.delete(db_budget)
    db.commit()
    return True

def get_budget_spent(db: Session, user_id: int, category_id: int, start_date: datetime, end_date: datetime):
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id,
        Transaction.category_id == category_id,
        Transaction.type == "OUT",
        Transaction.date >= start_date,
        Transaction.date <= end_date
    ).all()
    return sum(t.amount for t in transactions)