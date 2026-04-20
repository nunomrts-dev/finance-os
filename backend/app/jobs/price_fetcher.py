import logging
import yfinance as yf
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.price_snapshot import PriceSnapshot
from app.utils.market_hours import is_market_open
from app.config import settings

logger = logging.getLogger(__name__)

def fetch_cspx_price():
    if not is_market_open():
        logger.info("Market is closed. Skipping price fetch.")
        return

    db: Session = SessionLocal()
    try:
        ticker = yf.Ticker(settings.cspx_ticker)
        data = ticker.history(period="1d", interval="1m")

        if data.empty:
            logger.warning("No price data returned from yfinance.")
            return

        latest_price = float(data["Close"].iloc[-1])

        snapshot = PriceSnapshot(
            ticker=settings.cspx_ticker,
            price_eur=latest_price,
            market_open=True
        )
        db.add(snapshot)
        db.commit()
        logger.info(f"CSPX price fetched: {latest_price} EUR")

    except Exception as e:
        logger.error(f"Failed to fetch CSPX price: {e}")
        db.rollback()
    finally:
        db.close()

def get_latest_price(db: Session):
    return db.query(PriceSnapshot).order_by(
        PriceSnapshot.fetched_at.desc()
    ).first()