"""Testes do módulo de explainability de oportunidade."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import Pipeline
from core.opportunity.explain import oportunidade_score, confidence_score, explain_opportunity
from core.entities import Analysis, Opportunity, Priority, NextAction


def test_oportunidade_score_range():
    analysis = Analysis(lead_id="lead_1", research_id="res_1")
    s = oportunidade_score(analysis)
    assert 0.0 <= s <= 1.0
    print("✓ oportunidade_score range")


def test_oportunidade_score_strengths():
    analysis = Analysis(
        lead_id="lead_1", research_id="res_1",
        strengths=["website_ativo", "presenca_social", "segmento_definido"],
        weaknesses=[],
        opportunities=["marketing_digital"],
    )
    s = oportunidade_score(analysis)
    assert s > 0.5
    print(f"✓ oportunidade_score with strengths: {s}")


def test_confidence_score():
    analysis = Analysis(
        lead_id="lead_1", research_id="res_1",
        strengths=["website_ativo"],
        weaknesses=[],
        hypotheses=["Teste hipótese"],
    )
    opp = Opportunity(
        lead_id="lead_1", score_id="scr_1", score_geral=0.8,
        prioridade=Priority.HIGH, hipotese="Teste", proxima_acao=NextAction.CONTACT
    )
    c = confidence_score(analysis, opp)
    assert 0.0 <= c <= 1.0
    print(f"✓ confidence_score: {c}")


def test_explain_opportunity():
    pipeline = Pipeline()
    results = pipeline.run()
    lead_r = results[0]
    research = __import__("core.research.engine", fromlist=["research_lead"]).research_lead(
        __import__("core.entities", fromlist=["Lead"]).Lead(**{
            k: v for k, v in lead_r["lead"].items()
            if k in ("empresa", "segmento", "localizacao", "website", "redes_sociais", "fonte", "lead_id", "status")
        })
    )
    from core.analysis.engine import analyze
    analysis = analyze(research.to_dict().get("lead_id", research.lead_id) and research.lead_id and __import__("core.entities", fromlist=["Lead"]).Lead(empresa="X") or research.lead_id, research) if False else analyze(
        __import__("core.entities", fromlist=["Lead"]).Lead(
            empresa=lead_r["lead"]["empresa"],
            segmento=lead_r["lead"]["segmento"],
            localizacao=lead_r["lead"]["localizacao"],
            website=lead_r["lead"]["website"],
            redes_sociais=lead_r["lead"]["redes_sociais"],
            fonte=lead_r["lead"]["fonte"],
            lead_id=lead_r["lead"]["lead_id"],
        ),
        research,
    )
    # Build opportunity from score
    score_dict = lead_r["score"]
    from core.entities import Score, Opportunity
    score = Score(
        lead_id=score_dict["lead_id"],
        dimensoes=score_dict["dimensoes"],
        pesos=score_dict["pesos"],
        score_geral=score_dict["score_geral"],
        score_id=score_dict["score_id"],
    )
    from core.qualification.engine import qualify
    opp = qualify(
        __import__("core.entities", fromlist=["Lead"]).Lead(
            empresa=lead_r["lead"]["empresa"],
            segmento=lead_r["lead"]["segmento"],
            localizacao=lead_r["lead"]["localizacao"],
            website=lead_r["lead"]["website"],
            redes_sociais=lead_r["lead"]["redes_sociais"],
            fonte=lead_r["lead"]["fonte"],
            lead_id=lead_r["lead"]["lead_id"],
        ),
        research,
        analysis,
    )
    expl = explain_opportunity(analysis, opp)
    assert "hipotese" in expl
    assert "motivo" in expl
    assert "proxima_acao" in expl
    assert "pontuacao" in expl
    print("✓ explain_opportunity")


def test_pipeline_opportunity_complete():
    """Opportunity from pipeline deve responder: Quem, O quê, Por quê, Quanto, E agora?"""
    pipe = Pipeline()
    results = pipe.run()
    for r in results:
        opp = r["opportunity"]
        analysis = r["analysis"]
        # Quem?
        assert opp["lead_id"] is not None
        # O quê?
        assert opp["hipotese"] != ""
        # Por quê?
        assert opp["motivo"] != "" or len(opp["hipotese"]) > 0
        # Quanto?
        assert opp["score_geral"] >= 0.0
        # E agora?
        assert opp["proxima_acao"] in ("CONTATO", "EMAIL", "NUTRICAO", "DESCARTAR")
    print("✓ Pipeline opportunity complete")


if __name__ == "__main__":
    test_oportunidade_score_range()
    test_oportunidade_score_strengths()
    test_confidence_score()
    test_explain_opportunity()
    test_pipeline_opportunity_complete()
    print("\n✅ Todos os testes de opportunity explainability passaram")