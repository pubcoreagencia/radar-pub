"""Módulo de qualification — transforma Research + Analysis em Opportunity.

Fase 1: heurísticas baseadas em sinais e problemas.
Fase futura: ML, sinais de intenção, dados de mercado.
"""
from core.entities import Lead, Research, Analysis, Score, Opportunity, Priority, NextAction
from core.scoring.engine import build_score, classify_prioridade
from core.config import CONFIG


def qualify(lead: Lead, research: Research, analysis: Analysis) -> Opportunity:
    """Qualifica um lead: calcula score baseado em Analysis e gera Opportunity."""
    dimensoes = _compute_dimensoes(analysis)
    score = build_score(lead.lead_id, dimensoes)

    if not analysis.hypotheses:
        from core.opportunity.engine import generate_opportunity
        return generate_opportunity(lead, research, score)

    prioridade = classify_prioridade(score.score_geral)
    hipotese = analysis.hypotheses[0] if analysis.hypotheses else ""
    motivo = _motivo(prioridade, analysis)
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


def _compute_dimensoes(analysis: Analysis) -> dict[str, float]:
    """Calcula dimensões do score a partir da Analysis.

    Heurística: strength → 1.0, weakness → 0.0, neutro → 0.5.
    """
    dims: dict[str, float] = {}
    for dim in CONFIG.scoring.weights:
        if _has_strength_for(analysis, dim):
            dims[dim] = 1.0
        elif _has_weakness_for(analysis, dim):
            dims[dim] = 0.0
        else:
            dims[dim] = 0.5
    return dims


def _has_strength_for(analysis: Analysis, dim: str) -> bool:
    """Verdadeiro se há força relacionada à dimensão."""
    mapping = {
        "seo": ["website_ativo"],
        "website": ["website_ativo"],
        "social": ["presenca_social"],
        "tracking": [],
        "conversion": [],
        "commercial_potential": ["segmento_definido"],
    }
    for strength in analysis.strengths:
        if strength in mapping.get(dim, []):
            return True
    return False


def _has_weakness_for(analysis: Analysis, dim: str) -> bool:
    """Verdadeiro se há fraqueza relacionada à dimensão."""
    mapping = {
        "seo": ["falta_de_website"],
        "website": ["falta_de_website"],
        "social": ["falta_de_presenca_social"],
        "tracking": ["falta_de_tracking"],
        "conversion": ["falta_de_conversion"],
        "commercial_potential": [],
    }
    for weakness in analysis.weaknesses:
        if weakness in mapping.get(dim, []):
            return True
    return False


def _motivo(prioridade: Priority, analysis: Analysis) -> str:
    """Motivo adaptado ao número de forças/fraquezas."""
    if analysis.strengths and not analysis.weaknesses:
        return "Lead sólido — forças digitais consistentes."
    if analysis.weaknesses:
        return "Problemas detectados — alta oportunidade de intervenção."
    return MOTIVO_TEMPLATES.get(prioridade, "")


MOTIVO_TEMPLATES: dict[Priority, str] = {
    Priority.HIGH: "Alta presença digital e forte potencial comercial.",
    Priority.MEDIUM: "Presença digital moderada com espaço para crescimento.",
    Priority.LOW: "Presença digital limitada; oportunidade de longo prazo.",
}

NEXT_ACTION_TEMPLATES: dict[Priority, NextAction] = {
    Priority.HIGH: NextAction.CONTACT,
    Priority.MEDIUM: NextAction.EMAIL,
    Priority.LOW: NextAction.NURTURE,
}