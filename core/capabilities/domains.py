# Enums de domínio para capacidades PUB.
# Cada enum inclui label amigável para UI/relatórios.

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import ClassVar


class Domain(str, Enum):
    AGENCY = "agencia"
    PROTOTYPING = "prototipacao"
    MEMORIA_CONHECIMENTO = "memoria_conhecimento"
    ROUTING_LLM = "routing_llm"
    CRM_PROSPECCAO = "crm_prospeccao"
    INTELIGENCIA_COMERCIAL = "inteligencia_comercial"
    TRANSPORTE_ORQUESTRACAO = "transporte_orquestracao"
    ECOMMERCE = "ecommerce"
    MARKETPLACE_REGIONAL = "marketplace_regional"
    INTELIGENCIA = "inteligencia"
    AUTONOMIA = "autonomia"
    LANDING_PAGES = "landing_pages"
    AGRO = "agro"

    @property
    def label(self) -> str:
        return _DOMAIN_LABELS[self]


# Labels amigáveis para relatórios e UI.

@dataclass(frozen=True)
class DomainLabel:
    value: str
    label: str

    def __str__(self) -> str:
        return self.label


# Mapeamento de cada Domain para seu label amigável.

_DOMAIN_LABELS: ClassVar[dict["Domain", str]] = {
    Domain.AGENCY: "Publicação e Descoberta",
    Domain.PROTOTYPING: "Prototipação",
    Domain.MEMORIA_CONHECIMENTO: "Memória e Conhecimento",
    Domain.ROUTING_LLM: "Gateway de Roteamento LLM",
    Domain.CRM_PROSPECCAO: "CRM e Prospecção",
    Domain.INTELIGENCIA_COMERCIAL: "Inteligência Comercial",
    Domain.TRANSPORTE_ORQUESTRACAO: "Transporte e Orquestração",
    Domain.ECOMMERCE: "E-commerce",
    Domain.MARKETPLACE_REGIONAL: "Marketplace Regional",
    Domain.INTELIGENCIA: "Inteligência (Radar PUB)",
    Domain.AUTONOMIA: "Autonomia (AGENTES PUB)",
    Domain.LANDING_PAGES: "Páginas de Aterrissagem",
    Domain.AGRO: "Agricultura",
}

# Extras convenientes para uso interno.

ALL_DOMAINS: list[Domain] = list(Domain)
ALL_DOMAIN_LABELS: list[DomainLabel] = [
    DomainLabel(d.value, d.label) for d in Domain
]

# Helper para lookups de valor→label.

_DOMAIN_LABEL_BY_VALUE: ClassVar[dict[str, DomainLabel]] = {
    label.value: label for label in ALL_DOMAIN_LABELS
}


def domain_label(domain_value: str) -> DomainLabel | None:
    return _DOMAIN_LABEL_BY_VALUE.get(domain_value)