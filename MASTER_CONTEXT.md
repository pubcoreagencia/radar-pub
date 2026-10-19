# PUB RADAR — MASTER CONTEXT

> **Documento canônico de contexto arquitetural e estratégico do PUB RADAR.**
>
> Este arquivo registra as decisões consolidadas da arquitetura do RADAR e deve ser consultado antes de novas decisões de produto, integração, criação de capabilities, mods ou refactors.

## 1. Visão

**PUB RADAR** é o **Orquestrador Operacional da PUB Holding**.

O RADAR deixou de ser entendido apenas como um Business Intelligence / Opportunity Intelligence Engine isolado. Sua direção estratégica é tornar-se a camada que:

- entende o objetivo;
- planeja o que precisa acontecer;
- resolve quais capabilities podem executar cada etapa;
- seleciona e compõe sistemas e módulos;
- delega execução;
- acompanha estado e evidências;
- toma decisões;
- devolve resultados para os sistemas operacionais;
- aprende com os resultados.

O RADAR **não substitui os sistemas especializados da PUB**. Ele os conecta e orquestra.

### Princípio central

> **RADAR decide/componha/orquestra; os sistemas especializados executam suas responsabilidades canônicas.**

---

## 2. Decisão crítica: Hermes é transitório

**Hermes NÃO é um produto PUB, NÃO é uma capability comercial PUB e NÃO deve ser tratado como mod estratégico do RADAR.**

O Hermes atualmente funciona como uma **camada provisória de full-stack agentic execution/orchestration** enquanto o PDL ainda não possui toda a capacidade necessária.

### Estado atual

```
RADAR → PDL → HERMES → AGENTS → TOOLS
                         ↑
                    provisório
```

### Estado futuro

```
RADAR → PDL → AGENTS → TOOLS
          ↑
      execução autônoma
```

Quando o PDL tiver capacidade suficiente, o Hermes será retirado progressivamente dessa posição.

### Regra arquitetural

O RADAR deve ser projetado contra um **contrato de runtime de execução**, e não contra a arquitetura interna do Hermes.

Hermes é uma dependência de transição.

O objetivo não é "integrar o RADAR ao Hermes" como destino arquitetural.

O objetivo é:

> **RADAR integrar um runtime de execução, usando Hermes como runtime provisório e PDL como runtime estratégico.**

### Classificação

```yaml
hermes:
  type: transitional_runtime
  owner: external
  strategic: false
  pub_product: false
  replacement: pdl
  status: temporary
```

Não criar novos produtos, capabilities ou catálogos do RADAR baseados em Hermes.

---

## 3. Papel do PDL

**PUB Dev Loop (PDL)** é o Harness de execução autônoma estratégico.

O PDL deve substituir a camada provisória do Hermes à medida que atingir maturidade suficiente para:

- executar agentes;
- executar ferramentas;
- operar workflows;
- validar resultados;
- recuperar falhas;
- manter contexto;
- produzir evidências;
- persistir estado;
- realizar operações full-stack;
- executar tarefas de desenvolvimento e automação de forma autônoma.

### Separação

- **RADAR** = orquestração operacional da Holding.
- **PDL** = harness/runtime de execução.
- **Hermes** = runtime transitório enquanto o PDL não cobre a capacidade necessária.

---

## 4. Arquitetura-alvo

```
                         PUB HOLDING
                             │
                             ▼
                    ┌─────────────────┐
                    │    PUB RADAR    │
                    │                 │
                    │ ORQUESTRATOR    │
                    │ Decide          │
                    │ Planeja         │
                    │ Delega          │
                    │ Compõe          │
                    │ Observa         │
                    │ Aprende         │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
          ▼                  ▼                  ▼
     PUB LEADS          PUB RESEARCH       PUB MACHINE
     acquisition        intelligence       scoring
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                             ▼
                         PUB WAR
                   commercial knowledge
                             │
          ┌──────────────────┼──────────────────┐
          ▼                  ▼                  ▼
        NEURAL             PDL              MODS
       knowledge         execution        capabilities
                             │
                             ▼
                       AGENTS / TOOLS
                             │
                             ▼
                          EVIDENCE
                             │
                             ▼
                           RADAR
```

