"""Módulo de memória — histórico de decisões e aprendizado.

Fase 1: registry em memória (volatile).
Fase futura: persistência em Turso/SQLite, feedback comercial, learning loop.
"""
from core.entities import DecisionRecord, Lead, Research, Score, Opportunity


class Memory:
    """Registry em memória de decisões. Thread-safe para uso single-process."""
    def __init__(self) -> None:
        self._decisions: list[DecisionRecord] = []

    def record(self, lead_id: str, etapa: str, decisao: str, justificativa: str = "") -> DecisionRecord:
        d = DecisionRecord(lead_id=lead_id, etapa=etapa, decisao=decisao, justificativa=justificativa)
        self._decisions.append(d)
        return d

    def record_lead(self, lead: Lead) -> DecisionRecord:
        return self.record(lead.lead_id, "discovery", f"lead criado: {lead.empresa}")

    def record_research(self, research: Research) -> DecisionRecord:
        return self.record(research.lead_id, "research", f"presenca: {research.presenca_digital.value}")

    def record_score(self, score: Score) -> DecisionRecord:
        return self.record(score.lead_id, "scoring", f"score_geral: {score.score_geral}")

    def record_opportunity(self, opp: Opportunity) -> DecisionRecord:
        return self.record(opp.lead_id, "opportunity", f"prioridade: {opp.prioridade.value}, acao: {opp.proxima_acao.value}")

    def all(self) -> list[DecisionRecord]:
        return list(self._decisions)

    def clear(self) -> None:
        self._decisions.clear()