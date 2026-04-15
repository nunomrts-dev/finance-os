from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Investment(Base):
    __tablename__ = "investments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount_invested_eur = Column(Float, nullable=False)
    cspx_price_at_purchase = Column(Float, nullable=False)
    units_purchased = Column(Float, nullable=False)
    fees = Column(Float, default=0.0)
    funding_source = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="investments")