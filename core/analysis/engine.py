"""RADAR PUB — Analysis module.

Transforma Research em Analysis: strengths, weaknesses, opportunities, hypotheses.

Fase 1: heurísticas baseadas em sinais e problemas.
Fase futura: ML, NLP, dados de mercado.
"""
from __future__ import annotations

from core.entities import Lead, Research, Analysis


def analyze(lead: Lead, research: Research) -> Analysis:
    """Gera Analysis a partir de Lead + Research."""
    strengths = _detect_strengths(lead, research)
    weaknesses = _detect_weaknesses(lead, research)
    opportunities = _detect_opportunities(lead, research)
    hypotheses = _build_hypotheses(lead, research, strengths, weaknesses, opportunities)

    return Analysis(
        lead_id=lead.lead_id,
        research_id=research.research_id,
        strengths=strengths,
        weaknesses=weaknesses,
        opportunities=opportunities,
        hypotheses=hypotheses,
    )


def _detect_strengths(lead: Lead, research: Research) -> list[str]:
    """Detecta forças do lead."""
    strengths: list[str] = []
    if "website" in research.sinais_encontrados:
        strengths.append("website_ativo")
    if "social" in research.sinais_encontrados:
        strengths.append("presenca_social")
    if lead.segmento:
        strengths.append("segmento_definido")
    return strengths


def _detect_weaknesses(lead: Lead, research: Research) -> list[str]:
    """Detecta fraquezas do lead."""
    weaknesses: list[str] = []
    for problema in research.problemas_detectados:
        weaknesses.append(problema)
    if not lead.segmento:
        weaknesses.append("segmento_nao_definido")
    return weaknesses


def _detect_opportunities(lead: Lead, research: Research) -> list[str]:
    """Detecta oportunidades de intervenção."""
    opportunities: list[str] = []
    if "falta_de_website" in research.problemas_detectados:
        opportunities.append("construicao_website")
    if "falta_de_presenca_social" in research.problemas_detectados:
        opportunities.append("marketing_digital")
    if "website_nao_seguro" in research.problemas_detectados:
        opportunities.append("seguranca_web")
    if not research.problemas_detectados:
        opportunities.append("profundamento_relacionamento")
    return opportunities


def _build_hypotheses(
    lead: Lead,
    research: Research,
    strengths: list[str],
    weaknesses: list[str],
    opportunities: list[str],
) -> list[str]:
    """Gera hipóteses de intervenção."""
    hypotheses: list[str] = []
    for opp in opportunities:
        if opp == "construicao_website":
            hypotheses.append("A empresa não possui website. O Pub pode oferecer construção de presença digital.")
        elif opp == "marketing_digital":
            hypotheses.append("A empresa não está em redes sociais. O Pub pode atuar em marketing digital.")
        elif opp == "seguranca_web":
            hypotheses.append("Website não é seguro. O Pub pode sugerir migração para HTTPS e melhoria de conversão.")
        elif opp == "profundamento_relacionamento":
            hypotheses.append("Lead com presença digital sólida; oportunidade para aprofundamento de relacionamento.")
    return hypotheses