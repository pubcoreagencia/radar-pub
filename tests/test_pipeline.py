"""Testes rápidos do pipeline vertical.

Valida o fluxo: descoberta -> pesquisa -> qualificação -> pontuação -> oportunidade.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import Pipeline


def test_pipeline_run():
    pipe = Pipeline()
    resultados = pipe.run()
    assert isinstance(resultados, list)
    assert len(resultados) > 0, "Esperado pelo menos um lead da fixture"
    for r in resultados:
        assert "lead" in r
        assert "research" in r
        assert "score" in r
        assert "opportunity" in r
        assert r["opportunity"]["score_geral"] >= 0.0
        assert r["opportunity"]["score_geral"] <= 1.0
        assert r["opportunity"]["prioridade"] in ("ALTA", "MEDIA", "BAIXA", "DESCARTADO")
    print(f"✓ Pipeline executou {len(resultados)} leads")


def test_pipeline_lead_specific():
    from core.discovery.engine import discover
    pipe = Pipeline()
    for lead in discover():
        r = pipe.run_lead(lead)
        assert r["lead"]["empresa"] == lead.empresa
        assert r["research"]["lead_id"] == lead.lead_id
        break
    print("✓ Pipeline lead específico")


if __name__ == "__main__":
    test_pipeline_run()
    test_pipeline_lead_specific()
    print("\n✅ Todos os testes de pipeline passaram")