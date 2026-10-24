# RADAR PUB

**Business Intelligence + Opportunity Intelligence Engine** para a PUB Holding.

Infraestrutura autônoma de prospecção comercial 24/7: descobre, pesquisa, analisa, pontua e gera hipóteses de oportunidade.

## Estado Atual (MVP - Fase 7 Concluída)

```text
PUB HOLDING
     ↓
RADAR PUB (intelligence engine)
  ├── Domain: Lead, Research, Analysis, Score, Opportunity, DecisionRecord
  ├── Config: ScoringConfig (pesos/thresholds centralizados)
  ├── Core: discovery, research, analysis, scoring, opportunity, memory, persistence, daemon, api, merge, env, logging, integrations
  ├── DiscoverySource abstraction (trocar fonte sem tocar pipeline)
  ├── Logging estruturado
  └── Pipeline: Discovery → Research → Analysis → Scoring → Opportunity
     ↓
Hermes (orquestrador externo) — integrations/hermes/
     ↓
PDL/Harness (futuro executor) — integrations/pdl/
     ↓
Agentes + Ferramentas + Memória
```

## Instalação

```bash
git clone https://github.com/pubcoreagencia/radar-pub.git
cd radar-pub
pip install -e .
```

## Execução

### MVP (pipeline completo, dados mockados)
```bash
python scripts/run_mvp.py
```

### Demo
```bash
python scripts/demo.py
```

### Daemon 24/7 (loops contínuos com persistência)
```bash
python scripts/run_daemon.py
```

### API HTTP (Hermes consome via GET)
```bash
python scripts/serve_api.py
# Endpoints:
#   GET /health
#   GET /discover
#   GET /opportunities?prioridade=ALTA
#   GET /priority-leads?min_score=0.8
```

### Testes
```bash
python tests/run_all.py
```

## Configuração

Copie `.env.example` para `.env` e ajuste credenciais (nunca commit `.env`):
```bash
cp .env.example .env
```

Variáveis principais:
- `RADAR_DB_PATH` — caminho do SQLite (default: `radar.db`)
- `RADAR_DISCOVERY_INTERVAL` — intervalo do loop de descoberta (segundos)
- `RADAR_RESEARCH_INTERVAL` — intervalo do loop de pesquisa (segundos)
- `RADAR_QUALIFICATION_INTERVAL` — intervalo do loop de qualificação (segundos)
- `RADAR_API_HOST` / `RADAR_API_PORT` — host/porta da API HTTP
- `HERMES_URL` / `HERMES_TOKEN` — integração Hermes
- `PDL_URL` / `PDL_TOKEN` — integração PDL/Harness
- `INSTAGRAM_USERNAME` / `INSTAGRAM_PASSWORD` — slot Instagram (não implementado)
- `WHATSAPP_PHONE` / `WHATSAPP_API_TOKEN` — slot WhatsApp (não implementado)
- `SMTP_HOST` / `SMTP_USERNAME` / `SMTP_PASSWORD` / `SMTP_FROM` — envio de email

## Limitações do MVP

- **Descoberta**: dados mockados (sem scraping real)
- **Pesquisa**: heurísticas baseadas em texto (sem browser automation)
- **Pontuação**: regras estáticas (sem ML)
- **Outreach**: slots preparados, sem envio automático
- **Persistência**: SQLite local (futuro: Turso)
- **Execução**: loops contínuos em single-thread (futuro: async + job queue)
- **Integrações**: stubs HTTP (futuro: API real do Hermes/PDL)

## Roadmap (Atualizado - Fase 7 Concluída)

### Fases Concluídas:

