"""RADAR PUB — domínios e modelos de dados.

Modelo de dados pensado para evoluir: múltiplas fontes, múltiplos agentes,
jobs assíncronos, execução contínua, memória, histórico de decisões,
feedback comercial e aprendizado por conversão.

Convenção: dataclasses imutáveis para entidades de valor, dict para payloads
de transporte (serializáveis para JSON). Sem dependências externas.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional
from datetime import datetime, timezone
import uuid


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Priority(str, Enum):
    HIGH = "ALTA"
    MEDIUM = "MEDIA"
    LOW = "BAIXA"
    DISQUALIFIED = "DESCARTADO"


class DigitalPresence(str, Enum):
    HIGH = "ALTA"
    MEDIUM = "MEDIA"
    LOW = "BAIXA"
    ABSENT = "AUSENTE"


class NextAction(str, Enum):
    CONTACT = "CONTATO"
    EMAIL = "EMAIL"
    NURTURE = "NUTRICAO"
    DISCARD = "DESCARTAR"


class LeadStatus(str, Enum):
    NEW = "NOVO"
    RESEARCHED = "PESQUISADO"
    SCORED = "PONTUADO"
    QUALIFIED = "QUALIFICADO"
    OUTREACH_READY = "PRONTO_PARA_ABORDAGEM"
    ARCHIVED = "ARQUIVADO"


# ---------------------------------------------------------------------------
# Lead
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Lead:
    """Empresa potencial. Fonte é um identificador de origem (ex.: 'scout:mock')."""
    empresa: str
    segmento: str = ""
    localizacao: str = ""
    website: Optional[str] = None
    redes_sociais: list[str] = field(default_factory=list)
    fonte: str = "unknown"
    lead_id: str = field(default_factory=lambda: _new_id("lead"))
    status: LeadStatus = LeadStatus.NEW
    criado_em: str = field(default_factory=_now_iso)
    metadados: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value if isinstance(self.status, LeadStatus) else self.status
        return d


# ---------------------------------------------------------------------------
# Research — presença digital, sinais, problemas, evidências
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Evidence:
    """Evidência coletada. `kind` = seo | website | social | tracking | conversion."""
    kind: str
    descricao: str
    fonte: str = ""
    coletado_em: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Research:
    """Resultado da pesquisa de presença digital de um lead."""
    lead_id: str
    presenca_digital: DigitalPresence = DigitalPresence.ABSENT
    sinais_encontrados: list[str] = field(default_factory=list)
    problemas_detectados: list[str] = field(default_factory=list)
    evidencias: list[Evidence] = field(default_factory=list)
    research_id: str = field(default_factory=lambda: _new_id("res"))
    criado_em: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["presenca_digital"] = self.presenca_digital.value
        d["evidencias"] = [e.to_dict() for e in self.evidencias]
        return d


# ---------------------------------------------------------------------------
# Analysis — forças, fraquezas, oportunidades, hipóteses
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Analysis:
    """Análise de um lead: strengths, weaknesses, opportunities, hypotheses."""
    lead_id: str
    research_id: str
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)
    opportunities: list[str] = field(default_factory=list)
    hypotheses: list[str] = field(default_factory=list)
    analysis_id: str = field(default_factory=lambda: _new_id("ana"))
    criado_em: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Score — pontuação por dimensão + score geral
# ---------------------------------------------------------------------------

# Pesos do score geral. Somam 1.0. Evoluível: viram config por segmento.
DEFAULT_WEIGHTS: dict[str, float] = {
    "seo": 0.20,
    "website": 0.25,
    "social": 0.15,
    "tracking": 0.10,
    "conversion": 0.15,
    "commercial_potential": 0.15,
}


@dataclass(frozen=True)
class Score:
    """Pontuação de um lead em 0..1 por dimensão + score geral ponderado."""
    lead_id: str
    dimensoes: dict[str, float] = field(default_factory=dict)
    pesos: dict[str, float] = field(default_factory=lambda: dict(DEFAULT_WEIGHTS))
    score_geral: float = 0.0
    score_id: str = field(default_factory=lambda: _new_id("scr"))
    criado_em: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# Opportunity — hipótese, prioridade, próxima ação
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Opportunity:
    """Resultado final: o quão boa é a oportunidade e por quê."""
    lead_id: str
    score_id: str
    score_geral: float = 0.0
    prioridade: Priority = Priority.LOW
    hipotese: str = ""
    motivo: str = ""
    proxima_acao: NextAction = NextAction.NURTURE
    opportunity_id: str = field(default_factory=lambda: _new_id("opp"))
    criado_em: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["prioridade"] = self.prioridade.value
        d["proxima_acao"] = self.proxima_acao.value
        return d


# ---------------------------------------------------------------------------
# DecisionRecord — memória de decisões (evolução futura: feedback/learning)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class DecisionRecord:
    """Registro de decisão tomada pelo motor. Base para aprendizado futuro."""
    decision_id: str = field(default_factory=lambda: _new_id("dec"))
    lead_id: str = ""
    etapa: str = ""
    decisao: str = ""
    justificativa: str = ""
    criado_em: str = field(default_factory=_now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
