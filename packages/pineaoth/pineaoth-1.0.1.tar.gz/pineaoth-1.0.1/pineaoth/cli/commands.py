import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from pineaoth.core.manager import add_account, list_accounts, delete_account
from pineaoth.core.otp import show_live_otp

def parse_cli():
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

    add = subparsers.add_parser("add", help="Tambah akun OTP")
    add.add_argument("service")
    add.add_argument("username")
    add.add_argument("secret")
    add.set_defaults(func=lambda args: add_account(args.service, args.username, args.secret))

    lst = subparsers.add_parser("list", help="Lihat semua akun")
    lst.set_defaults(func=lambda args: list_accounts())

    delete = subparsers.add_parser("delete", help="Hapus akun")
    delete.add_argument("service")
    delete.add_argument("username")
    delete.set_defaults(func=lambda args: delete_account(args.service, args.username))

    live = subparsers.add_parser("live", help="Live OTP")
    live.set_defaults(func=lambda args: show_live_otp())

    parser.add_argument("-v", "--version", action="version", version="pineaoth 1.0.1")

    return parser
