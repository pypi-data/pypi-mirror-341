import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pineaoth.database.db import init_db
from pineaoth.cli.commands import parse_cli

def main():
    init_db()
    parser = parse_cli()
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
