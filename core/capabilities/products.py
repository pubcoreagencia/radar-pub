from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .catalog import Capability
from .catalog import CapabilityType as _CapabilityType


@dataclass(frozen=True)
class ProductOffer:
    """A product offer associated with a Capability.

    Only created for capabilities with type ``product`` or ``vertical``.
    """

    id: str
    capability_id: str
    name: str
    description: str
    commercial_model: str


# Offers for PRODUCT-type capabilities (type=product)
PRODUCT_OFFERS: List[ProductOffer] = [
    # pub-ecom: plataforma e-commerce
    ProductOffer(
        id="ecom-platform",
        capability_id="pub-ecom",
        name="Plataforma E-commerce",
        description="Node.js HTTP API + PostgreSQL + TanStack Start frontend + Cloudflare Workers deploy + Supabase auth/RLS + Catalog Worker + Shopee Scraper ingestion + Checkout lifecycle + secure RPC + strict RLS + atomic inventory reservation",
        commercial_model="plataforma e-commerce",
    ),
    # feira-virtual: marketplace regional
    ProductOffer(
        id="marketplace-regional",
        capability_id="feira-virtual",
        name="Marketplace Regional",
        description="Node.js 22 + TypeScript + Express + SPA HTML5 + Multi-produtor checkout (decomposição por produtor) + Controle estoque atômico (InsufficientStockError) + Taxa 5% + entrega determinística (R$8 mesma cidade, R$15 entre cidades) + CI/CD GitHub Actions + Dockerfile multi-stage",
        commercial_model="marketplace regional",
    ),
    # pub-pulse-saas: landing pages (partial V0)
    ProductOffer(
        id="landing-page-builder",
        capability_id="pub-pulse-saas",
        name="Landing Page Builder",
        description="React 19 + Vite + Tailwind + aceternity + lucide-react + dist/ build exists + design evidence screenshots (partial V0)",
        commercial_model="serviço de landing page",
    ),
]


def get_product_offers(capability_id: str) -> List[ProductOffer]:
    """Return all product offers for a given capability id."""
    return [o for o in PRODUCT_OFFERS if o.capability_id == capability_id]
