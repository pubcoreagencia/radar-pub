# RADAR PUB

**Business Intelligence + Opportunity Intelligence Engine** para a PUB Holding.

Infraestrutura autônoma de prospecção comercial 24/7: descobre, pesquisa, analisa, pontua e gera hipóteses de oportunidade para empresas potenciais.

## Problema que resolve

A PUB Holding precisa identificar continuamente **quais empresas representam uma oportunidade comercial e por quê**. O Radar PUB constrói essa inteligência de forma autônoma, preparada para operar 24/7 via Hermes (orquestrador) e PDL/Harness (execução).

## Arquitetura

```
PUB Holding
     ↓
RADAR PUB (intelligence engine: Discovery → Research → Analysis → Scoring → Opportunity)
     ↓
Hermes (operador/orquestrador externo)
     ↓
PDL/Harness (futuro executor)
     ↓
Agentes + Ferramentas + Execução + Memória
```

Detalhes em [`ARCHITECTURE.md`](./ARCHITECTURE.md).

## Fluxo Principal

```mermaid
graph LR
    A[Discovery] --> B[Research]
    B --> C[Analysis]
    C --> D[Scoring]
    D --> E[Opportunity]
```

## Instalação

```bash
git clone https://github.com/pubcoreagencia/radar-pub.git
cd radar-pub
```

Sem dependências externas no MVP — apenas Python ≥ 3.11 stdlib.

## Execução

```bash
# Pipeline completo (3 leads mockados)
python scripts/run_mvp.py

# Lead específico
python scripts/demo.py Acme

# Todos os testes (22 testes)
python tests/run_all.py
```

## Estado Atual

**Fase 1 — Foundation (completa)**

- Pipeline vertical funcional: Discovery → Research → Scoring → Opportunity
- Domínio isolado: `Lead`, `Research`, `Score`, `Opportunity`, `DecisionRecord`
- Configuração centralizada: pesos de scoring e thresholds em `core/config.py`
- Abstração de fontes: `DiscoverySource` interface (MockSource implementado)
- Interfaces de integração: `integrations/hermes/`, `integrations/pdl/`
- 22 testes passando (entities, scoring, pipeline, edge cases, config)
- Dados 100% mockados/fixtures — nenhuma fonte real ainda

## Limitações

- **Dados mockados**: nenhuma fonte real implementada (web, maps, social)
- **Análise simplificada**: heurísticas básicas baseadas em website/redes sociais
- **Sem persistência**: memória volátil (perdida entre execuções)
- **Sem execução contínua**: roda uma vez, não é um loop 24/7
- **Sem LLMs**: scoring baseado em regras, não aprendizado
- **Sem outreach real**: apenas preparação de hipótese

## Score Explicável

O score geral é a soma ponderada das dimensões (pesos em `core/config.py`):

| Dimensão | Peso | Origem (MVP) |
|---|---|---|
| SEO | 0.20 | proxy via website |
| Website | 0.25 | presença de website |
| Social | 0.15 | presença de redes sociais |
| Tracking | 0.10 | placeholder |
| Conversion | 0.15 | placeholder |
| Commercial Potential | 0.15 | placeholder |

Prioridade: `score ≥ 0.70 → ALTA`, `≥ 0.45 → MEDIA`, `< 0.45 → BAIXA`.

## Roadmap

Ver [`ROADMAP.md`](./ROADMAP.md) — 8 fases: Foundation → Intelligence → Real Discovery → Continuous Execution → Hermes Integration → PDL Integration → Autonomous Prospecting → Learning Loop.

## Estrutura

```
core/           # motor de inteligência (entities, config, pipeline, módulos)
agents/         # dispositivos de processamento (futuro)
integrations/   # interfaces Hermes/PDL
tests/          # testes (entities, scoring, pipeline, edge cases, config)
scripts/        # run_mvp.py, demo.py
docs/           # concepts, workflows, decisions (ADRs)
```

## Documentação

- [`ARCHITECTURE.md`](./ARCHITECTURE.md) — camadas e decisões
- [`ROADMAP.md`](./ROADMAP.md) — 8 fases
- [`docs/decisions/`](./docs/decisions/) — ADRs

## Licença

Proprietary — PUB Holding.