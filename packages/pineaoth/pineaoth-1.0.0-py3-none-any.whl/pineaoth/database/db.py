import os
import sqlite3

def get_base_dir():
    return os.path.join(os.path.expanduser("~"), ".pineaoth")

DB_FILE = os.path.join(get_base_dir(), "accounts.db")

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT NOT NULL,
                    username TEXT NOT NULL,
                    secret TEXT NOT NULL)''')
    conn.commit()
    conn.close()
