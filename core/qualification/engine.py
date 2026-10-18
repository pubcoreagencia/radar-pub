"""Módulo de qualification — transforma Research + Analysis em Opportunity.

Fase 1: heurísticas baseadas em sinais e problemas.
Fase futura: ML, sinais de intenção, dados de mercado.
"""
from core.entities import Lead, Research, Analysis, Score, Opportunity, Priority, NextAction
from core.scoring.engine import build_score, classify_prioridade, compute_dimensions
from core.logging import log_event
from core.config import CONFIG


def qualify(lead: Lead, research: Research, analysis: Analysis, pipeline_score: Score | None = None) -> Opportunity:
    """Qualifica um lead: gera Opportunity baseada em Score.

    Se `pipeline_score` for fornecido, é usado EXATAMENTE — não recálculo.
    Se None, calcula fallback a partir da Analysis (compatibilidade) e
    registra log_event identificável ("qualification_score_fallback_used").
    """
    if pipeline_score is None:
        log_event("qualification_score_fallback_used", lead_id=lead.lead_id,
                  motivo="pipeline_score_fornecido_nao_recalcular", pipeline_score=False)
        dimensoes = compute_dimensions(analysis)
        score = build_score(lead.lead_id, dimensoes)
    else:
        score = pipeline_score

    if not analysis.hypotheses:
        from core.opportunity.engine import generate_opportunity
        # Extract capability dimensions from the effective score (handles fallback)
        capability_fit = score.dimensoes.get("capability_fit", 0.0)
        commercial_fit = score.dimensoes.get("commercial_fit", 0.0)
        confidence = score.dimensoes.get("confidence", 0.0)
        # Call generate_opportunity and then augment with capability dimensions
        opp = generate_opportunity(lead, research, score)
        # Create new opportunity with extracted capability dimensions
        return Opportunity(
            lead_id=opp.lead_id,
            score_id=opp.score_id,
            score_geral=opp.score_geral,
            prioridade=opp.prioridade,
            hipotese=opp.hipotese,
            motivo=opp.motivo,
            proxima_acao=opp.proxima_acao,
            capability_fit=capability_fit,
            commercial_fit=commercial_fit,
            confidence=confidence,
            opportunity_id=opp.opportunity_id,
            criado_em=opp.criado_em,
        )

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
        capability_fit=score.dimensoes.get("capability_fit", 0.0),
        commercial_fit=score.dimensoes.get("commercial_fit", 0.0),
        confidence=score.dimensoes.get("confidence", 0.0),
    )


def _compute_dimensoes(analysis: Analysis) -> dict[str, float]:
    """Compatibilidade: delega para core.scoring.engine.compute_dimensions.

    Mantém chamadas antigas funcionando. O caminho preferencial é
    core.scoring.engine.compute_dimensions(analysis).
    """
    return compute_dimensions(analysis)


def _has_strength_for(analysis: Analysis, dim: str) -> bool:
    """Verdadeiro se há força relacionada à dimensão.

    Mantém compatibilidade. A implementação real está em
    core.scoring.engine._has_strength_for.
    """
    from core.scoring.engine import _has_strength_for as _real_has_strength_for
    return _real_has_strength_for(analysis, dim)


def _has_weakness_for(analysis: Analysis, dim: str) -> bool:
    """Verdadeiro se há fraqueza relacionada à dimensão.

    Mantém compatibilidade. A implementação real está em
    core.scoring.engine._has_weakness_for.
    """
    from core.scoring.engine import _has_weakness_for as _real_has_weakness_for
    return _real_has_weakness_for(analysis, dim)


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