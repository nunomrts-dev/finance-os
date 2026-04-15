from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BudgetBase(BaseModel):
    category_id: int
    amount_limit: float
    period: str
    start_date: datetime
    end_date: Optional[datetime] = None
    alert_at_percent: float = 80.0

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BaseModel):
    amount_limit: Optional[float] = None
    alert_at_percent: Optional[float] = None
    end_date: Optional[datetime] = None

class BudgetResponse(BudgetBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True