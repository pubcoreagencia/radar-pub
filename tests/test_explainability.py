"""Testes do módulo de explainability do scoring."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scoring.engine import build_score
from core.scoring.explain import explain_score, format_score_report
from core.config import CONFIG


def _full_dimensoes() -> dict:
    """Todas as dimensões de CONFIG (9 dims), valores decrescentes."""
    return {dim: 0.9 - i * 0.1 for i, dim in enumerate(CONFIG.scoring.weights)}


def test_explain_score():
    dimensoes = _full_dimensoes()
    score = build_score("lead_1", dimensoes)
    exp = explain_score(score)
    assert exp["score_geral"] == score.score_geral
    assert len(exp["explicacao"]) == len(CONFIG.scoring.weights)
    total = sum(l["contribuicao"] for l in exp["explicacao"])
    assert abs(total - score.score_geral) < 0.001
    print("✓ explain_score")


def test_format_score_report():
    dimensoes = _full_dimensoes()
    score = build_score("lead_1", dimensoes)
    report = format_score_report(score)
    assert "Score Report" in report
    assert "score_geral" in report
    assert "Breakdown" in report
    print("✓ format_score_report")


def test_explain_score_sprint2_dims():
    """Sprint 2: dimensões de capability_fit/commercial_fit/confidence presentes."""
    dimensoes = _full_dimensoes()
    score = build_score("lead_1", dimensoes)
    exp = explain_score(score)
    dims = {l["dimensao"] for l in exp["explicacao"]}
    assert "capability_fit" in dims
    assert "commercial_fit" in dims
    assert "confidence" in dims
    print("✓ explain_score com dimensões Sprint 2")


if __name__ == "__main__":
    test_explain_score()
    test_format_score_report()
    test_explain_score_sprint2_dims()
    print("\n✅ Todos os testes de explainability passaram")