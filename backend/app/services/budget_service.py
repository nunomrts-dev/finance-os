from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.repositories.budget_repo import (
    get_budgets_by_user,
    get_budget_by_id,
    create_budget,
    update_budget,
    delete_budget,
    get_budget_spent
)
from app.schemas.budget import BudgetCreate, BudgetUpdate

def get_all_budgets(db: Session, user_id: int):
    return get_budgets_by_user(db, user_id)

def get_single_budget(db: Session, budget_id: int, user_id: int):
    budget = get_budget_by_id(db, budget_id, user_id)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return budget

def create_new_budget(db: Session, budget: BudgetCreate, user_id: int):
    return create_budget(db, budget, user_id)

def update_existing_budget(db: Session, budget_id: int, user_id: int, updates: BudgetUpdate):
    budget = update_budget(db, budget_id, user_id, updates)
    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return budget

def delete_existing_budget(db: Session, budget_id: int, user_id: int):
    result = delete_budget(db, budget_id, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Budget not found"
        )
    return {"message": "Budget deleted successfully"}

def get_budgets_status(db: Session, user_id: int):
    budgets = get_budgets_by_user(db, user_id)
    status_list = []
    for budget in budgets:
        end_date = budget.end_date or datetime.utcnow()
        spent = get_budget_spent(
            db, user_id, budget.category_id,
            budget.start_date, end_date
        )
        percent_used = (spent / budget.amount_limit * 100) if budget.amount_limit > 0 else 0
        status_list.append({
            "budget_id": budget.id,
            "category_id": budget.category_id,
            "amount_limit": budget.amount_limit,
            "amount_spent": spent,
            "amount_remaining": budget.amount_limit - spent,
            "percent_used": round(percent_used, 2),
            "alert_at_percent": budget.alert_at_percent,
            "is_over_budget": percent_used > 100,
            "is_near_limit": percent_used >= budget.alert_at_percent
        })
    return status_list