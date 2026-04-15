from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional
from datetime import datetime
from app.models.transaction import Transaction
from app.models.account import Account
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def get_transactions(
    db: Session,
    user_id: int,
    type: Optional[str] = None,
    category_id: Optional[int] = None,
    account_id: Optional[int] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
):
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    if type:
        query = query.filter(Transaction.type == type)
    if category_id:
        query = query.filter(Transaction.category_id == category_id)
    if account_id:
        query = query.filter(Transaction.account_id == account_id)
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    return query.order_by(Transaction.date.desc()).all()

def get_transaction_by_id(db: Session, transaction_id: int, user_id: int):
    return db.query(Transaction).filter(
        Transaction.id == transaction_id,
        Transaction.user_id == user_id
    ).first()

def create_transaction(db: Session, transaction: TransactionCreate, user_id: int):
    db_transaction = Transaction(
        user_id=user_id,
        account_id=transaction.account_id,
        category_id=transaction.category_id,
        type=transaction.type,
        amount=transaction.amount,
        currency=transaction.currency,
        description=transaction.description,
        notes=transaction.notes,
        date=transaction.date,
        is_recurring=transaction.is_recurring,
        recurring_frequency=transaction.recurring_frequency
    )
    db.add(db_transaction)
    account = db.query(Account).filter(Account.id == transaction.account_id).first()
    if account:
        if transaction.type == "IN":
            account.current_balance += transaction.amount
        else:
            account.current_balance -= transaction.amount
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, user_id: int, updates: TransactionUpdate):
    db_transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not db_transaction:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_transaction, key, value)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int, user_id: int):
    db_transaction = get_transaction_by_id(db, transaction_id, user_id)
    if not db_transaction:
        return None
    account = db.query(Account).filter(Account.id == db_transaction.account_id).first()
    if account:
        if db_transaction.type == "IN":
            account.current_balance -= db_transaction.amount
        else:
            account.current_balance += db_transaction.amount
    db.delete(db_transaction)
    db.commit()
    return True