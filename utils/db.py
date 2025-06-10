import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, last_analysis INTEGER)"
    )
    conn.commit()
    conn.close()

def get_last_analysis(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT last_analysis FROM users WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def update_last_analysis(user_id: int, timestamp: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if get_last_analysis(user_id) is None:
        c.execute("INSERT INTO users (user_id, last_analysis) VALUES (?, ?)", (user_id, timestamp))
    else:
        c.execute("UPDATE users SET last_analysis = ? WHERE user_id = ?", (timestamp, user_id))
    conn.commit()
    conn.close()
