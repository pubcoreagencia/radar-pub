"""Testes de regressão Sprint 2 — FASE 8.

Cobrem as integrações críticas entre as fases concluídas:
- Opportunity entity evoluído (capability_fit, commercial_fit, confidence)
- Persistence salva/restaura os novos campos
- Daemon usa pipeline.run_lead (Score ÚNICO)
- Explainability textual (explain_text.py)
- Pipeline retorna 'matches' no resultado
"""
import sys
import os
import json
import tempfile
import gc
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities import Opportunity, Lead, Research, Analysis, Score, Priority, NextAction
from core.scoring.engine import build_score, classify_prioridade
from core.capabilities.catalog import get_catalog, get_capability, CATALOG_EXCLUDED
from core.capabilities.capability_matcher import match_capabilities, CapabilityMatch
from core.opportunity.explain_text import explain_opportunity_text, explain_opportunity_dict


def _make_db():
    tmpdir = tempfile.mkdtemp(prefix="radar_reg_")
    db_path = os.path.join(tmpdir, "reg.db")
    from core.persistence import Database
    db = Database(db_path)
    return db, tmpdir


def _cleanup(db, tmpdir):
    db.close()
    gc.collect()
    shutil.rmtree(tmpdir, ignore_errors=True)


# --- FASE 4: Opportunity entity ---
def test_opportunity_has_capability_fit_fields():
    opp = Opportunity(lead_id="l1", score_id="s1")
    assert "capability_fit" in opp.__dataclass_fields__
    assert "commercial_fit" in opp.__dataclass_fields__
    assert "confidence" in opp.__dataclass_fields__
    print("✓ Opportunity entity has capability_fit fields")


def test_opportunity_defaults_zero():
    opp = Opportunity(lead_id="l1", score_id="s1")
    assert opp.capability_fit == 0.0
    assert opp.commercial_fit == 0.0
    assert opp.confidence == 0.0
    print("✓ Opportunity capabilities fit defaults to 0.0")


def test_opportunity_to_dict_includes_new_fields():
    opp = Opportunity(
        lead_id="l1", score_id="s1", score_geral=0.7,
        prioridade=Priority.HIGH, hipotese="Test", motivo="Motivo",
        proxima_acao=NextAction.CONTACT,
        capability_fit=0.6, commercial_fit=0.7, confidence=0.9,
    )
    d = opp.to_dict()
    assert d["capability_fit"] == 0.6
    assert d["commercial_fit"] == 0.7
    assert d["confidence"] == 0.9
    print("✓ Opportunity.to_dict includes capability_fit/commercial_fit/confidence")


# --- FASE 6: Score reformulado ---
def test_score_geral_inclui_capability_dims():
    from core.pipeline import Pipeline
    pipe = Pipeline()
    results = pipe.run()
    for r in results:
        dims = r["score"]["dimensoes"]
        assert "capability_fit" in dims
        assert "commercial_fit" in dims
        assert "confidence" in dims
        assert 0.0 <= dims["capability_fit"] <= 1.0
        assert 0.0 <= dims["commercial_fit"] <= 1.0
        assert 0.0 <= dims["confidence"] <= 1.0
    print("✓ Score includes capability_fit/commercial_fit/confidence dims")


def test_pipeline_resultado_contem_matches():
    from core.pipeline import Pipeline
    pipe = Pipeline()
    results = pipe.run()
    for r in results:
        assert "matches" in r
        assert isinstance(r["matches"], list)
        for m in r["matches"]:
            assert "capability_id" in m
            assert "capability" in m
            assert "problem" in m
            assert "confidence" in m
            assert "fit_level" in m
    print("✓ Pipeline results include matches structure")


# --- FASE 10: Persistência ---
def test_persistence_salva_campos_novos():
    db, tmp = _make_db()
    opp = Opportunity(
        lead_id="l1", score_id="s1", score_geral=0.8,
        prioridade=Priority.HIGH, hipotese="H", motivo="M",
        proxima_acao=NextAction.CONTACT,
        capability_fit=0.6, commercial_fit=0.7, confidence=0.9,
    )
    db.save_opportunity(opp)
    opps = db.get_opportunities()
    assert len(opps) == 1
    row = opps[0]
    assert row["capability_fit"] == 0.6
    assert row["commercial_fit"] == 0.7
    assert row["confidence"] == 0.9
    _cleanup(db, tmp)
    print("✓ Persistence saves capability_fit/commercial_fit/confidence")


