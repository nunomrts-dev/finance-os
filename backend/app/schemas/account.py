from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AccountBase(BaseModel):
    name: str
    type: str
    currency: str = "EUR"
    current_balance: float = 0.0

class AccountCreate(AccountBase):
    pass

class AccountUpdate(BaseModel):
    name: Optional[str] = None
    current_balance: Optional[float] = None
    is_active: Optional[bool] = None

class AccountResponse(AccountBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True