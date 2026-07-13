import os

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine, Base, get_db
import models
from assets import all_assets_grouped, get_asset_info, SYMBOL_MAP
from signal_engine import SignalEngine
from config import SUPPORTED_TIMEFRAMES, BINARY_TIMEFRAMES
from background_scanner import scanner

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Trading Assistant API",
    version="1.1.0",
)

# Allow the PWA (served from any origin: file, github pages, etc.) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def start_background_scanner():
    scanner.start()


@app.get("/")
def home():
    return {"application": "AI Trading Assistant", "status": "Running"}


@app.get("/health")
def health():
    return {"status": "OK"}


@app.get("/timeframes")
def timeframes():
    return {"timeframes": SUPPORTED_TIMEFRAMES, "binary_timeframes": BINARY_TIMEFRAMES}


@app.get("/assets")
def assets():
    return all_assets_grouped()


# ============================================
# Signals
# ============================================

@app.get("/signal/{symbol}/{timeframe}")
def signal(symbol: str, timeframe: str):
    if timeframe not in SUPPORTED_TIMEFRAMES:
        return {"status": False, "message": "Unsupported timeframe."}

    if get_asset_info(symbol) is None:
        return {"status": False, "message": f"Unknown symbol '{symbol}'."}

    return SignalEngine.generate(symbol=symbol, timeframe=timeframe)


@app.post("/signals")
def multiple_signals(request: dict):
    symbols = request.get("symbols", [])
    timeframe = request.get("timeframe", "1h")

    result = []
    for sym in symbols:
        try:
            result.append(SignalEngine.generate(sym, timeframe, include_alignment=False))
        except Exception as e:
            result.append({"status": False, "symbol": sym, "message": str(e)})

    return result


@app.get("/binary/{symbol}/{timeframe}")
def binary_signal(symbol: str, timeframe: str):
    if timeframe not in BINARY_TIMEFRAMES:
        return {"status": False, "message": f"Binary trading supports timeframes: {BINARY_TIMEFRAMES}"}

    if get_asset_info(symbol) is None:
        return {"status": False, "message": f"Unknown symbol '{symbol}'."}

    return SignalEngine.generate_binary(symbol=symbol, timeframe=timeframe)


# ============================================
# Watchlist
# ============================================

@app.get("/watchlist")
def get_watchlist(db: Session = Depends(get_db)):
    items = db.query(models.WatchlistItem).order_by(models.WatchlistItem.symbol).all()
    return [{"symbol": i.symbol, "market_type": i.market_type} for i in items]


@app.post("/watchlist")
def add_to_watchlist(request: dict, db: Session = Depends(get_db)):
    symbol = request.get("symbol", "").upper()
    info = get_asset_info(symbol)

    if info is None:
        return {"status": False, "message": f"Unknown symbol '{symbol}'."}

    existing = db.query(models.WatchlistItem).filter(models.WatchlistItem.symbol == symbol).first()
    if existing:
        return {"status": True, "message": "Already in watchlist."}

    item = models.WatchlistItem(symbol=symbol, market_type=info["market"])
    db.add(item)
    db.commit()

    return {"status": True, "message": f"{symbol} added to watchlist."}


@app.delete("/watchlist/{symbol}")
def remove_from_watchlist(symbol: str, db: Session = Depends(get_db)):
    symbol = symbol.upper()
    item = db.query(models.WatchlistItem).filter(models.WatchlistItem.symbol == symbol).first()

    if not item:
        return {"status": False, "message": "Symbol not in watchlist."}

    db.delete(item)
    db.commit()

    return {"status": True, "message": f"{symbol} removed from watchlist."}


@app.get("/history/{symbol}")
def signal_history(symbol: str, limit: int = 50, db: Session = Depends(get_db)):
    rows = (
        db.query(models.SignalHistory)
        .filter(models.SignalHistory.symbol == symbol.upper())
        .order_by(models.SignalHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return [
        {
            "symbol": r.symbol,
            "timeframe": r.timeframe,
            "signal": r.signal,
            "confidence": r.confidence,
            "entry": r.entry,
            "stop_loss": r.stop_loss,
            "take_profit_1": r.take_profit_1,
            "take_profit_2": r.take_profit_2,
            "take_profit_3": r.take_profit_3,
            "next_candle": r.next_candle,
            "trend": r.trend,
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in rows
    ]


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
