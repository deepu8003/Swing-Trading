from database.db import get_connection


class PortfolioTracker:

    def add_stock(
        self,
        symbol,
        quantity,
        buy_price,
        current_price
    ):

        pnl = (
            current_price - buy_price
        ) * quantity

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO portfolio(
                symbol,
                quantity,
                buy_price,
                current_price,
                pnl
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                symbol,
                quantity,
                buy_price,
                current_price,
                pnl
            )
        )

        conn.commit()
        conn.close()

    def get_portfolio(self):

        conn = get_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM portfolio
            """
        )

        data = cursor.fetchall()

        conn.close()

        return data