---

## 5. Sistemas canônicos da PUB

O RADAR deve **consumir capabilities dos sistemas existentes**, e não recriar suas responsabilidades.

### PUB Leads

Responsabilidade canônica:

- prospecção;
- aquisição de dados;
- enriquecimento;
- contatos;
- qualificação operacional;
- CRM;
- pipeline;
- outreach;
- WhatsApp;
- gestão comercial de leads.

PUB Leads é principalmente **lead-centric**.

### PUB Research

Responsabilidade canônica:

```
SOURCE
↓
CAPTURE
↓
EXTRACT
↓
NORMALIZE
↓
ANALYZE
↓
QUALIFY
↓
PERSIST
```

Produz:

- evidências;
- URLs/fontes;
- conteúdo bruto;
- OCR;
- transcrição;
- entidades;
- tópicos;
- claims;
- produtos;
- marcas;
- insights;
- oportunidades;
- relevância;
- qualificação;
- provenance.

O RADAR deve consumir Research como fonte de inteligência/evidência, e não recriar um Research Engine paralelo.

### PUB Machine

Responsabilidade canônica de inteligência comercial:

- lead scoring;
- intent signals;
- lead enrichment intelligence;
- prioritization;
- conversion velocity;
- deal velocity;
- deal probability;
- forecasting;
- audience intelligence;
- segmentation;
- recommended actions.

**Não duplicar esses engines no RADAR.**

### PUB WAR

Responsabilidade canônica comercial:

- catálogo de ofertas;
- capabilities comerciais;
- produtos;
- serviços;
- ICPs;
- sinais;
- canais;
- ofertas de entrada;
- upsell;
- recorrência;
- modelos comerciais;
- funil comercial;
- evidências de entrega.

Regra comercial:

```
CATÁLOGO AMPLO
→ PORTFÓLIO PRIORITÁRIO
→ SKU DE ENTRADA
→ UPSELL
→ RECORRÊNCIA
→ REPLICAÇÃO
```

O RADAR não deve criar um segundo catálogo comercial.

### PUB Neural

Responsabilidade canônica de memória/knowledge:

```
REPOSITORY
→ AUDIT
→ DISCOVERY
→ CLASSIFICATION
→ EXTRACTION
→ NORMALIZATION
→ PROVENANCE
→ VALIDATION
→ FUSION
→ NEURAL
```

Regra:

> UNKNOWN não significa DOES NOT EXIST.

O RADAR não deve virar um segundo sistema de memória institucional.

---

## 6. Opportunity Intelligence — domínio próprio do RADAR

Embora o RADAR seja o orquestrador geral, sua inteligência proprietária deve continuar concentrada em **Opportunity Intelligence**.

Responsabilidades próprias:

- Opportunity Context;
- Evidence Fusion;
- Problem Detection;
- Problem Hypothesis;
- Capability Resolution;
- Capability Fit;
- Commercial Fit;
- Opportunity Reasoning;
- Opportunity Score;
- Confidence;
- Explainability;
- Opportunity Ranking;
- Next Action;
- Outcome Feedback;
- Learning.

### Distinção fundamental

**Lead Score** e **Opportunity Score** não são a mesma coisa.

PUB Machine pode produzir:

```
Lead Score = 90
Opportunity Score = 20
```

Isso é válido se o lead for atraente, mas não houver fit real com uma solução PUB.

Também pode ocorrer:

```
Lead Score = 55
Opportunity Score = 88
```

quando houver dor clara, evidência forte e alto fit entre capability e oferta.

### Regra

- **PUB Machine owns Lead / Intent Score**
- **RADAR owns Opportunity Score**

