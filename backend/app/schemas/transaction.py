from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    account_id: int
    category_id: Optional[int] = None
    type: str
    amount: float
    currency: str = "EUR"
    description: Optional[str] = None
    notes: Optional[str] = None
    date: datetime
    is_recurring: bool = False
    recurring_frequency: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseModel):
    category_id: Optional[int] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    date: Optional[datetime] = None
    is_recurring: Optional[bool] = None
    recurring_frequency: Optional[str] = None

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True