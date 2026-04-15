from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
from app.repositories.transaction_repo import (
    get_transactions,
    get_transaction_by_id,
    create_transaction,
    update_transaction,
    delete_transaction
)
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def get_all_transactions(
    db: Session,
    user_id: int,
    type: Optional[str] = None,
    category_id: Optional[int] = None,
    account_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    return get_transactions(db, user_id, type, category_id, account_id, start_date, end_date)

def get_single_transaction(db: Session, transaction_id: int, user_id: int):
    transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

def create_new_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    if transaction.type not in ["IN", "OUT"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Transaction type must be IN or OUT"
        )
    if transaction.amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Amount must be greater than zero"
        )
    return create_transaction(db, transaction, user_id)

def update_existing_transaction(db: Session, transaction_id: int, user_id: int, updates: TransactionUpdate):
    transaction = update_transaction(db, transaction_id, user_id, updates)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return transaction

def delete_existing_transaction(db: Session, transaction_id: int, user_id: int):
    result = delete_transaction(db, transaction_id, user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transaction not found"
        )
    return {"message": "Transaction deleted successfully"}