Nunca criar dois engines concorrentes para o mesmo score.

---

## 7. Capability Registry

O RADAR precisa de um **Capability Registry**, não de uma coleção de implementações duplicadas.

Exemplos de capabilities:

```
discover_company
enrich_company
research_web
extract_evidence
ocr
transcribe
score_lead
detect_intent
find_opportunity
match_capability
generate_offer
send_whatsapp
send_email
manage_crm
create_prototype
modify_code
run_tests
commit_code
deploy
observe_metrics
learn_from_result
```

Cada capability deve registrar:

```
capability
├── provider
├── mod
├── version
├── inputs
├── outputs
├── cost
├── permissions
├── reliability
├── latency
└── evidence requirements
```

O RADAR pergunta:

> "Quem consegue executar esta capability?"

e não:

> "Como o PUB Leads implementa isso internamente?"

---

## 8. Mod Runtime

O RADAR deverá utilizar uma arquitetura modular.

Estrutura conceitual:

```
radar/
├── core/
│   ├── orchestrator/
│   ├── planner/
│   ├── router/
│   ├── state/
│   ├── events/
│   ├── policies/
│   ├── contracts/
│   └── execution/
│
├── mods/
│   ├── leads/
│   ├── research/
│   ├── machine/
│   ├── neural/
│   ├── war/
│   ├── pdl/
│   ├── browser/
│   ├── github/
│   ├── social/
│   ├── seo/
│   ├── analytics/
│   └── scraping/
│
├── agents/
├── workflows/
├── adapters/
├── sdk/
└── cli/
```

Um mod expõe capabilities através de contratos.

Exemplo:

```yaml
name: pub-leads
version: 1.0
capabilities:
  - discover_companies
  - enrich_company
  - find_contacts
  - manage_pipeline
```

Outro:

```yaml
name: pub-research
capabilities:
  - web_research
  - extract_evidence
  - analyze_source
  - provenance
```

Outro:

```yaml
name: pub-machine
capabilities:
  - lead_scoring
  - intent_detection
  - prioritization
  - forecasting
```

Os mods devem ser reutilizáveis pelo RADAR e, quando fizer sentido, por projetos externos/futuros.

---

## 9. Open Source / Reutilização

A estratégia é desenvolver ferramentas modulares que possam compor o RADAR, mas que também possam suprir necessidades de outros projetos.

Exemplos potenciais:

```
PUB RADAR CORE
        │
        ├── radar-mod-leads
        ├── radar-mod-research
        ├── radar-mod-browser
        ├── radar-mod-github
        ├── radar-mod-seo
        ├── radar-mod-social
        ├── radar-mod-analytics
        ├── radar-mod-scraper
        ├── radar-mod-memory
        └── radar-mod-pdl
```

Esses módulos não devem ser criados artificialmente apenas para preencher uma arquitetura.

### DNA de criação de módulos

```
NECESSIDADE
↓
AUDITORIA
↓
JÁ EXISTE?
├── SIM → ADAPTER
└── NÃO → CREATE MOD
↓
MOD CONTRACT
↓
TESTES
↓
REGISTRO
↓
RADAR
```

---

## 10. Não duplicação

Antes de implementar qualquer nova capability:

1. auditar os repositórios da PUB;
2. localizar implementação existente;
3. identificar owner canônico;
4. verificar se a capability já existe sob outro nome;
5. preferir adapter quando já existir;
6. somente criar novo mod quando houver gap real.

Nunca criar:

- segundo lead scorer;
- segundo intent engine;
- segundo research engine;
- segundo CRM;
- segundo catálogo comercial;
- segunda memória institucional;
- segundo sistema de oportunidade;
- segunda camada de execução full-stack sem justificativa.

---

## 11. Capability Map

Antes de grandes implementações do RADAR, manter um mapa de capabilities da Holding:

