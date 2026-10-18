"""Módulo de pontuação — calcula score geral ponderado e prioridade.

Responsabilidades:
- calcular o score_geral a partir das dimensões e pesos
- classificar a prioridade (ALTA/MEDIA/BAIXA/DESCARTADO)

Sem dependências externas. Evolui: pesos por segmento via config.
"""
from core.entities import Score, Priority
from core.config import CONFIG


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def compute_score_geral(dimensoes: dict[str, float], pesos: dict[str, float]) -> float:
    """Score geral = soma(dimensoes[k] * pesos[k]) / soma(pesos[k presentes])."""
    total_w = 0.0
    total_v = 0.0
    for k, w in pesos.items():
        if k in dimensoes:
            total_v += clamp(dimensoes[k]) * w
            total_w += w
    if total_w == 0:
        return 0.0
    return round(total_v / total_w, 4)


def classify_prioridade(score_geral: float) -> Priority:
    if score_geral >= CONFIG.scoring.threshold_high:
        return Priority.HIGH
    if score_geral >= CONFIG.scoring.threshold_medium:
        return Priority.MEDIUM
    return Priority.LOW


def build_score(lead_id: str, dimensoes: dict[str, float], pesos: dict[str, float] | None = None) -> Score:
    from core.entities import DEFAULT_WEIGHTS
    p = pesos or dict(DEFAULT_WEIGHTS)
    g = compute_score_geral(dimensoes, p)
    return Score(lead_id=lead_id, dimensoes=dimensoes, pesos=p, score_geral=g)