"""Testes unitários para domínios de entidades do radar-pub.

Sem dependências externas; pura Python stdlib.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities import Lead, LeadStatus, Research, Evidence, DigitalPresence, Score, Opportunity, Priority, NextAction


def test_lead():
    lead = Lead(empresa="Test Co", segmento="Tech", localizacao="BR")
    assert lead.empresa == "Test Co"
    assert lead.lead_id.startswith("lead_")
    assert lead.status == LeadStatus.NEW
    print("✓ Lead")


def test_research():
    research = Research(lead_id="lead_123", presenca_digital=DigitalPresence.HIGH)
    assert research.lead_id == "lead_123"
    assert research.presenca_digital == DigitalPresence.HIGH
    print("✓ Research")


def test_score():
    score = Score(lead_id="lead_123", dimensoes={"seo": 0.8, "website": 0.9}, score_geral=0.85)
    assert score.score_geral == 0.85
    print("✓ Score")


def test_opportunity():
    opp = Opportunity(lead_id="lead_123", score_id="scr_123", prioridade=Priority.HIGH, hipotese="Teste")
    assert opp.prioridade == Priority.HIGH
    print("✓ Opportunity")


def test_pipeline_import():
    from core.pipeline import Pipeline
    assert Pipeline is not None
    print("✓ Pipeline import")


if __name__ == "__main__":
    test_lead()
    test_research()
    test_score()
    test_opportunity()
    test_pipeline_import()
    print("\n✅ Todos os testes passaram")