from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.category_repo import (
    get_categories,
    get_category_by_id,
    create_category,
    update_category,
    delete_category,
    seed_default_categories
)
from app.schemas.category import CategoryCreate, CategoryUpdate

def get_all_categories(db: Session, user_id: int):
    seed_default_categories(db)
    return get_categories(db, user_id)

def create_new_category(db: Session, category: CategoryCreate, user_id: int):
    return create_category(db, category, user_id)

def update_existing_category(db: Session, category_id: int, user_id: int, updates: CategoryUpdate):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    if category.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify default categories"
        )
    if category.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this category"
        )
    return update_category(db, category_id, updates)

def delete_existing_category(db: Session, category_id: int, user_id: int):
    category = get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found"
        )
    if category.is_default:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete default categories"
        )
    if category.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this category"
        )
    delete_category(db, category_id)
    return {"message": "Category deleted successfully"}