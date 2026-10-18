# ADR 001: Inicialização do Projeto — Arquitetura Base

## Contexto

O Radar PUB precisa ser inicializado como uma infraestrutura autônoma de prospecção 24/7. A decisão arquitetural central é não acoplar toda a lógica ao Hermes, mantendo Radar como uma engine independente.

## Decisão

- **Arquitetura Layered**: Domain, Config, Core, Agents, Integration, Tests, Scripts
- **Sem dependências externas no MVP**: apenas Python stdlib
- **Dataclasses imutáveis** para entidades de valor
- **DiscoverySource abstract interface** para futuras múltiplas fontes
- **Configuração centralizada** em `core/config.py`

## Consequências

- Evita hardcoded values espalhados
- Permite troca de fontes sem alterar pipeline
- Permite testes unitários isolados
- Permite futura persistência (Turso/SQLite)
- Permite futura integração com Hermes/PDL sem acoplamento

---

# ADR 002: Configuração Centralizada

## Contexto

Pesos do scoring e thresholds estavam potencialmente hardcoded, dificultando evolução.

## Decisão

- `core/config.py` centraliza todos os valores de configuração
- `ScoringConfig`, `PipelineConfig`, `RadarConfig` como dataclasses imutáveis
- Singleton global `CONFIG` para acesso fácil
- Thresholds movidos de `core/scoring/engine.py` para `core/config.py`

## Consequências

- Alterar peso/threshold = mudar config, não código de engine
- Facilita A/B testing futuro
- Evita magic numbers