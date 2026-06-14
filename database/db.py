import sqlite3


DB_NAME = "swingtrading.db"


def get_connection():

    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        buy_price REAL NOT NULL,
        current_price REAL NOT NULL,
        pnl REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()