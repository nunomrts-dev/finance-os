from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InvestmentBase(BaseModel):
    amount_invested_eur: float
    cspx_price_at_purchase: float
    units_purchased: float
    fees: float = 0.0
    funding_source: str
    notes: Optional[str] = None
    date: datetime

class InvestmentCreate(InvestmentBase):
    pass

class InvestmentResponse(InvestmentBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class InvestmentPerformance(BaseModel):
    total_invested: float
    current_value: float
    gain_loss_eur: float
    gain_loss_percent: float
    current_price: float

class InvestmentSourceBreakdown(BaseModel):
    funding_source: str
    amount_invested: float
    current_value: float
    gain_loss_eur: float
    gain_loss_percent: float