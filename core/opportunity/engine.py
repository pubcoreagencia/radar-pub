"""Módulo de oportunidade — gera hipótese, motivo, próxima ação.

Fase 1: templates baseados em prioridade e problemas detectados.
Fase futura: personalização por segmento, dados de mercado, histórico.
"""
from core.entities import Lead, Research, Score, Opportunity, Priority, NextAction

# Templates de hipótese por problema.
HYPOTHESE_TEMPLATES: dict[str, str] = {
    "falta_de_website": "A empresa não possui website. O Pub pode oferecer construção de presença digital.",
    "falta_de_presenca_social": "A empresa não está em redes sociais. O Pub pode atuar em marketing digital.",
    "website_nao_seguro": "Website não é seguro. O Pub pode sugerir migração para HTTPS e melhoria de conversão.",
}

# Motivo por prioridade.
MOTIVO_TEMPLATES: dict[Priority, str] = {
    Priority.HIGH: "Alta presença digital e forte potencial comercial.",
    Priority.MEDIUM: "Presença digital moderada com espaço para crescimento.",
    Priority.LOW: "Presença digital limitada; oportunidade de longo prazo.",
}

# Próxima ação por prioridade.
NEXT_ACTION_TEMPLATES: dict[Priority, NextAction] = {
    Priority.HIGH: NextAction.CONTACT,
    Priority.MEDIUM: NextAction.EMAIL,
    Priority.LOW: NextAction.NURTURE,
}


def generate_opportunity(lead: Lead, research: Research, score: Score) -> Opportunity:
    """Gera uma Opportunity a partir de Lead + Research + Score."""
    prioridade = _classify(score.score_geral)
    hipotese = _build_hipotese(research.problemas_detectados)
    motivo = MOTIVO_TEMPLATES.get(prioridade, "")
    proxima_acao = NEXT_ACTION_TEMPLATES.get(prioridade, NextAction.NURTURE)
    return Opportunity(
        lead_id=lead.lead_id,
        score_id=score.score_id,
        score_geral=score.score_geral,
        prioridade=prioridade,
        hipotese=hipotese,
        motivo=motivo,
        proxima_acao=proxima_acao,
    )


def _classify(score_geral: float) -> Priority:
    from core.scoring.engine import classify_prioridade
    return classify_prioridade(score_geral)


def _build_hipotese(problemas: list[str]) -> str:
    if not problemas:
        return "Lead com presença digital sólida; oportunidade para aprofundamento de relacionamento."
    parts = [HYPOTHESE_TEMPLATES.get(p, f"Problema detectado: {p}") for p in problemas[:2]]
    return " ".join(parts)