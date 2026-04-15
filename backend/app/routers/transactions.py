from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services.transaction_service import (
    get_all_transactions,
    get_single_transaction,
    create_new_transaction,
    update_existing_transaction,
    delete_existing_transaction
)
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("", response_model=List[TransactionResponse])
def list_transactions(
    type: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    account_id: Optional[int] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_all_transactions(
        db, current_user.id, type, category_id, account_id, start_date, end_date
    )

@router.post("", response_model=TransactionResponse, status_code=201)
def create_transaction(
    transaction: TransactionCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_new_transaction(db, transaction, current_user.id)

@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
    transaction_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_single_transaction(db, transaction_id, current_user.id)

@router.put("/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    updates: TransactionUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return update_existing_transaction(db, transaction_id, current_user.id, updates)

@router.delete("/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return delete_existing_transaction(db, transaction_id, current_user.id)