"""Testes de persistência SQLite."""
import sys, os, tempfile, gc, shutil
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.persistence import Database
from core.entities import Lead, LeadStatus, Lead as LeadEntity


def _make_db():
    tmpdir = tempfile.mkdtemp(prefix="radar_test_")
    db_path = os.path.join(tmpdir, "test_radar.db")
    db = Database(db_path)
    return db, tmpdir


def _cleanup_db(db, tmpdir):
    db.close()
    gc.collect()
    for _ in range(5):
        try:
            shutil.rmtree(tmpdir, ignore_errors=False)
            return
        except PermissionError:
            import time; time.sleep(0.1)
    shutil.rmtree(tmpdir, ignore_errors=True)


def _row_to_lead(d: dict) -> Lead:
    return Lead(
        lead_id=d.get("lead_id"),
        empresa=d["empresa"],
        segmento=d.get("segmento"),
        localizacao=d.get("localizacao"),
        website=d.get("website"),
        redes_sociais=d.get("redes_sociais") or [],
        fonte=d.get("fonte"),
        status=d.get("status"),
    )


def test_save_and_get_lead():
    db, tmp = _make_db()
    lead = Lead(empresa="PersistTest", segmento="Tech", localizacao="BR", website="https://persist.example.com")
    db.save_lead(lead)
    row = db.get_lead(lead.lead_id)
    assert row is not None
    assert row["empresa"] == "PersistTest"
    assert row["website"] == "https://persist.example.com"
    _cleanup_db(db, tmp)
    print("✓ save_and_get_lead")


def test_get_leads():
    db, tmp = _make_db()
    for i in range(5):
        db.save_lead(Lead(empresa=f"Co{i}", segmento="Tech"))
    leads = db.get_leads()
    assert len(leads) == 5
    _cleanup_db(db, tmp)
    print("✓ get_leads")


def test_pipeline_persists():
    """Pipeline completo com persistência."""
    from core.pipeline import Pipeline
    db, tmp = _make_db()
    pipe = Pipeline()
    results = pipe.run()
    for r in results:
        db.save_lead(_row_to_lead(r["lead"]))
        db.save_research(r["research"])
        db.save_analysis(r["analysis"])
        db.save_score(r["score"])
        db.save_opportunity(r["opportunity"])
    leads = db.get_leads()
    assert len(leads) == 3
    opps = db.get_opportunities()
    assert len(opps) == 3
    scores = [o["score_geral"] for o in opps]
    assert scores == sorted(scores, reverse=True)
    _cleanup_db(db, tmp)
    print("✓ pipeline_persists")


def test_opportunities_by_priority():
    from core.entities import Opportunity, Priority, NextAction
    db, tmp = _make_db()
    opp_high = Opportunity(lead_id="l1", score_id="s1", score_geral=0.9, prioridade=Priority.HIGH,
                           hipotese="High", proxima_acao=NextAction.CONTACT)
    opp_low = Opportunity(lead_id="l2", score_id="s2", score_geral=0.3, prioridade=Priority.LOW,
                          hipotese="Low", proxima_acao=NextAction.NURTURE)
    db.save_opportunity(opp_high)
    db.save_opportunity(opp_low)
    high = db.get_opportunities("ALTA")
    assert len(high) == 1
    assert high[0]["prioridade"] == "ALTA"
    _cleanup_db(db, tmp)
    print("✓ opportunities_by_priority")


if __name__ == "__main__":
    test_save_and_get_lead()
    test_get_leads()
    test_pipeline_persists()
    test_opportunities_by_priority()
    print("\n✅ Todos os testes de persistência passaram")