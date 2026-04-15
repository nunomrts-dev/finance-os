from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class NetWorthSnapshot(Base):
    __tablename__ = "networth_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_bank_balance = Column(Float, nullable=False)
    total_investment_value = Column(Float, nullable=False)
    total_net_worth = Column(Float, nullable=False)
    snapshot_date = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="networth_snapshots")