# --- Daemon usa pipeline.run_lead ---
def test_daemon_usa_pipeline():
    from core.daemon import RadarDaemon
    tmpdir = tempfile.mkdtemp(prefix="radar_daemon_reg_")
    db_path = os.path.join(tmpdir, "daemon_reg.db")
    daemon = RadarDaemon(db_path=db_path)
    daemon._discovery_loop()
    daemon._qualification_loop()
    opps = daemon.db.get_opportunities()
    assert len(opps) == 3
    for o in opps:
        assert "capability_fit" in o
        assert "commercial_fit" in o
        assert "confidence" in o
    daemon.db.close()
    shutil.rmtree(tmpdir, ignore_errors=True)
    print("✓ Daemon uses pipeline.run_lead with capability dims")


# --- Explainability textual ---
def test_explain_text_inclui_capability_dims():
    opp = Opportunity(
        lead_id="l1", score_id="s1", score_geral=0.75,
        prioridade=Priority.MEDIUM, hipotese="Teste hipótese",
        proxima_acao=NextAction.EMAIL,
        capability_fit=0.6, commercial_fit=0.7, confidence=0.85,
    )
    text = explain_opportunity_text(opp, empresa="TestCorp")
    assert "TestCorp" in text
    assert "0.60" in text or "0.6" in text
    assert "Próxima ação:" in text
    print("✓ explain_opportunity_text includes capability dims")


def test_explain_dict_inclui_capabilities():
    opp = Opportunity(
        lead_id="l1", score_id="s1", score_geral=0.75,
        prioridade=Priority.HIGH, hipotese="H", proxima_acao=NextAction.CONTACT,
        capability_fit=0.8, commercial_fit=0.6, confidence=0.9,
    )
    d = explain_opportunity_dict(opp, matches=[])
    assert "capability_fit" in d
    assert "commercial_fit" in d
    assert "confidence" in d
    assert d["capabilities"] == []
    print("✓ explain_opportunity_dict includes new fields")


# --- Capability matcher integration ---
def test_match_capabilities_returns_real_matches():
    lead = Lead(empresa="Test", segmento="Retail")
    research = Research(lead_id="l1", presenca_digital="AUSENTE")
    analysis = Analysis(
        lead_id="l1", research_id="r1",
        weaknesses=["falta_de_website"],
        opportunities=["sem_crm_estruturado"],
        hypotheses=["Teste"],
    )
    matches = match_capabilities(lead, research, analysis)
    assert len(matches) > 0
    for m in matches:
        assert m.capability.confidence in (0.6, 0.9)
        assert m.offers is not None
    print(f"✓ match_capabilities found {len(matches)} real matches")


def test_catalog_ativo_tem_12():
    catalog = get_catalog()
    assert len(catalog) == 12
    print("✓ Catalog ativo tem 12 capacidades")


def test_catalog_excluded_tem_entrada():
    assert len(CATALOG_EXCLUDED) >= 20
    print(f"✓ CATALOG_EXCLUDED tem {len(CATALOG_EXCLUDED)} entradas")


# --- Score ÚNICO: pipeline vs opportunity ---
def test_score_unico_pipeline_vs_opportunity():
    from core.pipeline import Pipeline
    pipe = Pipeline()
    results = pipe.run()
    for r in results:
        assert r["opportunity"]["score_id"] == r["score"]["score_id"], "score_id divergente"
        assert r["opportunity"]["score_geral"] == r["score"]["score_geral"], "score_geral divergente"
    print("✓ Score único: pipeline vs opportunity consistent")


if __name__ == "__main__":
    test_opportunity_has_capability_fit_fields()
    test_opportunity_defaults_zero()
    test_opportunity_to_dict_includes_new_fields()
    test_score_geral_inclui_capability_dims()
    test_pipeline_resultado_contem_matches()
    test_persistence_salva_campos_novos()
    test_daemon_usa_pipeline()
    test_explain_text_inclui_capability_dims()
    test_explain_dict_inclui_capabilities()
    test_match_capabilities_returns_real_matches()
    test_catalog_ativo_tem_12()
    test_catalog_excluded_tem_entrada()
    test_score_unico_pipeline_vs_opportunity()
    print("\n✅ Todos os 13 testes de regressão Sprint 2 passaram")
