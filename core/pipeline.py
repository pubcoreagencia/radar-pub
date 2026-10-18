"""Pipeline vertical do MVP: Discovery → Research → Analysis → Scoring → Opportunity.

Orquestra os módulos em um fluxo simples. Cada etapa é um agente.
"""
from core.entities import Lead, Research, Score, Opportunity
from core.discovery.engine import discover, discover_one
from core.research.engine import research_lead
from core.qualification.engine import qualify
from core.opportunity.engine import generate_opportunity
from core.memory.engine import Memory


class Pipeline:
    """Pipeline vertical do MVP. Cada lead passa por todas as etapas."""

    def __init__(self, memory: Memory | None = None) -> None:
        self.memory = memory or Memory()

    def run(self, source: str | None = None) -> list[dict]:
        """Executa o pipeline completo para todos os leads da fonte."""
        results: list[dict] = []
        for lead in discover(source):
            results.append(self.run_lead(lead))
        return results

    def run_lead(self, lead: Lead) -> dict:
        """Executa o pipeline para um lead específico."""
        self.memory.record_lead(lead)

        research = research_lead(lead)
        self.memory.record_research(research)

        score = qualify(lead, research)
        self.memory.record_score(score)

        opportunity = generate_opportunity(lead, research, score)
        self.memory.record_opportunity(opportunity)

        return {
            "lead": lead.to_dict(),
            "research": research.to_dict(),
            "score": score.to_dict(),
            "opportunity": opportunity.to_dict(),
        }

    def get_memory(self) -> list[dict]:
        return [d.to_dict() for d in self.memory.all()]