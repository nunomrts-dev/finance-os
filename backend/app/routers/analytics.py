from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.database import get_db
from app.services.analytics_service import (
    get_spending_analysis,
    get_income_analysis,
    get_cashflow_analysis,
    get_monthly_analysis,
    get_dashboard_summary
)
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/spending")
def spending_by_category(
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = datetime.utcnow().replace(day=1)
    if not end_date:
        end_date = datetime.utcnow()
    return get_spending_analysis(db, current_user.id, start_date, end_date)

@router.get("/income")
def income_by_source(
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = datetime.utcnow().replace(day=1)
    if not end_date:
        end_date = datetime.utcnow()
    return get_income_analysis(db, current_user.id, start_date, end_date)

@router.get("/cashflow")
def cashflow(
    start_date: datetime = Query(default=None),
    end_date: datetime = Query(default=None),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=180)
    if not end_date:
        end_date = datetime.utcnow()
    return get_cashflow_analysis(db, current_user.id, start_date, end_date)

@router.get("/monthly")
def monthly_summary(
    year: int = Query(default=None),
    month: int = Query(default=None),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    if not year:
        year = datetime.utcnow().year
    if not month:
        month = datetime.utcnow().month
    return get_monthly_analysis(db, current_user.id, year, month)

@router.get("/dashboard")
def dashboard_summary(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_dashboard_summary(db, current_user.id)