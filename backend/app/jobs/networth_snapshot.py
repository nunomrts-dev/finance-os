import logging
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.networth_snapshot import NetWorthSnapshot
from app.repositories.account_repo import get_total_balance
from app.jobs.price_fetcher import get_latest_price
from app.repositories.investment_repo import get_investments_by_user

logger = logging.getLogger(__name__)

def take_networth_snapshot(user_id: int):
    db: Session = SessionLocal()
    try:
        bank_balance = get_total_balance(db, user_id)
        investments = get_investments_by_user(db, user_id)
        latest_price = get_latest_price(db)
        current_price = latest_price.price_eur if latest_price else 0
        total_units = sum(i.units_purchased for i in investments)
        investment_value = total_units * current_price
        total_net_worth = bank_balance + investment_value

        snapshot = NetWorthSnapshot(
            user_id=user_id,
            total_bank_balance=bank_balance,
            total_investment_value=investment_value,
            total_net_worth=total_net_worth
        )
        db.add(snapshot)
        db.commit()
        logger.info(f"Net worth snapshot taken for user {user_id}: {total_net_worth} EUR")

    except Exception as e:
        logger.error(f"Failed to take net worth snapshot: {e}")
        db.rollback()
    finally:
        db.close()