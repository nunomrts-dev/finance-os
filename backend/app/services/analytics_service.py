from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.repositories.analytics_repo import (
    get_spending_by_category,
    get_income_by_source,
    get_cashflow,
    get_monthly_summary
)

def get_spending_analysis(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return get_spending_by_category(db, user_id, start_date, end_date)

def get_income_analysis(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return get_income_by_source(db, user_id, start_date, end_date)

def get_cashflow_analysis(db: Session, user_id: int, start_date: datetime, end_date: datetime):
    return get_cashflow(db, user_id, start_date, end_date)

def get_monthly_analysis(db: Session, user_id: int, year: int, month: int):
    return get_monthly_summary(db, user_id, year, month)

def get_dashboard_summary(db: Session, user_id: int):
    now = datetime.utcnow()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    monthly = get_monthly_summary(db, user_id, now.year, now.month)
    spending = get_spending_by_category(db, user_id, start_of_month, now)
    cashflow = get_cashflow(
        db, user_id,
        now - timedelta(days=180),
        now
    )

    return {
        "total_income_this_month": monthly["total_income"],
        "total_expenses_this_month": monthly["total_expenses"],
        "net_savings_this_month": monthly["net_savings"],
        "savings_rate_this_month": monthly["savings_rate"],
        "spending_by_category": spending,
        "cashflow_last_6_months": cashflow
    }