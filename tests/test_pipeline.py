"""Testes do novo pipeline (Analysis + explainability)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import Pipeline


def test_pipeline_with_analysis():
    pipe = Pipeline()
    resultados = pipe.run()
    assert isinstance(resultados, list)
    assert len(resultados) > 0
    for r in resultados:
        assert "lead" in r
        assert "research" in r
        assert "analysis" in r
        assert "score" in r
        assert "opportunity" in r
        assert 0.0 <= r["opportunity"]["score_geral"] <= 1.0
        assert r["opportunity"]["prioridade"] in ("ALTA", "MEDIA", "BAIXA", "DESCARTADO")
        assert r["opportunity"]["hipotese"] != ""
    print(f"✓ Pipeline com Analysis executou {len(resultados)} leads")


def test_analysis_structure():
    from core.analysis.engine import analyze
    from core.discovery.engine import discover
    from core.research.engine import research_lead

    lead = discover()[0]
    research = research_lead(lead)
    analysis = analyze(lead, research)

    assert analysis.lead_id == lead.lead_id
    assert analysis.research_id == research.research_id
    assert isinstance(analysis.strengths, list)
    assert isinstance(analysis.weaknesses, list)
    assert isinstance(analysis.opportunities, list)
    assert isinstance(analysis.hypotheses, list)
    print("✓ Analysis structure")


def test_qualification_structure():
    from core.qualification.engine import qualify
    from core.entities import Lead
    from core.research.engine import research_lead
    from core.analysis.engine import analyze

    lead = Lead(empresa="QualTest", segmento="Tech", localizacao="BR")
    research = research_lead(lead)
    analysis = analyze(lead, research)
    opp = qualify(lead, research, analysis)
    assert opp.lead_id == lead.lead_id
    assert opp.hipotese != ""
    print("✓ Qualification structure")


def test_score_varied():
    """Score deve variar por lead, não fixo em 0.5."""
    from core.discovery.engine import discover
    from core.research.engine import research_lead
    from core.analysis.engine import analyze
    from core.qualification.engine import qualify

    pipe = Pipeline()
    scores = []
    for lead in discover():
        research = research_lead(lead)
        analysis = analyze(lead, research)
        opp = qualify(lead, research, analysis)
        scores.append(opp.score_geral)

    # Pelo menos dois scores diferentes → scoring é real
    assert len(set(scores)) > 1, f"Scores todos iguais: {scores}"
    print(f"✓ Score varied: {scores}")


if __name__ == "__main__":
    test_pipeline_with_analysis()
    test_analysis_structure()
    test_qualification_structure()
    test_qualification_structure()
    test_score_varied()
    print("\n✅ Todos os testes de pipeline passaram")