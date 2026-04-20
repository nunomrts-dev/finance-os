from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router
from app.models import User, Account, Category, Transaction, Budget, Investment, PriceSnapshot, NetWorthSnapshot, AuditLog
from app.routers.accounts import router as accounts_router
from app.routers.categories import router as categories_router
from app.routers.transactions import router as transactions_router
from app.routers.budgets import router as budgets_router
from app.middleware.logging_middleware import logging_middleware
from app.middleware.rate_limiter import rate_limit_middleware
from starlette.middleware.base import BaseHTTPMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from app.jobs.price_fetcher import fetch_cspx_price
from app.routers.investments import router as investments_router
from app.jobs.networth_snapshot import take_networth_snapshot
from app.routers.networth import router as networth_router
from app.routers.analytics import router as analytics_router
from app.routers.networth import router as networth_router

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

app.add_middleware(BaseHTTPMiddleware, dispatch=logging_middleware)
app.add_middleware(BaseHTTPMiddleware, dispatch=rate_limit_middleware)

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_cspx_price, "interval", hours=1)
scheduler.add_job(take_networth_snapshot, "cron", hour=23, minute=0, args=[2])
scheduler.start()

app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(categories_router)
app.include_router(transactions_router)
app.include_router(budgets_router)
app.include_router(investments_router)
app.include_router(networth_router)
app.include_router(networth_router)
app.include_router(analytics_router)

@app.get("/health")
def health_check():
    return {"status": "ok"}