```
EXISTS
├── CAPABILITY
├── SERVICE
├── PRODUCT
├── ENGINE
├── MOD CANDIDATE
└── INFRASTRUCTURE

DUPLICATE
├── overlap
├── owner
└── canonical source

MISSING
├── capability
├── priority
└── reason to build

UNKNOWN
└── needs audit
```

Nenhuma capability deve ser declarada como existente sem evidência no código, contexto, documentação ou execução.

---

## 12. RADAR Core futuro

O Core deve concentrar apenas responsabilidades de orquestração.

```
radar/core/
├── orchestrator/
├── planner/
├── router/
├── capability_registry/
├── mod_registry/
├── state/
├── events/
├── policies/
├── execution_manager/
├── evidence/
└── contracts/
```

### Responsabilidades

**Orchestrator**
- coordena o fluxo global.

**Planner**
- transforma objetivo em plano executável.

**Router**
- resolve capability → provider/mod.

**Capability Registry**
- registra capacidades disponíveis.

**Mod Registry**
- registra módulos e versões.

**State**
- mantém estado do workflow.

**Events**
- comunicação/event sourcing entre componentes.

**Policies**
- permissões, custos, limites, evidência e regras.

**Execution Manager**
- envia trabalho ao runtime disponível.

**Evidence Manager**
- garante evidência verificável dos resultados.

---

## 13. SDK futuro

O ecossistema deve ter contratos estáveis para:

- Mod SDK;
- Agent SDK;
- Tool SDK;
- Workflow SDK;
- Event SDK.

A implementação interna dos projetos pode evoluir sem quebrar o contrato de capability.

---

## 14. Fluxo operacional-alvo

```
USER
 ↓
RADAR
 ↓
PLAN
 ↓
RESOLVE CAPABILITIES
 ↓
SELECT MODS
 ↓
PDL
 ↓
AGENTS
 ↓
TOOLS
 ↓
EVIDENCE
 ↓
RADAR
 ↓
DECISION
 ↓
ACTION
 ↓
RESULT
 ↓
FEEDBACK / LEARNING
```

Quando Hermes ainda for necessário:

```
RADAR
 ↓
PDL
 ↓
HERMES
 ↓
AGENTS / TOOLS
 ↓
EVIDENCE
 ↓
RADAR
```

Essa dependência é transitória.

---

## 15. O que RADAR NÃO é

RADAR não é:

- apenas um scraper;
- apenas um CRM;
- apenas um lead scorer;
- apenas um research engine;
- apenas um catálogo comercial;
- apenas um agente;
- apenas um LLM wrapper;
- um substituto de todos os sistemas especializados;
- um produto baseado em Hermes.

RADAR é a **camada de orquestração e inteligência operacional que compõe esses sistemas**.

---

## 16. Roadmap estratégico revisado

### Fase 0 — Audit & Canonical Map

- auditoria ampla dos repositórios PUB;
- Capability Map;
- identificação de owners canônicos;
- identificação de duplicações;
- identificação de gaps;
- classificação EXISTS / DUPLICATE / MISSING / UNKNOWN.

### Fase 1 — RADAR Core

- Orchestrator;
- Planner;
- Router;
- Capability Registry;
- Mod Registry;
- State;
- Events;
- Policies;
- Contracts;
- Evidence Manager.

### Fase 2 — Mod / Adapter Layer

Integrar capabilities existentes através de adapters/mods:

- PUB Leads;
- PUB Research;
- PUB Machine;
- PUB Neural;
- PUB WAR;
- browser;
- GitHub;
- web;
- SEO;
- analytics;
- scraping;
- outros conforme necessidade real.

### Fase 3 — Opportunity Intelligence

Consolidar no RADAR:

```
signals
→ evidence
→ problems
→ hypotheses
→ capability resolution
→ capability fit
→ commercial fit
→ opportunity score
→ explanation
→ next action
```

### Fase 4 — PDL Integration

RADAR passa a delegar execução para o PDL através de contrato estável.

### Fase 5 — Autonomous Operations

