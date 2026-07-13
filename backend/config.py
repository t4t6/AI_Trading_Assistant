# ==========================================
# AI Trading Assistant Configuration
# ==========================================

APP_NAME = "AI Trading Assistant"

APP_VERSION = "1.0.0"

DEFAULT_TIMEFRAME = "1h"

SUPPORTED_TIMEFRAMES = [

    "1m",

    "3m",

    "5m",

    "15m",

    "30m",

    "1h",

    "4h",

    "1d"

]

# ==========================================
# Scan Settings
# ==========================================

AUTO_REFRESH = True

REFRESH_SECONDS = {

    "1m": 30,

    "3m": 60,

    "5m": 120,

    "15m": 300,

    "30m": 600,

    "1h": 1800,

    "4h": 7200,

    "1d": 21600

}

# ==========================================
# Forex
# Yahoo Finance Symbols
# ==========================================

FOREX_PAIRS = [

    "EURUSD=X",

    "GBPUSD=X",

    "USDJPY=X",

    "USDCHF=X",

    "USDCAD=X",

    "AUDUSD=X",

    "NZDUSD=X",

    "EURGBP=X",

    "EURJPY=X",

    "GBPJPY=X",

    "AUDJPY=X",

    "CHFJPY=X",

    "EURAUD=X",

    "GBPAUD=X",

    "EURCAD=X",

    "GBPCAD=X",

    "AUDCAD=X",

    "AUDCHF=X",

    "CADCHF=X",

    "EURNZD=X",

    "GBPNZD=X",

    "AUDNZD=X",

    "NZDJPY=X",

    "NZDCAD=X",

    "NZDCHF=X"

]

# ==========================================
# Commodities
# ==========================================

COMMODITIES = [

    "GC=F",      # Gold

    "SI=F",      # Silver

    "CL=F",      # WTI Oil

    "BZ=F",      # Brent Oil

    "NG=F",      # Natural Gas

    "HG=F"       # Copper

]

# ==========================================
# Crypto
# ==========================================

CRYPTO = [

    "BTC-USD",

    "ETH-USD",

    "BNB-USD",

    "SOL-USD",

    "XRP-USD",

    "ADA-USD",

    "DOGE-USD",

    "TRX-USD",

    "AVAX-USD",

    "LINK-USD",

    "DOT-USD",

    "LTC-USD"

]

# ==========================================
# Favorites
# ==========================================

FAVORITES = [

    "EURUSD=X",

    "GBPUSD=X",

    "USDJPY=X",

    "GC=F",

    "BTC-USD",

    "ETH-USD"

]

# ==========================================
# Scanner
# ==========================================

SCAN_MARKETS = (

    FOREX_PAIRS +

    COMMODITIES +

    CRYPTO

)

# ==========================================
# Risk
# ==========================================

DEFAULT_RISK_PERCENT = 1.0

MIN_CONFIDENCE = 70

ALLOW_WAIT_SIGNAL = True

# ==========================================
# Binary Module
# ==========================================

ENABLE_BINARY_SIGNALS = True

BINARY_TIMEFRAMES = [

    "1m",

    "3m",

    "5m"

]

# ==========================================
# Notifications
# ==========================================

ENABLE_PUSH_NOTIFICATION = True

NOTIFY_STRONG_SIGNALS_ONLY = True

MIN_NOTIFICATION_CONFIDENCE = 85