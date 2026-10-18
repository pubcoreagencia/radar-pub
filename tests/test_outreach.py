"""Testes dos canais de outreach e follow-up."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.outreach.channels import InstagramChannel, WhatsAppChannel, EmailChannel, OutreachManager
from core.followup.engine import FollowUpEngine
from core.entities import Opportunity, Priority, NextAction


def test_instagram_not_configured():
    ch = InstagramChannel()
    assert not ch.is_configured()
    result = ch.send("lead_1", "Olá")
    assert result["success"] == False
    assert result["error"] == "instagram_not_configured"
    print("✓ instagram_not_configured")


def test_whatsapp_not_configured():
    ch = WhatsAppChannel()
    assert not ch.is_configured()
    result = ch.send("lead_1", "Olá")
    assert result["success"] == False
    assert result["error"] == "whatsapp_not_configured"
    print("✓ whatsapp_not_configured")


def test_email_not_configured():
    ch = EmailChannel()
    assert not ch.is_configured()
    result = ch.send("lead_1", "Olá")
    assert result["success"] == False
    assert result["error"] == "email_not_configured"
    print("✓ email_not_configured")


def test_outreach_manager():
    mgr = OutreachManager()
    mgr.register("instagram", InstagramChannel())
    mgr.register("whatsapp", WhatsAppChannel())
    assert mgr.configured_channels() == []
    result = mgr.send("unknown", "lead_1", "Olá")
    assert result["success"] == False
    print("✓ outreach_manager")


def test_followup_prepare():
    engine = FollowUpEngine()
    opp = Opportunity(lead_id="l1", score_id="s1", score_geral=0.9,
                      prioridade=Priority.HIGH, hipotese="Teste", proxima_acao=NextAction.CONTACT)
    f = engine.prepare(opp)
    assert f["status"] == "preparado"
    assert f["canal_recomendado"] == "whatsapp"
    assert len(engine.get_pending()) == 1
    print("✓ followup_prepare")


def test_followup_mark_sent():
    engine = FollowUpEngine()
    opp = Opportunity(lead_id="l1", score_id="s1", score_geral=0.9,
                      prioridade=Priority.HIGH, hipotese="Teste", proxima_acao=NextAction.CONTACT)
    engine.prepare(opp)
    engine.mark_sent("l1")
    pending = engine.get_pending()
    assert pending[0]["status"] == "enviado"
    print("✓ followup_mark_sent")


if __name__ == "__main__":
    test_instagram_not_configured()
    test_whatsapp_not_configured()
    test_email_not_configured()
    test_outreach_manager()
    test_followup_prepare()
    test_followup_mark_sent()
    print("\n✅ Todos os testes de outreach/followup passaram")