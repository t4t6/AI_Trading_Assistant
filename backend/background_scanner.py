import threading
import time
import logging

from signal_engine import SignalEngine
from database import SessionLocal
import models

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s")

SCAN_INTERVAL_SECONDS = 900  # 15 minutes — keeps well inside free data-provider limits
SCAN_TIMEFRAME = "1h"


class BackgroundScanner:
    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self.scan_loop, daemon=True)
        self.thread.start()
        logging.info("Background watchlist scanner started")

    def stop(self):
        self.running = False

    def scan_loop(self):
        while self.running:
            try:
                self.scan_watchlist()
            except Exception as e:
                logging.error(f"Scan loop error: {e}")
            time.sleep(SCAN_INTERVAL_SECONDS)

    def scan_watchlist(self):
        db = SessionLocal()
        try:
            symbols = [w.symbol for w in db.query(models.WatchlistItem).all()]

            for symbol in symbols:
                try:
                    result = SignalEngine.generate(symbol, SCAN_TIMEFRAME, include_alignment=False)
                    if not result.get("status"):
                        continue

                    entry = models.SignalHistory(
                        symbol=result["symbol"],
                        timeframe=result["timeframe"],
                        signal=result["signal"],
                        confidence=result["confidence"],
                        entry=result["entry"],
                        stop_loss=result["stop_loss"],
                        take_profit_1=result["take_profit_1"],
                        take_profit_2=result["take_profit_2"],
                        take_profit_3=result["take_profit_3"],
                        next_candle=result["next_candle"],
                        trend=result["trend"],
                    )
                    db.add(entry)
                    db.commit()

                    logging.info(f"{symbol} {result['signal']} {result['confidence']}%")
                except Exception as e:
                    logging.error(f"{symbol}: {e}")
        finally:
            db.close()


scanner = BackgroundScanner()
