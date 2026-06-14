from pathlib import Path

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
DATABASE_DIR = BASE_DIR / "database"
ASSETS_DIR = BASE_DIR / "assets"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)

# ----------------------------------------------------
# Database
# ----------------------------------------------------

DATABASE_NAME = "swing_trading.db"

DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

# ----------------------------------------------------
# Default Settings
# ----------------------------------------------------

DEFAULT_PERIOD = "1y"

DEFAULT_INTERVAL = "1d"

DEFAULT_STOCK = "TCS.NS"

# ----------------------------------------------------
# Technical Indicators
# ----------------------------------------------------

EMA_SHORT = 20

EMA_LONG = 50

RSI_PERIOD = 14

MACD_FAST = 12

MACD_SLOW = 26

MACD_SIGNAL = 9

# ----------------------------------------------------
# Scanner
# ----------------------------------------------------

MAX_SCAN_STOCKS = 500

# ----------------------------------------------------
# Risk Management
# ----------------------------------------------------

DEFAULT_RISK_PERCENT = 1

# ----------------------------------------------------
# Version
# ----------------------------------------------------

APP_NAME = "Swing Trading AI Pro"

VERSION = "1.0.0"