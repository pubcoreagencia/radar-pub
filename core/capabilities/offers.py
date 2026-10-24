"""F3 — Capability → Offer Mapping.

Separa rigorosamente: PROBLEM → CAPABILITY → PRODUCT/SERVICE → OFFER → COMMERCIAL MODEL.

Uma capability interna NÃO vira automaticamente serviço comercial.
Capacidades com commercial_models vazio são internas (ex: AGENTES PUB).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.capabilities.catalog import Capability, get_catalog, get_capability
from core.capabilities.products import ProductOffer, get_product_offers
from core.capabilities.services import ServiceOffer, get_service_offers


@dataclass(frozen=True)
class Offer:
    """Oferta comercial derivada de uma capability.

    Distinto de Capability: uma capability pode gerar zero, uma ou múltiplas ofertas.
    Capabilidades internas (commercial_models vazio) geram ZERO ofertas.
    """
    offer_id: str
    capability_id: str
    name: str
    description: str
    type: str  # product | service
    commercial_model: str
    price_hint: str = ""
    delivery_model: str = ""
    evidence: list[str] = field(default_factory=list)


def get_offers_for_capability(capability: Capability) -> list[Offer]:
    """Retorna ofertas reais para uma capability.

    Regras:
    - capability.type == internal_capability → ZERO ofertas (não é comercial)
    - capability.commercial_models vazio → ZERO ofertas
    - capability.type in (product, service, vertical) → busca em products.py/services.py
    """
    if capability.type == "internal_capability":
        return []
    if not capability.commercial_models:
        return []

    offers: list[Offer] = []
    products = get_product_offers(capability.id)
    services = get_service_offers(capability.id)

    for p in products:
        offers.append(Offer(
            offer_id=p.offer_id if hasattr(p, "offer_id") else f"prod_{capability.id}",
            capability_id=capability.id,
            name=p.name if hasattr(p, "name") else str(p),
            description=p.description if hasattr(p, "description") else "",
            type="product",
            commercial_model=capability.commercial_models[0] if capability.commercial_models else "",
            evidence=p.evidence if hasattr(p, "evidence") else [],
        ))
    for s in services:
        offers.append(Offer(
            offer_id=s.offer_id if hasattr(s, "offer_id") else f"srv_{capability.id}",
            capability_id=capability.id,
            name=s.name if hasattr(s, "name") else str(s),
            description=s.description if hasattr(s, "description") else "",
            type="service",
            commercial_model=capability.commercial_models[0] if capability.commercial_models else "",
            evidence=s.evidence if hasattr(s, "evidence") else [],
        ))
    return offers


def get_all_offers() -> list[Offer]:
    """Retorna todas as ofertas do catálogo ativo."""
    all_offers: list[Offer] = []
    for cap in get_catalog():
        all_offers.extend(get_offers_for_capability(cap))
    return all_offers


def get_commercial_capabilities() -> list[Capability]:
    """Retorna apenas capacidades com ofertas comerciais."""
    return [c for c in get_catalog() if get_offers_for_capability(c)]


def get_internal_capabilities() -> list[Capability]:
    """Retorna capacidades internas (sem ofertas comerciais)."""
    return [c for c in get_catalog() if not get_offers_for_capability(c)]