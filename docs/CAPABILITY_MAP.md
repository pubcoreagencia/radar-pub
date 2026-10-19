# PUB RADAR — Capability Map

> Canonical audit artifact for Phase 0 (Audit & Canonical Map).
> Evidence is based on the repositories accessible in the PUB GitHub organization at the time of this audit.
>
> **Rule:** RADAR composes capabilities; it does not reimplement canonical owners.

## 1. Executive classification

| Domain | Canonical owner | RADAR status | Decision |
|---|---|---|---|
| Lead acquisition / enrichment / CRM / outreach transport | PUB Leads | EXISTS elsewhere | Adapter |
| Research / evidence extraction / provenance | PUB Research | EXISTS elsewhere | Adapter |
| Lead scoring / intent / prioritization / forecasting | PUB Machine | EXISTS elsewhere | Adapter |
| Institutional memory / knowledge / provenance | PUB Neural | EXISTS elsewhere | Adapter |
| Commercial catalog / SKUs / ICP / offers | PUB WAR | EXISTS elsewhere | Adapter |
| Autonomous execution / agents / tools / workflows | PDL | EXISTS elsewhere | Runtime contract |
| Opportunity Intelligence | RADAR | RADAR-owned | Build/retain |
| Cross-system planning / routing / orchestration | RADAR | RADAR-owned | Build/retain |
| Evidence-backed decision / outcome feedback | RADAR | RADAR-owned | Build/retain |
| Hermes full-stack execution | Hermes | TRANSITIONAL | Do not deepen coupling |

## 2. Canonical evidence

### PUB Leads

Repository: `pubcoreagencia/pub-leads`

Observed capabilities include:

- lead acquisition from Google Maps / Places / CNPJ / Overpass / Apify;
- website enrichment;
- Instagram / Google qualification;
- lead persistence and lifecycle;
- pipeline / funnel state;
- bulk import;
- WhatsApp instances, queues, native sending and message funnels;
- lead notes and message events.

**Ownership conclusion:** PUB Leads is the canonical lead-centric system.

**RADAR action:** expose these capabilities through contracts/adapters; do not create a second CRM, lead acquisition engine or outreach transport.

### PUB Research

Repository: `pubcoreagencia/pub-research`

Observed repository structure is explicitly organized as research intelligence and includes research records for:

- PUB Machine;
- PUB Neural;
- PUB Dev Loop;
- scraping;
- AI/browser systems;
- infrastructure and ecosystem components.

**Ownership conclusion:** PUB Research remains the canonical research/intelligence-source layer.

**RADAR action:** consume research/evidence/provenance capabilities rather than maintaining a parallel research engine.

### PUB Machine

Repository: `pubcoreagencia/pub-machine`

Observed implementation includes:

- `lead-scoring.service.ts`;
- `lead-intent-signals.service.ts`;
- `lead-prioritization-orchestrator.service.ts`;
- `lead-conversion-velocity.service.ts`;
- `deal-probability-forecasting.service.ts`;
- `predictive-deal-velocity.service.ts`;
- audience intelligence;
- segmentation;
- decision/action dispatch.

**Ownership conclusion:** PUB Machine owns Lead Score / Intent / prioritization and related commercial prediction.

**RADAR action:** consume Machine outputs. Do not create a competing Lead Score engine.

### PUB Neural

Repository: `pubcoreagencia/pub-neural`

Observed implementation includes:

- ingestion;
- document capture/parsing;
- GitHub synchronization;
- entity/relation extraction;
- evidence capture;
- provenance;
- hybrid retrieval;
- vector indexing;
- evidence abstention;
- semantic validation;
- knowledge/organizational architecture.

**Ownership conclusion:** PUB Neural is the canonical institutional knowledge/memory layer.

**RADAR action:** consume Neural knowledge and evidence capabilities. RADAR may maintain workflow state and decision context, but must not become a second institutional memory system.

### PUB WAR

Repository: `pubcoreagencia/pub-war`

Observed governance/market structure includes:

- master SKU catalog;
- portfolio;
- ICPs and channels;
- demand mapping;
- offer matrix;
- commercial microprocesses;
- brands and commercial variants;
- sales / evidence / playbooks.

