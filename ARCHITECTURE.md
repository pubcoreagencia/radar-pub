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
- Entidades: `Lead`, `Research`, `Score`, `Opportunity`
- Validações de domínio
- Regras de negócio

### Camada de Core (Core Layer)
- `core/discovery` - descoberta de leads
- `core/research` - pesquisa de presença digital
- `core/qualification` - qualificação de leads
- `core/scoring` - pontuação baseada em critérios
- `core/outreach` - preparação de abordagem (espaço reservado)
- `core/followup` - preparação de follow-up (espaço reservado)
- `core/memory` - histórico de decisões e aprendizado

### Camada de Agentes (Agent Layer)
- `agents/scout` - descobridor de leads
- `agents/researcher` - pesquisador digital
- `agents/analyst` - analista de dados
- `agents/qualifier` - qualificador de oportunidades
- `agents/outreach` - preparador de abordagem (espaço reservado)
- `agents/followup` - preparador de follow-up (espaço reservado)

### Camada de Integração (Integration Layer)
- `integrations/hermes` - integração com Hermes
- `integrations/pdl` - integração com PDL/Harness

### Camada de Testes (Test Layer)
- `tests/` - testes unitários e de integração

## Fluxo Vertical (MVP)

```
Discovery → Research → Analysis → Scoring → Opportunity
```

## Principais Decisões de Arquitetura

1. **Modularidade**: Cada domínio é independente e pode ser modificado sem afetar outros.
2. **Observabilidade**: Logging estruturado em cada etapa.
3. **Testabilidade**: Interfaces bem definidas, injeção de dependências.
4. **Escalabilidade**: Cada agente pode rodar em paralelo via jobs assíncronos.
5. **Persistência**: Memória de decisões e aprendizado.
6. **Integração**: Hermes como orquestrador externo, PDL como futuro Harness.

## Futuras Extensões

- Múltiplas fontes de leads
- Múltiplos agentes paralelos
- Jobs assíncronos (Redis/queue)
- Execução contínua 24/7
- Memória de longo prazo
- Feedback comercial
- Aprendizado baseado em conversão
- Ferramentas externas e APIs
- Browser automation
- CRM integration
- Canais de outreach