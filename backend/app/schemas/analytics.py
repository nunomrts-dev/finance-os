from pydantic import BaseModel
from typing import List
from datetime import datetime

class SpendingByCategory(BaseModel):
    category_name: str
    total_amount: float
    percentage: float

class IncomeBySource(BaseModel):
    category_name: str
    total_amount: float
    percentage: float

class CashflowPoint(BaseModel):
    date: datetime
    income: float
    expenses: float
    net: float

class MonthlySummary(BaseModel):
    month: str
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: float

class NetWorthPoint(BaseModel):
    date: datetime
    bank_balance: float
    investment_value: float
    total: float

class AnalyticsDashboard(BaseModel):
    total_balance: float
    monthly_income: float
    monthly_expenses: float
    savings_rate: float
    spending_by_category: List[SpendingByCategory]
    cashflow: List[CashflowPoint]