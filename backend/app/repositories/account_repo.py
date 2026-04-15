from sqlalchemy.orm import Session
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate

def get_accounts_by_user(db: Session, user_id: int):
    return db.query(Account).filter(
        Account.user_id == user_id,
        Account.is_active == True
    ).all()

def get_account_by_id(db: Session, account_id: int, user_id: int):
    return db.query(Account).filter(
        Account.id == account_id,
        Account.user_id == user_id
    ).first()

def create_account(db: Session, account: AccountCreate, user_id: int):
    db_account = Account(
        user_id=user_id,
        name=account.name,
        type=account.type,
        currency=account.currency,
        current_balance=account.current_balance
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account(db: Session, account_id: int, user_id: int, updates: AccountUpdate):
    db_account = get_account_by_id(db, account_id, user_id)
    if not db_account:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_account, key, value)
    db.commit()
    db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_id: int, user_id: int):
    db_account = get_account_by_id(db, account_id, user_id)
    if not db_account:
        return None
    db_account.is_active = False
    db.commit()
    return db_account

def get_total_balance(db: Session, user_id: int):
    accounts = get_accounts_by_user(db, user_id)
    return sum(account.current_balance for account in accounts)