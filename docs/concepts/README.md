# Conceitos do RADAR PUB

## Pipeline Vertical (MVP)

```
Discovery → Research → Analysis → Scoring → Opportunity
```

## Loops Futuros

- **Discovery Loop** - descoberta contínua de novos leads
- **Research Loop** - pesquisa contínua de presença digital
- **Qualification Loop** - qualificação contínua de leads
- **Outreach Loop** - preparação de abordagem
- **Follow-up Loop** - follow-up pós-contato
- **Learning Loop** - aprendizado com resultados

## Domínios

### Lead
Empresa potencial com dados básicos: nome, segmento, localização, website, redes sociais.

### Research
Resultado da pesquisa de presença digital: presença, sinais, problemas, evidências.

### Score
Pontuação por dimensão (SEO, website, social, tracking, conversion, commercial potential) com score geral ponderado.

### Opportunity
Resultado final: prioridade, hipótese, motivo, próxima ação.

### DecisionRecord
Registro de decisões tomadas pelo motor, base para aprendizado futuro.

## Princípios

1. **Modularidade** - cada domínio é independente
2. **Observabilidade** - logging estruturado em cada etapa
3. **Testabilidade** - interfaces bem definidas, injeção de dependências
4. **Escalabilidade** - cada agente pode rodar em paralelo
5. **Persistência** - memória de decisões e aprendizado
6. **Integração** - Hermes como orquestrador externo, PDL como futuro Harness