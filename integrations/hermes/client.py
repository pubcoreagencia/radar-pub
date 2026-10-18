"""Módulo de integração com Hermes.

Hermes é o operador/orquestrador externo do Radar PUB.
Fase atual: espaço reservado — interface preparada.
Fase futura: implementação de API cliente Hermes.
"""
from __future__ import annotations


class HermesClient:
    """Cliente para integração Hermes ↔ Radar PUB.

    Hermes atua como orquestrador externo. O Radar PUB expõe
    funcionalidades via API que Hermes consome.
    """

    def __init__(self, rpc_url: str = "http://localhost:8080") -> None:
        self.rpc_url = rpc_url

    def discover(self) -> list:
        """Solicita ao Radar a descoberta de leads.

        TODO (Phase 5): implementar chamada HTTP/gRPC para Radar API.
        """
        from core.pipeline import Pipeline
        pipe = Pipeline()
        resultados = pipe.run()
        return resultados

    def find_opportunities(self) -> list:
        """Solicita ao Radar as oportunidades prioritárias."""
        from core.pipeline import Pipeline
        pipe = Pipeline()
        resultados = pipe.run()
        opps = []
        for r in resultados:
            if r["opportunity"]["prioridade"] == "ALTA":
                opps.append(r)
        return opps