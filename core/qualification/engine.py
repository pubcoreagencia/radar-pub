"""Módulo de qualificação — transforma Research em Score.

Fase 1: heurísticas simples baseadas em sinais e problemas.
Fase futura: ML, sinais de intenção, dados de mercado.
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities import Lead, Research, Score
from core.scoring.engine import build_score


def _dimension_score(sinais: list[str], problemas: list[str], kind: str) -> float:
    """Devolve 0..1 para uma dimensão com base em sinais e problemas."""
    # Heurística: dimensão = 1.0 se sinal presente, 0.5 se neutro, 0.0 se problema grave.
    if kind in sinais:
        return 1.0
    problem_key = f"falta_de_{kind}"
    if problem_key in problemas:
        return 0.0
    return 0.5


def qualify(lead: Lead, research: Research) -> Score:
    """Qualifica um lead: calcula dimensões e devolve Score."""
    sinais = research.sinais_encontrados
    problemas = research.problemas_detectados
    dimensoes: dict[str, float] = {
        "seo": _dimension_score(sinais, problemas, "website"),
        "website": _dimension_score(sinais, problemas, "website"),
        "social": _dimension_score(sinais, problemas, "social"),
        "tracking": _dimension_score(sinais, problemas, "tracking"),
        "conversion": _dimension_score(sinais, problemas, "conversion"),
        "commercial_potential": _dimension_score(sinais, problemas, "commercial_potential"),
    }
    return build_score(lead.lead_id, dimensoes)