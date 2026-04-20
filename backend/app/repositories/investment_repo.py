from sqlalchemy.orm import Session
from app.models.investment import Investment
from app.models.price_snapshot import PriceSnapshot
from app.schemas.investment import InvestmentCreate

def get_investments_by_user(db: Session, user_id: int):
    return db.query(Investment).filter(
        Investment.user_id == user_id
    ).order_by(Investment.date.desc()).all()

def get_investment_by_id(db: Session, investment_id: int, user_id: int):
    return db.query(Investment).filter(
        Investment.id == investment_id,
        Investment.user_id == user_id
    ).first()

def create_investment(db: Session, investment: InvestmentCreate, user_id: int):
    db_investment = Investment(
        user_id=user_id,
        amount_invested_eur=investment.amount_invested_eur,
        cspx_price_at_purchase=investment.cspx_price_at_purchase,
        units_purchased=investment.units_purchased,
        fees=investment.fees,
        funding_source=investment.funding_source,
        notes=investment.notes,
        date=investment.date
    )
    db.add(db_investment)
    db.commit()
    db.refresh(db_investment)
    return db_investment

def delete_investment(db: Session, investment_id: int, user_id: int):
    db_investment = get_investment_by_id(db, investment_id, user_id)
    if not db_investment:
        return None
    db.delete(db_investment)
    db.commit()
    return True

def get_latest_price(db: Session):
    return db.query(PriceSnapshot).order_by(
        PriceSnapshot.fetched_at.desc()
    ).first()

def get_price_history(db: Session, limit: int = 100):
    return db.query(PriceSnapshot).order_by(
        PriceSnapshot.fetched_at.desc()
    ).limit(limit).all()
    