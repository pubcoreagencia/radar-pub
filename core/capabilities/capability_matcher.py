"""Radar PUB — Capability Matcher para (Lead + Research + Analysis) → PUB Capabilities.

Regras:
- Somente capacidades ATIVAS (implemented/partial) do catálogo são consideradas.
- Matching é por problems_solved (não palavras-chave).
- Se nenhuma capability corresponde, retorna lista vazia (sem artificial matches).
- Sem dependências externas, pure Python stdlib.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from core.entities import Lead, Research, Analysis
from core.capabilities.catalog import Capability, get_catalog, get_capability
from core.capabilities.products import get_product_offers
from core.capabilities.services import get_service_offers


@dataclass(frozen=True)
class CapabilityMatch:
    """Correspondência entre um problema detectado e uma capability PUB."""

    capability_id: str
    capability: Capability
    problem: str
    evidence: str
    confidence: float  # 0..1, baseado no status (implemented=0.9, partial=0.6)
    fit_level: str  # HIGH | MEDIUM | LOW
    fit_reason: str
    offers: Sequence[Any] = field(default_factory=list)

    def has_offer(self) -> bool:
        return len(self.offers) > 0


def _detect_problems(analysis: Analysis) -> Sequence[str]:
    """Extrai problemas detectados a partir da Analysis.

    Apenas `weaknesses` são tratados como PROBLEMAS reais que capacidades resolvem.
    `opportunities` são sinais de potencial, não problemas — não fazem match
    com problems_solved (evita false negatives de vocabulário).
    """
    return list(analysis.weaknesses)


def _get_evidence_for_problem(analysis: Analysis, problem: str) -> str:
    """Busca evidência textual para um problema específico."""
    if problem in analysis.weaknesses:
        return f"Fraqueza detectada: {problem}"
    if problem in analysis.opportunities:
        return f"Oportunidade identificada: {problem}"
    return f"Problema detectado: {problem}"


def _match_capability(
    capability: Capability,
    problem: str,
    analysis: Analysis,
) -> CapabilityMatch | None:
    """Verifica se uma capability resolve um problema específico."""
    if problem not in capability.problems_solved:
        return None

    evidence = _get_evidence_for_problem(analysis, problem)
    confidence = capability.confidence  # já mapeado para 0.9/0.6 pelo audit
    fit_level = "HIGH" if confidence >= 0.8 else "MEDIUM" if confidence >= 0.5 else "LOW"
    fit_reason = f"Capability {capability.name} resolve {problem} com confiança {confidence:.2f}"

    offers: list[Any] = []
    if capability.type in ("product", "vertical", "service"):
        offers.extend(get_product_offers(capability.id))
        offers.extend(get_service_offers(capability.id))

    return CapabilityMatch(
        capability_id=capability.id,
        capability=capability,
        problem=problem,
        evidence=evidence,
        confidence=confidence,
        fit_level=fit_level,
        fit_reason=fit_reason,
        offers=offers,
    )


def match_capabilities(
    lead: Lead,
    research: Research,
    analysis: Analysis,
    catalog: Sequence[Capability] | None = None,
) -> Sequence[CapabilityMatch]:
    """Encontra capacidades PUB que resolvem problemas detectados no lead.

    Regras:
    - Apenas capacidades ATIVAS (implemented/partial) são consideradas.
    - Matching é por problems_solved, não por palavras-chave.
    - Se nenhuma capability corresponde, retorna lista vazia (sem artificial matches).
    """
    if catalog is None:
        catalog = get_catalog()

    problemas = _detect_problems(analysis)
    matches: list[CapabilityMatch] = []

    for problem in problemas:
        for capability in catalog:
            match = _match_capability(capability, problem, analysis)
            if match:
                matches.append(match)

    return matches


def has_capability_match(matches: Sequence[CapabilityMatch]) -> bool:
    """Verifica se há pelo menos um match de capability."""
    return len(matches) > 0


def get_best_match(matches: Sequence[CapabilityMatch]) -> CapabilityMatch | None:
    """Retorna o match com maior confiança."""
    if not matches:
        return None
    return max(matches, key=lambda m: m.confidence)


def get_high_fit_matches(matches: Sequence[CapabilityMatch]) -> Sequence[CapabilityMatch]:
    """Filtra apenas matches com fit HIGH."""
    return [m for m in matches if m.fit_level == "HIGH"]


def get_offers_for_match(match: CapabilityMatch) -> Sequence[Any]:
    """Retorna ofertas associadas a um match."""
    return match.offers