- workflows contínuos;
- multi-agent execution;
- evidence-first execution;
- recovery;
- feedback;
- learning.

### Fase 6 — Hermes Decommission

Quando o PDL possuir capacidade suficiente:

```
RADAR → PDL → AGENTS → TOOLS
```

Hermes deixa de ser dependência operacional.

### Fase 7 — Ecosystem / Open Source

Extrair módulos reutilizáveis para outros projetos sem acoplar esses projetos ao RADAR.

---

## 17. Dogfooding da PUB Holding

A PUB Holding é o primeiro ambiente real de uso do RADAR.

Isso significa:

> **O RADAR deve resolver primeiro problemas reais da PUB, mas sua arquitetura não deve ser limitada às estruturas internas da PUB.**

A Holding fornece:

- casos reais;
- sistemas existentes;
- dados;
- feedback;
- métricas;
- evidências;
- necessidade comercial.

O RADAR transforma isso em uma arquitetura modular reutilizável.

---

## 18. Regras de engenharia

### Evidence First

Nenhuma integração ou capability deve ser considerada concluída sem evidência verificável.

### Zero Fake Work

Não declarar implementação, integração, teste ou execução que não tenha ocorrido.

### Fail Closed

Quando uma capability, provider ou estado não puder ser comprovado, marcar como UNKNOWN ou falhar explicitamente.

### Canonical Ownership

Cada capability importante deve ter um owner canônico.

### Adapter Before Rewrite

Se já existe implementação funcional, criar adapter antes de reimplementar.

### Contracts Before Coupling

O RADAR deve depender de contratos/capabilities, não de detalhes internos dos sistemas.

### Preserve Existing Systems

Não apagar ou absorver projetos existentes sem necessidade. Preferir integração, ownership, adapter ou depreciação explícita.

### Evidence + Tests + Commit

Mudanças relevantes devem terminar com:

```
IMPLEMENT
→ TEST
→ VERIFY
→ EVIDENCE
→ COMMIT
```

---

## 19. Decisão arquitetural consolidada

A direção estratégica atual é:

> **PUB RADAR será o sistema de orquestração operacional da PUB Holding.**
>
> **Os demais projetos continuam donos de suas capabilities.**
>
> **O RADAR resolve e compõe essas capabilities através de contratos e mods/adapters.**
>
> **O PDL é o Harness estratégico de execução.**
>
> **Hermes é apenas uma camada transitória utilizada enquanto o PDL não possui toda a capacidade necessária.**
>
> **O objetivo final é eliminar a dependência operacional do Hermes sem transformar o RADAR em um clone de nenhum dos sistemas existentes.**

---

## 20. Regra para futuras decisões

Antes de criar qualquer novo componente no RADAR, responder:

1. Isso é uma responsabilidade de orquestração?
2. Já existe essa capability em algum projeto PUB?
3. Quem é o owner canônico?
4. Precisamos de um adapter ou de um novo mod?
5. Isso pertence ao Opportunity Intelligence do RADAR?
6. Isso pertence ao runtime do PDL?
7. Isso é apenas uma dependência transitória do Hermes?
8. Existe evidência suficiente para afirmar que a capability existe?
9. O contrato pode ser reutilizado por outro projeto?
10. Estamos criando algo novo porque existe necessidade real ou apenas duplicando arquitetura?

Se a resposta indicar que outro sistema já é dono da responsabilidade, **não recriar no RADAR**.

---

## Status

**Arquitetura estratégica:** CONSOLIDADA  
**RADAR como orquestrador:** DECIDIDO  
**Capability Map:** PRÓXIMA ETAPA  
**PDL como Harness estratégico:** DECIDIDO  
**Hermes como runtime transitório:** DECIDIDO  
**Modularização:** DIREÇÃO ESTRATÉGICA  
**Auditoria completa da Holding:** PENDENTE  
**RADAR Core 3.0:** PENDENTE DA AUDITORIA
