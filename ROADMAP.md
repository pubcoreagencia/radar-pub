# RADAR PUB — Roadmap

## Fase 1 — Foundation (Concluída)
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

## Fase 2 — Intelligence (Concluída)
- [x] Módulo Analysis explícito (forças, fraquezas, oportunidades, hipóteses)
- [x] Explainability do scoring (explain_score, format_score_report)
- [x] Explainability do opportunity (opportunity_score, confidence_score, explain_opportunity)
- [x] Scoring baseado em Analysis (não hardcoded)
- [x] Testes de edge cases (lead vazio, dados malformados, pipeline vazio)

## Fase 3 — Persistence (Concluída)
- [x] SQLite com save/get para Leads, Research, Analysis, Score, Opportunity, Decision
- [x] Testes de persistência (save_and_get_lead, get_leads, pipeline_persists, opportunities_by_priority)
- [x] Migration v1->v2 (placeholder para futuras versões)

## Fase 4 — Continuous Execution (Concluída)
- [x] Daemon 24/7 com loops (discovery, research, qualification)
- [x] Graceful shutdown (SIGINT/SIGTERM com threading.Event)
- [x] Logging em cada loop
- [x] Persistência automática
- [x] Testes de daemon (init, discovery_loop, research_loop, qualification_loop)

## Fase 5 — API Facade (Concluída)
- [x] HTTP API (http.server stdlib)
- [x] Endpoints: /health, /discover, /opportunities, /priority-leads
- [x] HermesClient (descobrir, find_opportunities)
- [x] PDLClient (executar tarefas)
- [x] Testes de API (health, discover, priority_leads)

## Fase 6 — Outreach Slots (Concluída)
- [x] InstagramChannel (slot preparado, não configurado)
- [x] WhatsAppChannel (slot preparado, não configurado)
- [x] EmailChannel (slot preparado, não configurado)
- [x] EmailChannelSMTP (implementação SMTP)
- [x] FollowUpEngine (preparar, marcar enviado)
- [x] Testes de outreach/followup

## Fase 7 — Integration Cleanup (Concluída)
- [x] Removida duplicação core/integrations/ vs integrations/
- [x] Imports corrigidos (sem sys.path hack)
- [x] core/env.py: configuração runtime via environment variables
- [x] core/migrations.py: migration placeholder
- [x] core/merge.py: MergeReconciler para múltiplos agents

## Fase 8 — Real Data Sources (Próximo)
- [ ] Browser automation (Scrapling) para descoberta real
- [ ] APIs de dados (maps, social, news)
- [ ] Múltiplas fontes de discovery (DiscoverySource abstração)
- [ ] Pesquisa com browser real (não apenas heurísticas)
- [ ] Dados de mercado para scoring

## Fase 9 — Learning Loop (Futuro)
- [ ] Persistência de decisões em Turso
- [ ] Feedback comercial (conversão real)
- [ ] Retreino de pesos de scoring
- [ ] Aprendizado contínuo

## Fase 10 — Autonomous Prospecting (Futuro)
- [ ] Execução 24/7 em infraestrutura dedicada
- [ ] Integração Hermes como orquestrador principal
- [ ] PDL/Harness como executor de tarefas
- [ ] Agentes especializados (scout, researcher, analyst, qualifier, outreach, followup)
- [ ] Automação de outreach (com rate limiting e compliance)