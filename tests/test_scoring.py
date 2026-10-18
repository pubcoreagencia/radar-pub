"""Testes do módulo de scoring.

Valida engine de pontuação e classificação de prioridade.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scoring.engine import build_score, classify_prioridade, compute_score_geral
from core.entities import Priority


def test_compute_score_geral():
    dimensoes = {"seo": 0.9, "website": 0.8}
    pesos = {"seo": 0.5, "website": 0.5}
    g = compute_score_geral(dimensoes, pesos)
    assert 0 <= g <= 1
    print("✓ compute_score_geral")


def test_classify_prioridade():
    assert classify_prioridade(0.80) == Priority.HIGH
    assert classify_prioridade(0.60) == Priority.MEDIUM
    assert classify_prioridade(0.30) == Priority.LOW
    print("✓ classify_prioridade")


def test_build_score():
    score = build_score("lead_1", {"seo": 1.0, "website": 0.5})
    assert score.lead_id == "lead_1"
    assert 0 <= score.score_geral <= 1
    print("✓ build_score")


if __name__ == "__main__":
    test_compute_score_geral()
    test_classify_prioridade()
    test_build_score()
    print("\n✅ Todos os testes de scoring passaram")