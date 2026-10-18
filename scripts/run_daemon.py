#!/usr/bin/env python3
"""Entry point do daemon 24/7 do RADAR PUB."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.daemon import RadarDaemon


def main() -> None:
    db_path = os.getenv("RADAR_DB_PATH", "radar.db")
    daemon = RadarDaemon(db_path=db_path)
    daemon.start()


if __name__ == "__main__":
    main()