from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.account_repo import (
    get_accounts_by_user,
    get_account_by_id,
    create_account,
    update_account,
    delete_account,
    get_total_balance
)
from app.schemas.account import AccountCreate, AccountUpdate

def get_all_accounts(db: Session, user_id: int):
    return get_accounts_by_user(db, user_id)

def get_account(db: Session, account_id: int, user_id: int):
    account = get_account_by_id(db, account_id, user_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account

def create_new_account(db: Session, account: AccountCreate, user_id: int):
    return create_account(db, account, user_id)

def update_existing_account(db: Session, account_id: int, user_id: int, updates: AccountUpdate):
    account = update_account(db, account_id, user_id, updates)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account

def delete_existing_account(db: Session, account_id: int, user_id: int):
    account = delete_account(db, account_id, user_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return {"message": "Account deleted successfully"}

def get_accounts_summary(db: Session, user_id: int):
    accounts = get_accounts_by_user(db, user_id)
    total = get_total_balance(db, user_id)
    return {
        "accounts": accounts,
        "total_balance": total,
        "account_count": len(accounts)
    }