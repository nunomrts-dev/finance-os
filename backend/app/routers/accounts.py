from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.account import AccountCreate, AccountUpdate, AccountResponse
from app.services.account_service import (
    get_all_accounts,
    get_account,
    create_new_account,
    update_existing_account,
    delete_existing_account,
    get_accounts_summary
)
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/accounts", tags=["Accounts"])

@router.get("", response_model=List[AccountResponse])
def list_accounts(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_all_accounts(db, current_user.id)

@router.post("", response_model=AccountResponse, status_code=201)
def create_account(
    account: AccountCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_new_account(db, account, current_user.id)

@router.get("/summary")
def accounts_summary(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_accounts_summary(db, current_user.id)

@router.get("/{account_id}", response_model=AccountResponse)
def get_single_account(
    account_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_account(db, account_id, current_user.id)

@router.put("/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    updates: AccountUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return update_existing_account(db, account_id, current_user.id, updates)

@router.delete("/{account_id}")
def delete_account(
    account_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return delete_existing_account(db, account_id, current_user.id)