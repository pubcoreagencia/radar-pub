# RADAR PUB - Roadmap

## Phase 1 — Foundation (Current/In Progress)

- [x] Project structure
- [x] Architecture definition
- [x] Domain model (Lead, Research, Score, Opportunity, DecisionRecord)
- [x] Core modules (discovery, research, qualification, scoring, opportunity, memory)
- [x] Config center (centralized weights, thresholds)
- [x] Logging structured
- [x] Discovery source abstraction (DiscoverySource interface)
- [x] Pipeline vertical: Discovery → Research → Analysis → Scoring → Opportunity
- [x] Mock fixtures for MVP
- [x] Tests (entities, scoring, pipeline, edge cases, config)
- [x] Documentation (README, ARCHITECTURE, ROADMAP, ADRs)
- [x] Package config (pyproject.toml)

## Phase 2 — Intelligence

- [ ] Scoring explainability report (dimension weight contributions)
- [ ] Analysis module extracted (strengths/weaknesses/opportunities)
- [ ] Hermes integration interface (integrations/hermes)
- [ ] PDL integration interface (integrations/pdl)
- [ ] Integration tests (pytest)
- [ ] CI workflow (GitHub Actions)

## Phase 3 — Real Discovery

- [ ] Persistence layer (SQLite/Turso)
- [ ] Async jobs queue (Redis)
- [ ] Real discovery sources (Google Maps, web scraping, social APIs)
- [ ] Browser automation (Scrapy/Playwright)

## Phase 4 — Continuous Execution

- [ ] 24/7 loops (discovery, research, qualification, outreach, followup, learning)
- [ ] Memory of decisions
- [ ] Feedback storage

## Phase 5 — Hermes Integration

- [ ] Radar ↔ Hermes API interface
- [ ] Hermes as external orchestrator

## Phase 6 — PDL/Harness Integration

- [ ] Radar ↘ integration interface ↙ PDL
- [ ] PDL as execution harness

## Phase 7 — Autonomous Prospecting

- [ ] Multi-agent execution
- [ ] Real outreach (outreach loop)
- [ ] Real follow-up (followup loop)

## Phase 8 — Learning Loop

- [ ] Feedback on commercial results
- [ ] Learning from conversion data
- [ ] Adaptive scoring