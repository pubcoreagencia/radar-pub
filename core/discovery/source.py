"""RADAR PUB — abstração de fontes de descoberta.

Permite trocar fontes de dados sem alterar o pipeline.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from core.entities import Lead


class DiscoverySource(ABC):
    """Interface para fontes de descoberta de leads."""

    name: str = "base"

    @abstractmethod
    def discover(self, source: str | None = None) -> list[Lead]:
        """Retorna lista de leads da fonte."""
        ...

    def __iter__(self) -> Iterator[Lead]:
        """Itera sobre todos os leads da fonte."""
        for lead in self.discover():
            yield lead


class MockDiscoverySource(DiscoverySource):
    """Fonte mockada para MVP. Substituir por fontes reais em fases futuras."""

    name = "mock"

    def __init__(self) -> None:
        from core.discovery.engine import FIXTURES
        self._fixtures = FIXTURES

    def discover(self, source: str | None = None) -> list[Lead]:
        from core.discovery.engine import discover
        return discover(source)


class CompositeDiscoverySource(DiscoverySource):
    """Combina múltiplas fontes de descoberta."""

    name = "composite"

    def __init__(self, sources: list[DiscoverySource] | None = None) -> None:
        self._sources = sources or [MockDiscoverySource()]

    def add_source(self, source: DiscoverySource) -> None:
        self._sources.append(source)

    def discover(self, source: str | None = None) -> list[Lead]:
        leads: list[Lead] = []
        for s in self._sources:
            leads.extend(s.discover(source))
        return leads


# Fonte padrão.
DEFAULT_SOURCE: DiscoverySource = MockDiscoverySource()