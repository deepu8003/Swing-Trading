import streamlit as st

from database.db import create_tables
from portfolio.tracker import PortfolioTracker

create_tables()

tracker = PortfolioTracker()

st.title("💼 Portfolio")

symbol = st.text_input("Symbol")

quantity = st.number_input(
    "Quantity",
    min_value=1
)

buy_price = st.number_input(
    "Buy Price",
    min_value=0.0
)

current_price = st.number_input(
    "Current Price",
    min_value=0.0
)

if st.button("Add Stock"):

    tracker.add_stock(
        symbol,
        quantity,
        buy_price,
        current_price
    )

    st.success("Added")

portfolio = tracker.get_portfolio()

st.dataframe(portfolio)