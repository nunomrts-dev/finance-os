from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False)
    price_eur = Column(Float, nullable=False)
    market_open = Column(Boolean, default=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())