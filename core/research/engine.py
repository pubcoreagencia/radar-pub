"""Módulo de pesquisa — coleta presença digital e sinais de um lead.

Fase 1: usa heurísticas baseadas no lead (website, redes sociais).
Fase futura: browser automation, APIs, SEO tools.
"""
from core.entities import Lead, Research, Evidence, DigitalPresence


def _has_website(lead: Lead) -> bool:
    return bool(lead.website)


def _has_social(lead: Lead) -> bool:
    return len(lead.redes_sociais) > 0


def _estimate_presence(lead: Lead) -> DigitalPresence:
    """Heurística simples: website + redes sociais = ALTA; só um = MEDIA; nada = AUSENTE."""
    w = _has_website(lead)
    s = _has_social(lead)
    if w and s:
        return DigitalPresence.HIGH
    if w or s:
        return DigitalPresence.MEDIUM
    return DigitalPresence.ABSENT


def _detect_problems(lead: Lead) -> list[str]:
    """Detecta problemas comuns com base no lead."""
    problemas: list[str] = []
    if not lead.website:
        problemas.append("falta_de_website")
    elif "https://" not in (lead.website or ""):
        problemas.append("website_nao_seguro")
    if not lead.redes_sociais:
        problemas.append("falta_de_presenca_social")
    return problemas


def _collect_evidences(lead: Lead) -> list[Evidence]:
    """Coleta evidências mockadas."""
    evs: list[Evidence] = []
    if lead.website:
        evs.append(Evidence(kind="website", descricao="website detectado", fonte="lead"))
    if lead.redes_sociais:
        evs.append(Evidence(kind="social", descricao="redes detectadas", fonte="lead"))
    return evs


def research_lead(lead: Lead) -> Research:
    """Pesquisa um lead e devolve Research."""
    sinais: list[str] = []
    if _has_website(lead):
        sinais.append("website")
    if _has_social(lead):
        sinais.append("social")
    presenca = _estimate_presence(lead)
    problemas = _detect_problems(lead)
    evidencias = _collect_evidences(lead)
    return Research(
        lead_id=lead.lead_id,
        presenca_digital=presenca,
        sinais_encontrados=sinais,
        problemas_detectados=problemas,
        evidencias=evidencias,
    )