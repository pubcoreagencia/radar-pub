#!/usr/bin/env python3
"""Entry point do servidor HTTP da API do RADAR PUB."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api import serve


def main() -> None:
    host = os.getenv("RADAR_API_HOST", "127.0.0.1")
    port = int(os.getenv("RADAR_API_PORT", "8787"))
    db_path = os.getenv("RADAR_DB_PATH", None)
    serve(host=host, port=port, db_path=db_path)


if __name__ == "__main__":
    main()