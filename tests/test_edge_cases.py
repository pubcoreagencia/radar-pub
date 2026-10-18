"""Testes de edge cases e robustez do pipeline.

Cobre:
- lead sem website
- lead sem redes sociais
- lead com dados parcialmente ausentes
- lead vazio
- dados malformados
- pipeline vazio
- scoring explicável
- múltiplos leads
- estrutura de Opportunity
- consistência do pipeline
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities import Lead, Research, Score, Opportunity, Priority, NextAction, DigitalPresence
from core.pipeline import Pipeline
from core.discovery.engine import discover
from core.scoring.engine import build_score, compute_score_geral
from core.research.engine import research_lead


def test_lead_without_website():
    lead = Lead(empresa="NoWeb", segmento="Indústria", localizacao="BR", website=None)
    research = research_lead(lead)
    assert research.presenca_digital == DigitalPresence.ABSENT
    assert "falta_de_website" in research.problemas_detectados
    print("✓ Lead sem website")


def test_lead_without_social():
    lead = Lead(empresa="NoSocial", website="https://nosocial.example.com", redes_sociais=[])
    research = research_lead(lead)
    assert research.presenca_digital == DigitalPresence.MEDIUM
    assert "falta_de_presenca_social" in research.problemas_detectados
    print("✓ Lead sem redes sociais")


def test_lead_partial_data():
    lead = Lead(empresa="Partial", website=None, redes_sociais=["linkedin:partial"])
    research = research_lead(lead)
    assert research.presenca_digital == DigitalPresence.MEDIUM
    assert "falta_de_website" in research.problemas_detectados
    print("✓ Lead com dados parcialmente ausentes")


def test_lead_malformed():
    lead = Lead(empresa="", segmento="", localizacao="", website=None, redes_sociais=[])
    research = research_lead(lead)
    assert research.presenca_digital == DigitalPresence.ABSENT
    assert len(research.problemas_detectados) > 0
    print("✓ Lead com dados malformados")


def test_empty_pipeline():
    pipe = Pipeline()
    assert pipe.run(source="fixture:nao_existe") == []
    print("✓ Pipeline vazio")


def test_score_explanatory():
    dimensoes = {
        "seo": 0.9,
        "website": 0.8,
        "social": 0.7,
        "tracking": 0.6,
        "conversion": 0.5,
        "commercial_potential": 0.4,
    }
    pesos = {
        "seo": 0.20,
        "website": 0.25,
        "social": 0.15,
        "tracking": 0.10,
        "conversion": 0.15,
        "commercial_potential": 0.15,
    }
    score = build_score("lead_1", dimensoes, pesos)
    g = compute_score_geral(dimensoes, pesos)
    assert score.score_geral == g
    for dim, val in dimensoes.items():
        assert val * pesos[dim] >= 0.0
    print("✓ Score explicável")


def test_pipeline_multiple_leads():
    pipe = Pipeline()
    resultados = pipe.run()
    assert len(resultados) == 3
    for r in resultados:
        assert r["lead"]["lead_id"] == r["research"]["lead_id"]
        assert r["research"]["lead_id"] == r["score"]["lead_id"]
        assert r["score"]["lead_id"] == r["opportunity"]["lead_id"]
    print("✓ Pipeline múltiplos leads")


def test_opportunity_structure():
    pipe = Pipeline()
    resultados = pipe.run()
    for r in resultados:
        opp = r["opportunity"]
        assert opp["lead_id"] is not None
        assert opp["hipotese"] != ""
        assert opp["motivo"] != ""
        assert opp["score_geral"] >= 0.0
        assert opp["proxima_acao"] in ("CONTATO", "EMAIL", "NUTRICAO", "DESCARTAR")
    print("✓ Opportunity structure")


def test_pipeline_consistency():
    pipe1 = Pipeline()
    pipe2 = Pipeline()
    lead = discover()[0]
    r1 = pipe1.run_lead(lead)
    r2 = pipe2.run_lead(lead)
    assert r1["lead"]["empresa"] == r2["lead"]["empresa"]
    assert r1["opportunity"]["prioridade"] == r2["opportunity"]["prioridade"]
    print("✓ Pipeline consistência")


if __name__ == "__main__":
    test_lead_without_website()
    test_lead_without_social()
    test_lead_partial_data()
    test_lead_malformed()
    test_empty_pipeline()
    test_score_explanatory()
    test_pipeline_multiple_leads()
    test_opportunity_structure()
    test_pipeline_consistency()
    print("\n✅ Todos os testes de edge cases passaram")