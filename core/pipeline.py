"""Pipeline vertical do MVP: Discovery → Research → Analysis → Scoring → Opportunity.

Orquestra os módulos em um fluxo simples. Cada etapa é um agente.
"""
from core.entities import Lead, Research, Analysis, Score, Opportunity
from core.discovery.engine import discover
from core.research.engine import research_lead
from core.analysis.engine import analyze
from core.qualification.engine import qualify
from core.scoring.engine import build_score, compute_dimensions, default_dimensions
from core.opportunity.engine import generate_opportunity
from core.memory.engine import Memory
from core.logging import log_event, log_error
from core.config import CONFIG


class Pipeline:
    """Pipeline vertical do MVP. Cada lead passa por todas as etapas."""

    def __init__(self, memory: Memory | None = None) -> None:
        self.memory = memory or Memory()

    def run(self, source: str | None = None) -> list[dict]:
        """Executa o pipeline completo para todos os leads da fonte."""
        log_event("pipeline_started", source=source or "all")
        leads = discover(source)
        if not leads:
            log_event("pipeline_empty", source=source or "all")
            return []
        results: list[dict] = []
        for lead in leads:
            try:
                results.append(self.run_lead(lead))
            except Exception as e:
                log_error("pipeline_lead_failed", e, lead_id=lead.lead_id, empresa=lead.empresa)
        log_event("pipeline_completed", leads_processed=len(results))
        return results

    def run_lead(self, lead: Lead) -> dict:
        """Executa o pipeline para um lead específico."""
        self.memory.record_lead(lead)
        log_event("lead_processing", lead_id=lead.lead_id, empresa=lead.empresa)

        research = research_lead(lead)
        self.memory.record_research(research)
        log_event("research_completed", lead_id=lead.lead_id, presenca=research.presenca_digital.value)

        analysis = analyze(lead, research)
        log_event("analysis_completed", lead_id=lead.lead_id,
                  strengths=len(analysis.strengths),
                  weaknesses=len(analysis.weaknesses),
                  opportunities=len(analysis.opportunities))

        # Score ÚNICO: dimensões reais derivadas da Analysis.
        # Se Analysis ausente (não acontece no fluxo normal), usa fallback documentado.
        dimensoes = compute_dimensions(analysis) if analysis else default_dimensions()

        # Sprint 2: capability_fit / commercial_fit / confidence são
        # derivados dos matches reais entre problemas detectados e capacidades PUB.
        matches = match_capabilities(lead, research, analysis)
        dimensoes["capability_fit"] = _capability_fit(matches)
        dimensoes["commercial_fit"] = _commercial_fit(matches, analysis)
        dimensoes["confidence"] = _confidence(matches, analysis)

        score = build_score(lead.lead_id, dimensoes)
        self.memory.record_score(score)
        log_event("score_generated", lead_id=lead.lead_id, score_geral=score.score_geral,
                  capability_fit=dimensoes["capability_fit"],
                  commercial_fit=dimensoes["commercial_fit"],
                  confidence=dimensoes["confidence"])

        # qualify() recebe o MESMO Score — opportunity.score_id e
        # opportunity.score_geral vêm do Score único.
        opportunity = qualify(lead, research, analysis, pipeline_score=score)
        self.memory.record_opportunity(opportunity)
        log_event("opportunity_created", lead_id=lead.lead_id,
                  prioridade=opportunity.prioridade.value)

        assert opportunity.score_id == score.score_id, "Score divergente pipeline vs opportunity"
        assert opportunity.score_geral == score.score_geral, "score_geral divergente pipeline vs opportunity"

        return {
            "lead": lead.to_dict(),
            "research": research.to_dict(),
            "analysis": analysis.to_dict(),
            "score": score.to_dict(),
            "opportunity": opportunity.to_dict(),
            "matches": [
                {
                    "capability_id": m.capability_id,
                    "capability": m.capability.name,
                    "problem": m.problem,
                    "evidence": m.evidence,
                    "confidence": m.confidence,
                    "fit_level": m.fit_level,
                    "fit_reason": m.fit_reason,
                    "offers": [o if isinstance(o, dict) else str(o) for o in m.offers],
                }
                for m in matches
            ],
        }

    def get_memory(self) -> list[dict]:
        return [d.to_dict() for d in self.memory.all()]


import os
from core.capabilities.catalog import get_catalog
from core.capabilities.capability_matcher import match_capabilities, CapabilityMatch


def _capability_fit(matches: list[CapabilityMatch]) -> float:
    """capability_fit: quão bem a PUB Holding resolve os problemas detectados.

    0.0 se nenhum match, 1.0 se todos HIGH, média ponderada caso contrário.
    """
    if not matches:
        return 0.0
    return max(m.confidence for m in matches)


def _commercial_fit(matches: list[CapabilityMatch], analysis: Analysis) -> float:
    """commercial_fit: probabilidade de conversão comercial.

    Baseado em:
    - exists match with offers (0.6)
    - exists match HIGH (0.3)
    - analysis has strengths (0.1)
    """
    score = 0.0
    if any(m.offers for m in matches):
        score += 0.6
    if any(m.fit_level == "HIGH" for m in matches):
        score += 0.3
    if analysis.strengths:
        score += 0.1
    return min(1.0, round(score, 4))


def _confidence(matches: list[CapabilityMatch], analysis: Analysis) -> float:
    """confidence: confiança na análise.

    0.5 base, +0.3 se há match, +0.2 se Analysis tem hipóteses.
    """
    base = 0.5
    if matches:
        base += 0.3
    if analysis.hypotheses:
        base += 0.2
    return min(1.0, round(base, 4))


def _default_dimensoes() -> dict[str, float]:
    """Fallback explícito — caminho alternativo sem Analysis.

    Em nenhuma circunstância o pipeline normal deve chamar esta função.
    Todas as dimensões em 0.5 não refletem sinais reais. Prefira usar
    compute_dimensions(analysis) sempre que uma Analysis estiver disponível.
    """
    from core.config import CONFIG
    return {dim: 0.5 for dim in CONFIG.scoring.weights}