"""RADAR PUB — follow-up loop.

Fase 6: preparação de follow-up (sem envio agressivo).
"""
from __future__ import annotations

from core.entities import Opportunity, NextAction
from core.logging import log_event


class FollowUpEngine:
    """Prepara follow-up para oportunidades.

    Fase 6: apenas preparação. Envio real = futuro.
    """

    def __init__(self) -> None:
        self._pending: list[dict] = []

    def prepare(self, opportunity: Opportunity) -> dict:
        """Prepara um follow-up para a oportunidade."""
        followup = {
            "lead_id": opportunity.lead_id,
            "opportunity_id": opportunity.opportunity_id,
            "prioridade": opportunity.prioridade.value,
            "proxima_acao": opportunity.proxima_acao.value,
            "hipotese": opportunity.hipotese,
            "canal_recomendado": self._canal_recomendado(opportunity),
            "status": "preparado",
        }
        self._pending.append(followup)
        log_event("followup_prepared", lead_id=opportunity.lead_id,
                  prioridade=opportunity.prioridade.value)
        return followup

    def get_pending(self) -> list[dict]:
        return list(self._pending)

    def mark_sent(self, lead_id: str) -> None:
        for f in self._pending:
            if f["lead_id"] == lead_id:
                f["status"] = "enviado"
                log_event("followup_sent", lead_id=lead_id)

    def _canal_recomendado(self, opportunity: Opportunity) -> str:
        if opportunity.proxima_acao == NextAction.CONTACT:
            return "whatsapp"
        if opportunity.proxima_acao == NextAction.EMAIL:
            return "email"
        return "nurture"