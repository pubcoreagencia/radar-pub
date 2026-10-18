"""Módulo de descoberta — produz candidatos a leads.

Fase 1: usa fixtures mockados (sem dados reais).
Fase futura: múltiplas fontes (scraping, APIs, feeds).
"""
from __future__ import annotations

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.entities import Lead, LeadStatus

# Fixtures mockados — substituir por fontes reais em fases futuras.
FIXTURES: list[dict] = [
    {
        "empresa": "Acme Corp",
        "segmento": "Tecnologia",
        "localizacao": "São Paulo, BR",
        "website": "https://acme.example.com",
        "redes_sociais": ["linkedin:acme", "twitter:acme"],
        "fonte": "fixture:acme",
    },
    {
        "empresa": "Globex Ltd",
        "segmento": "Saúde",
        "localizacao": "São Paulo, BR",
        "website": "https://globex.example.com",
        "redes_sociais": ["linkedin:globex"],
        "fonte": "fixture:globex",
    },
    {
        "empresa": "Initech",
        "segmento": "Indústria",
        "localizacao": "São Paulo, BR",
        "website": None,
        "redes_sociais": [],
        "fonte": "fixture:initech",
    },
]


def discover(source: str | None = None) -> list[Lead]:
    """Descobre leads. source = nome da fonte (ex: 'fixture:acme') ou None para todas."""
    leads: list[Lead] = []
    for f in FIXTURES:
        if source and f["fonte"] != source:
            continue
        leads.append(Lead(**f))
    return leads


def discover_one(lead_id: str) -> Lead | None:
    """Busca lead pelo id."""
    for l in discover():
        if l.lead_id == lead_id:
            return l
    return None