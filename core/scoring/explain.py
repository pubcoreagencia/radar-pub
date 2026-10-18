"""RADAR PUB — explainability do scoring.

Responde: "Por que essa empresa recebeu X?"
"""
from __future__ import annotations

from core.entities import Score
from core.config import CONFIG


def explain_score(score: Score) -> dict[str, any]:
    """Gera relatório de explicação do score."""
    pesos = score.pesos or CONFIG.scoring.weights
    dimensoes = score.dimensoes

    linhas: list[dict[str, float]] = []
    for dim, peso in pesos.items():
        valor = dimensoes.get(dim, 0.0)
        contribuicao = round(valor * peso, 4)
        linhas.append({
            "dimensao": dim,
            "valor": valor,
            "peso": peso,
            "contribuicao": contribuicao,
        })

    return {
        "score_id": score.score_id,
        "lead_id": score.lead_id,
        "score_geral": score.score_geral,
        "explicacao": linhas,
        "resumo": _resumo(linhas, score.score_geral),
    }


def _resumo(linhas: list[dict[str, float]], score_geral: float) -> str:
    partes = [f"{l['dimensao']}={l['contribuicao']:.2f}" for l in linhas]
    return f"score_geral={score_geral:.2f} because: " + ", ".join(partes)


def format_score_report(score: Score) -> str:
    """Formata relatório legível do score."""
    exp = explain_score(score)
    linhas = [
        f"Score Report — lead {exp['lead_id']}",
        f"score_geral: {exp['score_geral']}",
        "",
        "Breakdown:",
    ]
    for l in exp["explicacao"]:
        linhas.append(f"  {l['dimensao']:20s} {l['valor']:.2f} x {l['peso']:.2f} = {l['contribuicao']:.4f}")
    linhas.append("")
    linhas.append(exp["resumo"])
    return "\n".join(linhas)