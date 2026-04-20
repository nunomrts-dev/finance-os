from sqlalchemy.orm import Session
from app.models.networth_snapshot import NetWorthSnapshot

def get_networth_history(db: Session, user_id: int, limit: int = 30):
    return db.query(NetWorthSnapshot).filter(
        NetWorthSnapshot.user_id == user_id
    ).order_by(NetWorthSnapshot.snapshot_date.desc()).limit(limit).all()

def get_latest_networth(db: Session, user_id: int):
    return db.query(NetWorthSnapshot).filter(
        NetWorthSnapshot.user_id == user_id
    ).order_by(NetWorthSnapshot.snapshot_date.desc()).first()