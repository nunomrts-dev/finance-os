from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from app.services.budget_service import (
    get_all_budgets,
    get_single_budget,
    create_new_budget,
    update_existing_budget,
    delete_existing_budget,
    get_budgets_status
)
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/budgets", tags=["Budgets"])

@router.get("", response_model=List[BudgetResponse])
def list_budgets(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_all_budgets(db, current_user.id)

@router.post("", response_model=BudgetResponse, status_code=201)
def create_budget(
    budget: BudgetCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_new_budget(db, budget, current_user.id)

@router.get("/status")
def budgets_status(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_budgets_status(db, current_user.id)

@router.get("/{budget_id}", response_model=BudgetResponse)
def get_budget(
    budget_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_single_budget(db, budget_id, current_user.id)

@router.put("/{budget_id}", response_model=BudgetResponse)
def update_budget(
    budget_id: int,
    updates: BudgetUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return update_existing_budget(db, budget_id, current_user.id, updates)

@router.delete("/{budget_id}")
def delete_budget(
    budget_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return delete_existing_budget(db, budget_id, current_user.id)