# Decisões de Design do RADAR PUB

## 2026-10-18: Inicialização do Projeto

### Arquitetura Agentic
- Hermes como operador/orquestrador externo
- PDL como futuro Harness de execução
- Radar PUB com seus próprios domínios, memória, modelos de dados e lógica de negócio

### Modularidade
- Cada domínio em módulo independente
- Interfaces bem definidas
- Testabilidade garantida

### Dados Mockados no MVP
- Fixtures mockados para demonstração
- Sem dados reais
- Substituir por fontes reais em fases futuras

### Modelo de Dados
- Dataclasses imutáveis para entidades de valor
- Dict para payloads de transporte
- Serialização JSON
- Sem dependências externas no MVP

### Escalabilidade
- Cada agente pode rodar em paralelo via jobs assíncronos
- Memória de decisões e aprendizado
- Persistência futura em Turso/SQLite