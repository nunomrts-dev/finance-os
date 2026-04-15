from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.models import User, Account, Category, Transaction, Budget, Investment, PriceSnapshot, NetWorthSnapshot, AuditLog
from app.routers.accounts import router as accounts_router
from app.routers.categories import router as categories_router
from app.routers.transactions import router as transactions_router
from app.routers.budgets import router as budgets_router

app = FastAPI(
    title="Finance OS",
    description="Personal finance management system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(budgets_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}