"""RADAR PUB — configuração central.

Centraliza pesos, thresholds, configurações do pipeline.
Evita hardcoded values espalhados pelo código.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ScoringConfig:
    """Pesos do score geral por dimensão. Somam 1.0."""
    weights: dict[str, float] = field(default_factory=lambda: {
        "seo": 0.20,
        "website": 0.25,
        "social": 0.15,
        "tracking": 0.10,
        "conversion": 0.15,
        "commercial_potential": 0.15,
    })

    # Faixas de prioridade.
    threshold_high: float = 0.70
    threshold_medium: float = 0.45

    def get_weight(self, dimension: str) -> float:
        return self.weights.get(dimension, 0.0)

    def total_weight(self) -> float:
        return sum(self.weights.values())


@dataclass(frozen=True)
class PipelineConfig:
    """Configuração do pipeline."""
    name: str = "radar-pub-mvp"
    log_level: str = "INFO"
    max_concurrent_leads: int = 10


@dataclass(frozen=True)
class RadarConfig:
    """Configuração geral do RADAR PUB."""
    scoring: ScoringConfig = field(default_factory=ScoringConfig)
    pipeline: PipelineConfig = field(default_factory=PipelineConfig)
    environment: str = "development"
    debug: bool = False


# Instância global de configuração.
CONFIG: RadarConfig = RadarConfig()


def get_config() -> RadarConfig:
    return CONFIG


def update_config(**kwargs: Any) -> None:
    """Atualiza configuração global (usar com cuidado)."""
    global CONFIG
    # Cria nova instância com overrides.
    new_scoring = kwargs.pop("scoring", CONFIG.scoring)
    new_pipeline = kwargs.pop("pipeline", CONFIG.pipeline)
    CONFIG = RadarConfig(
        scoring=new_scoring,
        pipeline=new_pipeline,
        environment=kwargs.pop("environment", CONFIG.environment),
        debug=kwargs.pop("debug", CONFIG.debug),
    )