**Ownership conclusion:** PUB WAR owns commercial knowledge, catalog, offers and SKU-level commercial composition.

**RADAR action:** resolve commercial fit against WAR capabilities/offers; do not create a second commercial catalog.

### PDL

Repository: `pubcoreagencia/pub-dev-loop`

Observed PDL scope includes:

- autonomous execution;
- worker/execution events;
- task lifecycle;
- retries / DLQ;
- governance;
- workforce state;
- repositories;
- organizational memory and learning;
- autonomous pipelines;
- execution specifications;
- agent continuity and handoff.

**Ownership conclusion:** PDL is the strategic execution Harness/runtime.

**RADAR action:** integrate through a stable execution contract. RADAR should not depend on PDL internals where a capability contract is sufficient.

### Hermes

Hermes is represented in RADAR under `integrations/hermes/` and in PDL historical/diagnostic material.

**Ownership conclusion:** Hermes is a transitional runtime dependency only.

**RADAR action:** preserve compatibility where operationally required, but do not deepen Hermes-specific architecture. The target is:

```
RADAR → PDL → AGENTS → TOOLS
```

with Hermes only as a temporary bridge:

```
RADAR → PDL → HERMES → AGENTS / TOOLS
```

## 3. RADAR-owned capability boundary

The RADAR should concentrate proprietary intelligence in:

```
OBJECTIVE
  ↓
PLAN
  ↓
CAPABILITY RESOLUTION
  ↓
EVIDENCE FUSION
  ↓
PROBLEM DETECTION
  ↓
PROBLEM HYPOTHESIS
  ↓
CAPABILITY FIT
  ↓
COMMERCIAL FIT
  ↓
OPPORTUNITY SCORE
  ↓
EXPLANATION
  ↓
NEXT ACTION
  ↓
OUTCOME
  ↓
LEARNING
```

### Lead Score vs Opportunity Score

```
PUB MACHINE
  └── Lead / Intent Score

RADAR
  └── Opportunity Score
```

These are complementary signals, not competing implementations.

## 4. Current RADAR implementation audit

The current RADAR codebase still contains an earlier vertical MVP:

```
Discovery → Research → Analysis → Scoring → Opportunity
```

The following areas require architectural migration rather than blind expansion:

- `core/discovery/` — overlap with PUB Leads acquisition;
- `core/research/` — overlap with PUB Research;
- `core/qualification/` and `core/scoring/` — overlap risk with PUB Machine;
- `core/memory/` — overlap risk with PUB Neural;
- `core/outreach/` — overlap with PUB Leads / channel execution;
- `integrations/pdl/` — must be checked for runtime-contract purity;
- `integrations/hermes/` — retain only as transitional compatibility.

The existing `core/opportunity/` is the strongest candidate for evolution into the RADAR-owned Opportunity Intelligence domain.

## 5. Required next architecture move

Do **not** jump directly to more agents, scraping or 24/7 loops.

First establish:

1. canonical capability contracts;
2. provider/mod registry;
3. capability resolution;
4. adapter boundaries;
5. Opportunity Intelligence boundary;
6. execution runtime contract;
7. evidence contract;
8. state/event contract.

Only after these are stable should RADAR Core 3.0 absorb additional automation.

## 6. Audit state

### EXISTS

- PUB Leads
- PUB Research
- PUB Machine
- PUB Neural
- PUB WAR
- PDL

### RADAR-OWNED

- orchestration;
- planning;
- capability resolution;
- opportunity intelligence;
- opportunity scoring;
- explainability;
- next-action selection;
- outcome feedback / learning coordination.

### TRANSITIONAL

- Hermes runtime integration.

### UNKNOWN / requires deeper source audit

- exact API contracts exposed by each canonical system;
- production endpoints and authentication contracts;
- capability versions and SLAs;
- runtime cost/latency measurements;
- cross-system event schemas;
- complete provider inventory across the entire Holding.

## 7. Rule

Before creating a capability in RADAR:

```
AUDIT
→ IDENTIFY OWNER
→ VERIFY EVIDENCE
→ ADAPTER IF EXISTS
→ CREATE ONLY IF GAP IS REAL
```

No capability is considered canonical merely because a similarly named module exists in RADAR.
