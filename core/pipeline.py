"""Pipeline vertical do MVP: Discovery → Research → Analysis → Scoring → Opportunity.

Orquestra os módulos em um fluxo simples. Cada etapa é um agente.
"""
from core.entities import Lead, Research, Analysis, Score, Opportunity
from core.discovery.engine import discover
from core.research.engine import research_lead
from core.analysis.engine import analyze
from core.qualification.engine import qualify
from core.scoring.engine import build_score
from core.opportunity.engine import generate_opportunity
from core.memory.engine import Memory
from core.logging import log_event, log_error


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

        score = build_score(lead.lead_id, _default_dimensoes())
        self.memory.record_score(score)
        log_event("score_generated", lead_id=lead.lead_id, score_geral=score.score_geral)

        opportunity = qualify(lead, research, analysis)
        self.memory.record_opportunity(opportunity)
        log_event("opportunity_created", lead_id=lead.lead_id,
                  prioridade=opportunity.prioridade.value)

        return {
            "lead": lead.to_dict(),
            "research": research.to_dict(),
            "analysis": analysis.to_dict(),
            "score": score.to_dict(),
            "opportunity": opportunity.to_dict(),
        }

    def get_memory(self) -> list[dict]:
        return [d.to_dict() for d in self.memory.all()]


def _default_dimensoes() -> dict[str, float]:
    return {
        "seo": 0.5,
        "website": 0.5,
        "social": 0.5,
        "tracking": 0.5,
        "conversion": 0.5,
        "commercial_potential": 0.5,
    }