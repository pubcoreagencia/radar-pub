"""Testes do módulo de explainability do scoring."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.scoring.engine import build_score
from core.scoring.explain import explain_score, format_score_report


def test_explain_score():
    dimensoes = {
        "seo": 0.9,
        "website": 0.8,
        "social": 0.7,
        "tracking": 0.6,
        "conversion": 0.5,
        "commercial_potential": 0.4,
    }
    score = build_score("lead_1", dimensoes)
    exp = explain_score(score)
    assert exp["score_geral"] == score.score_geral
    assert len(exp["explicacao"]) == 6
    total = sum(l["contribuicao"] for l in exp["explicacao"])
    assert abs(total - score.score_geral) < 0.001
    print("✓ explain_score")


def test_format_score_report():
    dimensoes = {"seo": 1.0, "website": 0.5, "social": 0.5, "tracking": 0.5, "conversion": 0.5, "commercial_potential": 0.5}
    score = build_score("lead_1", dimensoes)
    report = format_score_report(score)
    assert "Score Report" in report
    assert "score_geral" in report
    assert "Breakdown" in report
    print("✓ format_score_report")


if __name__ == "__main__":
    test_explain_score()
    test_format_score_report()
    print("\n✅ Todos os testes de explainability passaram")