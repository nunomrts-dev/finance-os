from datetime import datetime
import pytz

def is_market_open() -> bool:
    london_tz = pytz.timezone("Europe/London")
    now = datetime.now(london_tz)
    
    if now.weekday() >= 5:
        return False
    
    market_open = now.replace(hour=8, minute=0, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=30, second=0, microsecond=0)
    
    return market_open <= now <= market_close