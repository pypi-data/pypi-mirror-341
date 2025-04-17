#!python
import sqlite3
import pyotp
import time
import os
import base64
import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt

console = Console()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "accounts.db")

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    service TEXT NOT NULL,
                    username TEXT NOT NULL,
                    secret TEXT NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

def is_valid_base32(secret):
    try:
        base64.b32decode(secret, casefold=True)
        return True
    except Exception:
        return False

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

def show_live_otp():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
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

def main():
    parser = argparse.ArgumentParser(
        prog="pineaoth",
        description="CLI 2FA Authenticator",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Contoh penggunaan:
  pineaoth add GitHub user123 ABCDEFGHIJKLMNOP
  pineaoth list
  pineaoth delete GitHub user123
  pineaoth live
"""
    )
    
    subparsers = parser.add_subparsers(dest="command")
    
    add_parser = subparsers.add_parser("add", help="Tambah akun OTP")
    add_parser.add_argument("service", help="Nama layanan (GitHub, GitLab, dll.)")
    add_parser.add_argument("username", help="Nama pengguna")
    add_parser.add_argument("secret", help="Secret key dalam format Base32")
    add_parser.set_defaults(func=lambda args: add_account(args.service, args.username, args.secret))
    
    list_parser = subparsers.add_parser("list", help="Lihat semua akun yang tersimpan")
    list_parser.set_defaults(func=lambda args: list_accounts())
    
    delete_parser = subparsers.add_parser("delete", help="Hapus akun OTP")
    delete_parser.add_argument("service", help="Nama layanan akun yang ingin dihapus")
    delete_parser.add_argument("username", help="Nama pengguna akun yang ingin dihapus")
    delete_parser.set_defaults(func=lambda args: delete_account(args.service, args.username))
    
    live_parser = subparsers.add_parser("live", help="Tampilkan kode OTP secara live")
    live_parser.set_defaults(func=lambda args: show_live_otp())
    
    parser.add_argument("-v", "--version", action="version", version="pineaoth 1.0")
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()