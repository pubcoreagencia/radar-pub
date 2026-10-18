"""Runner de todos os testes do radar-pub.

Executa todos os testes de forma sequencial e reporta resultado.
"""
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Executa cada arquivo de teste
test_files = [
    "tests/test_entities.py",
    "tests/test_scoring.py",
    "tests/test_pipeline.py",
    "tests/test_edge_cases.py",
    "tests/test_config.py",
    "tests/test_explainability.py",
    "tests/test_opportunity.py",
    "tests/test_persistence.py",
    "tests/test_outreach.py",
    "tests/test_daemon_api.py",
]

for tf in test_files:
    print(f"\n=== {tf} ===")
    with open(tf) as f:
        code = f.read()
    exec(compile(code, tf, "exec"))

print("\n✅ Todos os testes passaram")