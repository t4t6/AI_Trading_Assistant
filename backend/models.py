from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime

from database import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    market_type = Column(String, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class WatchlistItem(Base):
    __tablename__ = "watchlist"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, nullable=False)
    market_type = Column(String, nullable=False)
    added_at = Column(DateTime, default=datetime.utcnow)


class SignalHistory(Base):
    __tablename__ = "signal_history"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    timeframe = Column(String, nullable=False)
    signal = Column(String)
    confidence = Column(Float)
    entry = Column(Float)
    stop_loss = Column(Float)
    take_profit_1 = Column(Float)
    take_profit_2 = Column(Float)
    take_profit_3 = Column(Float)
    next_candle = Column(String)
    trend = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
