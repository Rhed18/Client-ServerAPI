import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "orders.db"

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer TEXT,
            bw_pages INTEGER DEFAULT 0,
            color_pages INTEGER DEFAULT 0,
            photo_pages INTEGER DEFAULT 0,
            total REAL,
            status TEXT DEFAULT 'pending',
            created_at TEXT
        )
        """
    )
    conn.commit()
    conn.close()