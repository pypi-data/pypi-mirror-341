import sqlite3
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pineaoth.database.db import DB_FILE
from pineaoth.core.utils import is_valid_base32
from rich.console import Console
from rich.table import Table

console = Console()

def add_account(service, username, secret):
    if not is_valid_base32(secret):
        console.print("❌ Secret key tidak valid! Harus dalam format Base32.", style="bold red")
        return
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO accounts (service, username, secret) VALUES (?, ?, ?)", 
              (service, username, secret))
    conn.commit()
    conn.close()
    console.print(f"✅ Akun {service} ({username}) berhasil ditambahkan!", style="bold green")

def list_accounts():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT service, username FROM accounts")
    accounts = c.fetchall()
    conn.close()
    
    if accounts:
        table = Table(title="📜 Daftar Akun OTP")
        table.add_column("Layanan", style="cyan")
        table.add_column("Username", style="magenta")
        for service, username in accounts:
            table.add_row(service, username)
        console.print(table)
    else:
        console.print("⚠️ Tidak ada akun yang tersimpan!", style="bold yellow")

def delete_account(service, username):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM accounts WHERE service = ? AND username = ?", (service, username))
    conn.commit()
    conn.close()
    console.print(f"❌ Akun {service} ({username}) berhasil dihapus!", style="bold red")
