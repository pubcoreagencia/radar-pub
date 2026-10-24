from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .catalog import Capability
from .catalog import CapabilityType as _CapabilityType


@dataclass(frozen=True)
class ServiceOffer:
    """A service offer associated with a Capability.

    Only created for capabilities with type ``service``.
    """

    id: str
    capability_id: str
    name: str
    description: str
    commercial_model: str


# Offers for SERVICE-type capabilities (type=service)
SERVICE_OFFERS: List[ServiceOffer] = [
    # pub-leads (SaaS/Produto → mapped to service type) — offers de prospecção/enriquecimento
    ServiceOffer(
        id="lead-prospecting",
        capability_id="pub-leads",
        name="Prospecting & Lead Enrichment",
        description="Apify Google Maps Scraper + Web enrichment (WhatsApp/Instagram/Email) + 3-layer qualification pipeline + Evolution API / WhatsApp Native + anti-blocking derriço + Cursor pagination + WhatsApp webhooks + CNPJ público fallback (planned)",
        commercial_model="saas crm b2b",
    ),
    ServiceOffer(
        id="lead-enrichment",
        capability_id="pub-leads",
        name="Lead Intelligence & Scoring",
        description="LeadScoringService + LeadIntentSignalsService + LeadConversionVelocityService + DealProbabilityForecasting + Signal/Capture Intelligence integration + Physical → Lead Intent integration + Audience intelligence (pseudonymous profiles, segmentation, intent bridge) + 3-layer automation",
        commercial_model="saas crm b2b",
    ),
    # Additional services from audit if any
]


def get_service_offers(capability_id: str) -> List[ServiceOffer]:
    """Return all service offers for a given capability id."""
    return [o for o in SERVICE_OFFERS if o.capability_id == capability_id]
