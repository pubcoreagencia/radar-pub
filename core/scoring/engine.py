"""Módulo de pontuação — calcula score geral ponderado e prioridade.

Responsabilidades:
- calcular o score_geral a partir das dimensões e pesos
- classificar a prioridade (ALTA/MEDIA/BAIXA/DESCARTADO)
- calcular dimensões reais a partir de uma Analysis (única fonte de verdade)

Sem dependências externas. Evolui: pesos por segmento via config.
"""
from core.entities import Score, Priority, Analysis
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
    if score_geral < CONFIG.scoring.threshold_low:
        return Priority.DISQUALIFIED
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


# ---------------------------------------------------------------------------
# Dimensões a partir da Analysis — única fonte de verdade do score.
# ---------------------------------------------------------------------------

# Força → dimensão = 1.0. Fraqueza → dimensão = 0.0. Neutro → 0.5.
_STRENGTH_MAPPING: dict[str, list[str]] = {
    "seo": ["website_ativo"],
    "website": ["website_ativo"],
    "social": ["presenca_social"],
    "tracking": [],
    "conversion": [],
    "commercial_potential": ["segmento_definido"],
}

_WEAKNESS_MAPPING: dict[str, list[str]] = {
    "seo": ["falta_de_website"],
    "website": ["falta_de_website"],
    "social": ["falta_de_presenca_social"],
    "tracking": ["falta_de_tracking"],
    "conversion": ["falta_de_conversion"],
    "commercial_potential": [],
}


def _has_strength_for(analysis: Analysis, dim: str) -> bool:
    """Verdadeiro se há força relacionada à dimensão."""
    for strength in analysis.strengths:
        if strength in _STRENGTH_MAPPING.get(dim, []):
            return True
    return False


def _has_weakness_for(analysis: Analysis, dim: str) -> bool:
    """Verdadeiro se há fraqueza relacionada à dimensão."""
    for weakness in analysis.weaknesses:
        if weakness in _WEAKNESS_MAPPING.get(dim, []):
            return True
    return False


def compute_dimensions(analysis: Analysis) -> dict[str, float]:
    """Calcula dimensões reais do score a partir de uma Analysis.

    Heurística: strength → 1.0, weakness → 0.0, neutro → 0.5.
    Esta é a ÚNICA função usada para derivar dimensões de uma Analysis
    no pipeline. Garante que o Score produzido reflete sinais reais
    (forças/fraquezas detectadas) e não valores padrão 0.5.
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


def default_dimensions() -> dict[str, float]:
    """Dimensões padrão (todas 0.5).

    FALLBACK EXPLICITO — usar SOMENTE quando não há Analysis disponível
    (ex.: lead sem análise, dados malformados, testes de scaffolding).
    No pipeline normal, Analysis é sempre produzido por analyze()
    e compute_dimensions() deve ser usado em vez deste.
    """
    return {dim: 0.5 for dim in CONFIG.scoring.weights}