"""Explicação textual da oportunidade — Sprint 2 FASE 7.

Gera texto legível para o humano explicando por que a oportunidade existe,
quais capacidades PUB se aplicam, e qual a próxima ação.
"""
from __future__ import annotations

from core.entities import Opportunity, Priority, NextAction
from core.capabilities.capability_matcher import CapabilityMatch


_PRIORITY_PT = {
    Priority.HIGH: "ALTA",
    Priority.MEDIUM: "MÉDIA",
    Priority.LOW: "BAIXA",
    Priority.DISQUALIFIED: "DESCARTADO",
}

_ACTION_PT = {
    NextAction.CONTACT: "Contato comercial direto",
    NextAction.EMAIL: "Prospecção por e-mail",
    NextAction.NURTURE: "Nutrição / relacionamento",
    NextAction.DISCARD: "Descartar",
}


def explain_opportunity_text(
    opportunity: Opportunity,
    matches: list[CapabilityMatch] | None = None,
    empresa: str = "",
) -> str:
    """Monta uma explicação textual completa da oportunidade.

    Args:
        opportunity: entidade Opportunity com capability_fit/commercial_fit/confidence.
        matches: matches de capabilities que fundamentam a oportunidade (opcional).
        empresa: nome da empresa (para dar contexto ao texto).

    Returns:
        String multi-linha em português explicando a oportunidade.
    """
    matches = matches or []
    alvo = empresa or opportunity.lead_id
    linhas: list[str] = []

    linhas.append(f"Oportunidade para {alvo}:")
    linhas.append(
        f"  Score geral: {opportunity.score_geral:.2f} — prioridade {_PRIORITY_PT.get(opportunity.prioridade, str(opportunity.prioridade))}"
    )
    linhas.append(
        f"  Capability fit: {opportunity.capability_fit:.2f} | "
        f"Commercial fit: {opportunity.commercial_fit:.2f} | "
        f"Confiança: {opportunity.confidence:.2f}"
    )
    if opportunity.hipotese:
        linhas.append(f"  Hipótese: {opportunity.hipotese}")
    if opportunity.motivo:
        linhas.append(f"  Motivo: {opportunity.motivo}")

    # Capacidades que resolvem os problemas detectados
    if matches:
        linhas.append("  Capacidades PUB aplicáveis:")
        for m in matches:
            linhas.append(
                f"    - {m.capability.name} ({m.fit_level}, conf {m.confidence:.2f}): resolve '{m.problem}'"
            )
    else:
        linhas.append("  Nenhuma capacidade PUB correspondente foi mapeada.")

    acao = _ACTION_PT.get(opportunity.proxima_acao, str(opportunity.proxima_acao))
    linhas.append(f"  Próxima ação: {acao}")

    return "\n".join(linhas)


def explain_opportunity_dict(
    opportunity: Opportunity,
    matches: list[CapabilityMatch] | None = None,
) -> dict:
    """Retorna a explicação em formato dict (para API / log estruturado)."""
    matches = matches or []
    return {
        "opportunity_id": opportunity.opportunity_id,
        "lead_id": opportunity.lead_id,
        "score_geral": opportunity.score_geral,
        "prioridade": opportunity.prioridade.value,
        "capability_fit": opportunity.capability_fit,
        "commercial_fit": opportunity.commercial_fit,
        "confidence": opportunity.confidence,
        "hipotese": opportunity.hipotese,
        "motivo": opportunity.motivo,
        "proxima_acao": opportunity.proxima_acao.value,
        "capabilities": [
            {
                "capability_id": m.capability_id,
                "name": m.capability.name,
                "fit_level": m.fit_level,
                "confidence": m.confidence,
                "problem": m.problem,
            }
            for m in matches
        ],
    }
