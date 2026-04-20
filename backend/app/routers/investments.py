from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.investment import InvestmentCreate, InvestmentResponse
from app.services.investment_service import (
    get_all_investments,
    get_single_investment,
    create_new_investment,
    delete_existing_investment,
    get_portfolio_performance,
    get_performance_by_source,
    get_current_price,
    get_price_snapshots
)
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/investments", tags=["Investments"])

@router.get("", response_model=List[InvestmentResponse])
def list_investments(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_all_investments(db, current_user.id)

@router.post("", response_model=InvestmentResponse, status_code=201)
def create_investment(
    investment: InvestmentCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_new_investment(db, investment, current_user.id)

@router.get("/performance")
def portfolio_performance(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_portfolio_performance(db, current_user.id)

@router.get("/performance/by-source")
def performance_by_source(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_performance_by_source(db, current_user.id)

@router.get("/price/current")
def current_price(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_current_price(db)

@router.get("/price/history")
def price_history(
    limit: int = Query(100),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_price_snapshots(db, limit)

@router.get("/{investment_id}", response_model=InvestmentResponse)
def get_investment(
    investment_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_single_investment(db, investment_id, current_user.id)

@router.delete("/{investment_id}")
def delete_investment(
    investment_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return delete_existing_investment(db, investment_id, current_user.id)