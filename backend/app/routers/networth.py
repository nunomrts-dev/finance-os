from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.networth_service import (
    get_current_networth,
    get_networth_trend,
    get_networth_breakdown
)
from app.routers.auth import get_current_active_user

router = APIRouter(prefix="/networth", tags=["Net Worth"])

@router.get("/current")
def current_networth(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_current_networth(db, current_user.id)

@router.get("/history")
def networth_history(
    limit: int = Query(30),
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_networth_trend(db, current_user.id, limit)

@router.get("/breakdown")
def networth_breakdown(
    current_user=Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_networth_breakdown(db, current_user.id)