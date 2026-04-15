from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

DEFAULT_CATEGORIES = [
    {"name": "Housing", "type": "EXPENSE"},
    {"name": "Utilities", "type": "EXPENSE"},
    {"name": "Groceries", "type": "EXPENSE"},
    {"name": "Transport", "type": "EXPENSE"},
    {"name": "Health", "type": "EXPENSE"},
    {"name": "Insurance", "type": "EXPENSE"},
    {"name": "Subscriptions", "type": "EXPENSE"},
    {"name": "Dining Out", "type": "EXPENSE"},
    {"name": "Clothing", "type": "EXPENSE"},
    {"name": "Personal Care", "type": "EXPENSE"},
    {"name": "Education", "type": "EXPENSE"},
    {"name": "Entertainment", "type": "EXPENSE"},
    {"name": "Travel", "type": "EXPENSE"},
    {"name": "Fees and Taxes", "type": "EXPENSE"},
    {"name": "Other Expense", "type": "EXPENSE"},
    {"name": "Salary", "type": "INCOME"},
    {"name": "Vinted Sales", "type": "INCOME"},
    {"name": "Resale", "type": "INCOME"},
    {"name": "Girlfriend Contribution", "type": "INCOME"},
    {"name": "Freelance", "type": "INCOME"},
    {"name": "Cashback", "type": "INCOME"},
    {"name": "Found Money", "type": "INCOME"},
    {"name": "Bonus", "type": "INCOME"},
    {"name": "Other Income", "type": "INCOME"},
]

def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(
        (Category.user_id == user_id) | (Category.is_default == True)
    ).all()

def get_category_by_id(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def create_category(db: Session, category: CategoryCreate, user_id: int):
    db_category = Category(
        user_id=user_id,
        name=category.name,
        type=category.type,
        color=category.color,
        icon=category.icon,
        is_default=False
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, category_id: int, updates: CategoryUpdate):
    db_category = get_category_by_id(db, category_id)
    if not db_category:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, category_id: int):
    db_category = get_category_by_id(db, category_id)
    if not db_category or db_category.is_default:
        return None
    db.delete(db_category)
    db.commit()
    return True

def seed_default_categories(db: Session):
    existing = db.query(Category).filter(Category.is_default == True).first()
    if existing:
        return
    for cat in DEFAULT_CATEGORIES:
        db_category = Category(
            name=cat["name"],
            type=cat["type"],
            is_default=True
        )
        db.add(db_category)
    db.commit()