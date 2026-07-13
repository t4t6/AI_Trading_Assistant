# ==========================================
# Asset Registry
# symbol   -> what the user/frontend sees and sends to the API
# source   -> which data provider to use (binance | yfinance)
# fetch    -> the symbol string that provider expects
# ==========================================

FOREX_MAJORS = [
    ("EURUSD", "Euro / US Dollar"),
    ("GBPUSD", "British Pound / US Dollar"),
    ("USDJPY", "US Dollar / Japanese Yen"),
    ("USDCHF", "US Dollar / Swiss Franc"),
    ("USDCAD", "US Dollar / Canadian Dollar"),
    ("AUDUSD", "Australian Dollar / US Dollar"),
    ("NZDUSD", "New Zealand Dollar / US Dollar"),
]

FOREX_MINORS = [
    ("EURGBP", "Euro / British Pound"),
    ("EURJPY", "Euro / Japanese Yen"),
    ("GBPJPY", "British Pound / Japanese Yen"),
    ("AUDJPY", "Australian Dollar / Japanese Yen"),
    ("CHFJPY", "Swiss Franc / Japanese Yen"),
    ("EURAUD", "Euro / Australian Dollar"),
    ("GBPAUD", "British Pound / Australian Dollar"),
    ("EURCAD", "Euro / Canadian Dollar"),
    ("GBPCAD", "British Pound / Canadian Dollar"),
    ("AUDCAD", "Australian Dollar / Canadian Dollar"),
    ("AUDCHF", "Australian Dollar / Swiss Franc"),
    ("CADCHF", "Canadian Dollar / Swiss Franc"),
    ("EURNZD", "Euro / New Zealand Dollar"),
    ("GBPNZD", "British Pound / New Zealand Dollar"),
    ("NZDJPY", "New Zealand Dollar / Japanese Yen"),
]

COMMODITIES = [
    ("XAUUSD", "Gold"),
    ("XAGUSD", "Silver"),
    ("WTIUSD", "Crude Oil (WTI)"),
    ("BRENTUSD", "Brent Oil"),
    ("NGASUSD", "Natural Gas"),
    ("COPPERUSD", "Copper"),
]

CRYPTO = [
    ("BTCUSDT", "Bitcoin"),
    ("ETHUSDT", "Ethereum"),
    ("BNBUSDT", "Binance Coin"),
    ("SOLUSDT", "Solana"),
    ("XRPUSDT", "Ripple"),
    ("ADAUSDT", "Cardano"),
    ("DOGEUSDT", "Dogecoin"),
    ("TRXUSDT", "Tron"),
    ("AVAXUSDT", "Avalanche"),
    ("LINKUSDT", "Chainlink"),
    ("DOTUSDT", "Polkadot"),
    ("LTCUSDT", "Litecoin"),
]

FAVORITES_DEFAULT = ["EURUSD", "GBPUSD", "XAUUSD", "BTCUSDT", "ETHUSDT"]

# Maps our display symbol -> (source, fetch_symbol)
# source "binance": live via Binance public REST (no key, truly real-time)
# source "yfinance": via Yahoo Finance (free, ~15min effective delay on many symbols)
SYMBOL_MAP = {}

for sym, desc in FOREX_MAJORS + FOREX_MINORS:
    SYMBOL_MAP[sym] = {"source": "yfinance", "fetch": f"{sym}=X", "market": "FOREX", "description": desc}

_COMMODITY_YF = {
    "XAUUSD": "GC=F",
    "XAGUSD": "SI=F",
    "WTIUSD": "CL=F",
    "BRENTUSD": "BZ=F",
    "NGASUSD": "NG=F",
    "COPPERUSD": "HG=F",
}
for sym, desc in COMMODITIES:
    SYMBOL_MAP[sym] = {"source": "yfinance", "fetch": _COMMODITY_YF[sym], "market": "COMMODITY", "description": desc}

for sym, desc in CRYPTO:
    SYMBOL_MAP[sym] = {"source": "binance", "fetch": sym, "market": "CRYPTO", "description": desc}


def get_asset_info(symbol):
    return SYMBOL_MAP.get(symbol.upper())


def all_assets_grouped():
    return {
        "forex_majors": [{"symbol": s, "description": d} for s, d in FOREX_MAJORS],
        "forex_minors": [{"symbol": s, "description": d} for s, d in FOREX_MINORS],
        "commodities": [{"symbol": s, "description": d} for s, d in COMMODITIES],
        "crypto": [{"symbol": s, "description": d} for s, d in CRYPTO],
        "favorites": FAVORITES_DEFAULT,
    }
