from database.db import create_tables
from portfolio.tracker import PortfolioTracker

create_tables()

tracker = PortfolioTracker()

tracker.add_stock(
    symbol="TCS.NS",
    quantity=10,
    buy_price=2000,
    current_price=2161
)

tracker.add_stock(
    symbol="INFY.NS",
    quantity=5,
    buy_price=1500,
    current_price=1600
)

portfolio = tracker.get_portfolio()

print("\n===== PORTFOLIO =====\n")

for row in portfolio:
    print(row)