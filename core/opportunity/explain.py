"""Função de fator de oportunidade e score de confiança.

Fase 1: heurística baseada no Analysis.
Fase futura: ML models treinados com conversão real.
"""
from __future__ import annotations

from core.entities import Analysis, Opportunity


def oportunidade_score(analysis: Analysis) -> float:
    """Calcula score de oportunidade (0..1) a partir da Analysis.

    Heurística:
      - cada força +0.2
      - cada fraqueza -0.1
      - cada oportunidade +0.15
      - normalizado para [0,1] via sigmoide para evitar extremos.
    """
    score = 0.5
    score += len(analysis.strengths) * 0.15
    score -= len(analysis.weaknesses) * 0.07
    score += len(analysis.opportunities) * 0.12
    # clamp para [0,1]
    score = max(0.0, min(1.0, score))
    return round(score, 4)


def confidence_score(analysis: Analysis, opportunity: Opportunity) -> float:
    """Score de confiança para a Opportunity gerada.

    Alta confiança se Analysis tiver hipóteses.
    Baixa confiança se campos críticos ausentes.
    """
    base = 0.5
    if analysis.hypotheses:
        base += 0.3
    if not analysis.weaknesses:
        base += 0.2
    if len(analysis.strengths) >= 2:
        base += 0.1
    return min(1.0, round(base, 4))


def explain_opportunity(analysis: Analysis, opportunity: Opportunity) -> dict:
    """Explica por quê essa Opportunity foi gerada."""
    return {
        "hipotese": opportunity.hipotese,
        "motivo": opportunity.motivo,
        "proxima_acao": opportunity.proxima_acao.value,
        "pontuacao": opportunity.score_geral,
        "prioridade": opportunity.prioridade.value,
        "strengths": analysis.strengths,
        "weaknesses": analysis.weaknesses,
        "oportunidades": analysis.opportunities,
        "habilidades_detectadas": {
            "has_website": any("website_ativo" in s for s in analysis.strengths),
            "has_social": any("presenca_social" in s for s in analysis.strengths),
            "has_segment": any("segmento_definido" in s for s in analysis.strengths),
        },
    }