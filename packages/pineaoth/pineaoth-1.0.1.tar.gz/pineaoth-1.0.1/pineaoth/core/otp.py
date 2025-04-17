import os
import time
import sqlite3
import pyotp
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from rich.console import Console
from rich.table import Table
from pineaoth.database.db import DB_FILE

console = Console()

def show_live_otp():
    while True:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT service, username, secret FROM accounts")
        accounts = c.fetchall()
        conn.close()

        if not accounts:
            console.print("⚠️ Tidak ada akun yang tersimpan!", style="bold yellow")
            time.sleep(10)
            continue

        for remaining in range(30, -1, -1):
            os.system('cls' if os.name == 'nt' else 'clear')
            table = Table(title=f"🔄 Live OTP Codes (Reset dalam {remaining}s)")
            table.add_column("Layanan", style="cyan")
            table.add_column("Username", style="magenta")
            table.add_column("OTP", style="green")
            for service, username, secret in accounts:
                try:
                    totp = pyotp.TOTP(secret)
                    otp = totp.now()
                    table.add_row(service, username, otp)
                except Exception as e:
                    console.print(f"❌ Error pada akun {service} ({username}): {e}", style="bold red")
            console.print(table)
            time.sleep(1)
