# RADAR PUB - Arquitetura

## Visão Geral

O Radar PUB é uma infraestrutura autônoma de prospecção comercial 24/7. Concebido como uma arquitetura agentic/autônoma, preparada para operar continuamente através do Hermes e posteriormente integrada ao PDL (PUB Dev Loop) como Harness de orquestração.

## Princípio Arquitetural

```
RADAR PUB (business intelligence + opportunity engine)
        ↓
Hermes (operador/orquestrador externo)
        ↓
PDL/Harness (futuro executor de agentes)
        ↓
Agentes + Ferramentas + Execução
```

**Hermes é o operador/orquestrador externo.** O Radar PUB possui seus próprios domínios, memória, modelos de dados e lógica de negócio. Não acouple toda a lógica diretamente ao Hermes.

## Camadas

### Camada de Domínio (Domain Layer)
- `core/entities.py` - Entidades: `Lead`, `Research`, `Score`, `Opportunity`, `DecisionRecord`
- Enums: `Priority`, `DigitalPresence`, `NextAction`, `LeadStatus`
- Validações de domínio
- Regras de negócio

### Camada de Configuração (Config Layer)
- `core/config.py` - Configuração central: pesos do scoring, thresholds, pipeline config
- Evita values hardcoded espalhados pelo código

### Camada de Core (Core Layer)
- `core/discovery/` - descoberta de leads + source abstraction (`DiscoverySource` interface)
- `core/research/` - pesquisa de presença digital
- `core/qualification/` - qualificação de leads (transforma Research em Score)
- `core/scoring/` - pontuação baseada em critérios + classificação de prioridade
- `core/opportunity/` - geração de hipóteses e próximas ações
- `core/memory/` - histórico de decisões e aprendizado
- `core/logging.py` - logging estruturado
- `core/pipeline.py` - pipeline vertical de orquestração

### Camada de Agentes (Agent Layer)
- `agents/scout/` - descobridor de leads
- `agents/researcher/` - pesquisador digital
- `agents/analyst/` - analista de dados
- `agents/qualifier/` - qualificador de oportunidades
- `agents/outreach/` - preparador de abordagem (espaço reservado)
- `agents/followup/` - preparador de follow-up (espaço reservado)

### Camada de Integração (Integration Layer)
- `integrations/hermes/` - integração com Hermes (orquestrador)
- `integrations/pdl/` - integração com PDL/Harness (futuro executor)

### Camada de Testes (Test Layer)
- `tests/` - testes unitários, edge cases e de configuração

### Camada de Scripts (Scripts Layer)
- `scripts/` - scripts de demo e execução

## Fluxo Vertical (MVP)

```
Discovery → Research → Analysis → Scoring → Opportunity
```

O `Pipeline` em `core/pipeline.py` orquestra esse fluxo vertical.

## Fluxos Futuros (Loops 24/7)

```
DISCOVERY LOOP → RESEARCH LOOP → QUALIFICATION LOOP →
OPPORTUNITY LOOP → OUTREACH LOOP → FOLLOW-UP LOOP →
LEARNING LOOP (↺)
```

## Principais Decisões de Arquitetura

1. **Modularidade**: Cada domínio é independente e pode ser modificado sem afetar outros.
2. **Observabilidade**: Logging estruturado via `core/logging.py`.
3. **Testabilidade**: Interfaces bem definidas, injeção de dependências, mocks isolados.
4. **Escalabilidade**: Cada agente pode rodar em paralelo via jobs assíncronos.
5. **Extensibilidade**: `DiscoverySource` abstrato permite múltiplas fontes.
6. **Configuração Centralizada**: `core/config.py` centraliza pesos e thresholds.
7. **Integração**: Hermes como orquestrador externo; PDL como futuro Harness.

## Futuras Extensões

- Múltiplas fontes de leads (DiscoverySource abstraction)
- Múltiplos agentes paralelos
- Jobs assíncronos (Redis/queue)
- Execução contínua 24/7
- Memória de longo prazo (persistência)
- Feedback comercial
- Aprendizado baseado em conversão
- Ferramentas externas e APIs
- Browser automation
- CRM integration
- Canais de outreach