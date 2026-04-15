from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.services.category_service import (
    get_all_categories,
    create_new_category,
    update_existing_category,
    delete_existing_category
)
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("", response_model=List[CategoryResponse])
def list_categories(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_all_categories(db, current_user.id)

@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(
    category: CategoryCreate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_new_category(db, category, current_user.id)

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    updates: CategoryUpdate,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return update_existing_category(db, category_id, current_user.id, updates)

@router.delete("/{category_id}")
def delete_category(
    category_id: int,
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return delete_existing_category(db, category_id, current_user.id)