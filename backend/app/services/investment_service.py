from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.investment_repo import (
    get_investments_by_user,
    get_investment_by_id,
    create_investment,
    delete_investment,
    get_latest_price,
    get_price_history
)
from app.schemas.investment import InvestmentCreate

def get_all_investments(db: Session, user_id: int):
    return get_investments_by_user(db, user_id)

def get_single_investment(db: Session, investment_id: int, user_id: int):
    investment = get_investment_by_id(db, investment_id, user_id)
    if not investment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    return investment

def create_new_investment(db: Session, investment: InvestmentCreate, user_id: int):
    return create_investment(db, investment, user_id)

def delete_existing_investment(db: Session, investment_id: int, user_id: int):
    result = delete_investment(db, investment_id, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investment not found"
        )
    return {"message": "Investment deleted successfully"}

def get_portfolio_performance(db: Session, user_id: int):
    investments = get_investments_by_user(db, user_id)
    if not investments:
        return {
            "total_invested": 0,
            "current_value": 0,
            "gain_loss_eur": 0,
            "gain_loss_percent": 0,
            "current_price": 0,
            "total_units": 0
        }

    latest_price_snapshot = get_latest_price(db)
    current_price = latest_price_snapshot.price_eur if latest_price_snapshot else 0

    total_invested = sum(i.amount_invested_eur + i.fees for i in investments)
    total_units = sum(i.units_purchased for i in investments)
    current_value = total_units * current_price
    gain_loss_eur = current_value - total_invested
    gain_loss_percent = (gain_loss_eur / total_invested * 100) if total_invested > 0 else 0

    return {
        "total_invested": round(total_invested, 2),
        "current_value": round(current_value, 2),
        "gain_loss_eur": round(gain_loss_eur, 2),
        "gain_loss_percent": round(gain_loss_percent, 2),
        "current_price": round(current_price, 2),
        "total_units": round(total_units, 4)
    }

def get_performance_by_source(db: Session, user_id: int):
    investments = get_investments_by_user(db, user_id)
    if not investments:
        return []

    latest_price_snapshot = get_latest_price(db)
    current_price = latest_price_snapshot.price_eur if latest_price_snapshot else 0

    sources = {}
    for inv in investments:
        source = inv.funding_source
        if source not in sources:
            sources[source] = {
                "funding_source": source,
                "amount_invested": 0,
                "units": 0,
                "fees": 0
            }
        sources[source]["amount_invested"] += inv.amount_invested_eur
        sources[source]["units"] += inv.units_purchased
        sources[source]["fees"] += inv.fees

    result = []
    for source, data in sources.items():
        current_value = data["units"] * current_price
        total_cost = data["amount_invested"] + data["fees"]
        gain_loss_eur = current_value - total_cost
        gain_loss_percent = (gain_loss_eur / total_cost * 100) if total_cost > 0 else 0
        result.append({
            "funding_source": source,
            "amount_invested": round(total_cost, 2),
            "current_value": round(current_value, 2),
            "gain_loss_eur": round(gain_loss_eur, 2),
            "gain_loss_percent": round(gain_loss_percent, 2)
        })

    return result

def get_current_price(db: Session):
    snapshot = get_latest_price(db)
    if not snapshot:
        return {"price": None, "message": "No price data available yet"}
    return {
        "ticker": snapshot.ticker,
        "price_eur": snapshot.price_eur,
        "fetched_at": snapshot.fetched_at
    }

def get_price_snapshots(db: Session, limit: int = 100):
    return get_price_history(db, limit)