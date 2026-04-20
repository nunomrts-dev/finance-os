from sqlalchemy.orm import Session
from app.repositories.networth_repo import get_networth_history, get_latest_networth
from app.repositories.account_repo import get_total_balance, get_accounts_by_user
from app.repositories.investment_repo import get_investments_by_user, get_latest_price

def get_current_networth(db: Session, user_id: int):
    latest_price = get_latest_price(db)
    current_price = latest_price.price_eur if latest_price else 0

    bank_balance = get_total_balance(db, user_id)
    investments = get_investments_by_user(db, user_id)
    total_units = sum(i.units_purchased for i in investments)
    investment_value = round(total_units * current_price, 2)
    total = round(bank_balance + investment_value, 2)

    return {
        "bank_balance": round(bank_balance, 2),
        "investment_value": investment_value,
        "total_net_worth": total,
        "current_cspx_price": round(current_price, 2)
    }

def get_networth_trend(db: Session, user_id: int, limit: int = 30):
    snapshots = get_networth_history(db, user_id, limit)
    return [
        {
            "date": s.snapshot_date,
            "bank_balance": s.total_bank_balance,
            "investment_value": s.total_investment_value,
            "total": s.total_net_worth
        }
        for s in snapshots
    ]

def get_networth_breakdown(db: Session, user_id: int):
    accounts = get_accounts_by_user(db, user_id)
    latest_price = get_latest_price(db)
    current_price = latest_price.price_eur if latest_price else 0
    investments = get_investments_by_user(db, user_id)
    total_units = sum(i.units_purchased for i in investments)
    investment_value = round(total_units * current_price, 2)

    account_breakdown = [
        {
            "account_name": a.name,
            "account_type": a.type,
            "balance": a.current_balance
        }
        for a in accounts
    ]

    return {
        "accounts": account_breakdown,
        "total_bank_balance": round(sum(a.current_balance for a in accounts), 2),
        "investment_value": investment_value,
        "total_units": round(total_units, 4),
        "current_cspx_price": round(current_price, 2)
    }