**Fase 1 — Foundation (Concluída)**
- [x] Estrutura de diretórios
- [x] Arquitetura definida
- [x] Modelo de domínio (Lead, Research, Analysis, Score, Opportunity, DecisionRecord)
- [x] Configuração centralizada (ScoringConfig)
- [x] Pipeline vertical (Discovery → Research → Analysis → Scoring → Opportunity)
- [x] Persistência SQLite
- [x] Logging estruturado
- [x] Testes (63 testes, 10 suites)
- [x] Documentação (README, ARCHITECTURE, ROADMAP, ADR)
- [x] Git + push para origin/main

**Fase 2 — Intelligence (Concluída)**
- [x] Módulo Analysis explícito (forças, fraquezas, oportunidades, hipóteses)
- [x] Explainability do scoring (explain_score, format_score_report)
- [x] Explainability do opportunity (opportunity_score, confidence_score, explain_opportunity)
- [x] Scoring baseado em Analysis (não hardcoded)
- [x] Testes de edge cases (lead vazio, dados malformados, pipeline vazio)

**Fase 3 — Persistence (Concluída)**
- [x] SQLite com save/get para Leads, Research, Analysis, Score, Opportunity, Decision
- [x] Testes de persistência (save_and_get_lead, get_leads, pipeline_persists, opportunities_by_priority)
- [x] Migration v1->v2 (placeholder para futuras versões)

**Fase 4 — Continuous Execution (Concluída)**
- [x] Daemon 24/7 com loops (discovery, research, qualification)
- [x] Graceful shutdown (SIGINT/SIGTERM com threading.Event)
- [x] Logging em cada loop
- [x] Persistência automática
- [x] Testes de daemon (init, discovery_loop, research_loop, qualification_loop)

**Fase 5 — API Facade (Concluída)**
- [x] HTTP API (http.server stdlib)
- [x] Endpoints: /health, /discover, /opportunities, /priority-leads
- [x] HermesClient (descobrir, find_opportunities)
- [x] PDLClient (executar tarefas)
- [x] Testes de API (health, discover, priority_leads)

**Fase 6 — Outreach Slots (Concluída)**
- [x] InstagramChannel (slot preparado, não configurado)
- [x] WhatsAppChannel (slot preparado, não configurado)
- [x] EmailChannel (slot preparado, não configurado)
- [x] EmailChannelSMTP (implementação SMTP)
- [x] FollowUpEngine (preparar, marcar enviado)
- [x] Testes de outreach/followup

**Fase 7 — Integration Cleanup (Concluída)**
- [x] Removida duplicação core/integrations/ vs integrations/
- [x] Imports corrigidos (sem sys.path hack)
- [x] core/env.py: configuração runtime via environment variables
- [x] core/migrations.py: migration placeholder
- [x] core/merge.py: MergeReconciler para múltiplos agents

### Próximas Fases:

**Fase 8 — Real Data Sources (Próximo)
- [ ] Browser automation (Scrapling) para descoberta real
- [ ] APIs de dados (maps, social, news)
- [ ] Múltiplas fontes de discovery (DiscoverySource abstração)
- [ ] Pesquisa com browser real (não apenas heurísticas)
- [ ] Dados de mercado para scoring

**Fase 9 — Learning Loop (Futuro)
- [ ] Persistência de decisões em Turso
- [ ] Feedback comercial (conversão real)
- [ ] Retreino de pesos de scoring
- [ ] Aprendizado contínuo

**Fase 10 — Autonomous Prospecting (Futuro)
- [ ] Execução 24/7 em infraestrutura dedicada
- [ ] Integração Hermes como orquestrador principal
- [ ] PDL/Harness como executor de tarefas
- [ ] Agentes especializados (scout, researcher, analyst, qualifier, outreach, followup)
- [ ] Automação de outreach (com rate limiting e compliance)

## Documentação

- `ARCHITECTURE.md` — camadas, interfaces, fluxo de dados
- `ROADMAP.md` — fases de evolução
- `docs/concepts/README.md` — conceitos do domínio
- `docs/workflows/README.md` — fluxos de trabalho
- `docs/decisions/001-initial-architecture.md` — ADR inicial

## Licença

MIT