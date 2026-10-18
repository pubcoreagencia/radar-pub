#!/usr/bin/env python3

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import Pipeline


def main():
    pipe = Pipeline()
    resultados = pipe.run()
    print("=== RADAR PUB DEMO ===")
    for r in resultados:
        l = r['lead']
        o = r['opportunity']
        print(f"{l['empresa']} | {o['prioridade']} | {o['hipotese']}")
    print("========================")


if __name__ == "__main__":
    main()