"""Catálogo de capacidades da PUB Holding.

Derivado DA AUDITORIA evidence-first (arquivo de delegação Agent A):
13 capacidades ativas listadas, das quais 12 são IMPLEMENTED/PARTIAL
(SAGAZ FARM OS é UNKNOWN e vai para CATALOG_EXCLUDED).

Contratos:
  - get_catalog() -> list[Capability]
  - get_capability(id) -> Capability | None
  - CATALOG_EXCLUDED: lista de tuplas (id_ou_nome, motivo)
  - evidence NUNCA vazio (testes exigem len(evidence) > 0)
  - internal_capability SEM commercial_models
  - implemented -> confidence 0.9; partial -> confidence 0.6
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .domains import Domain


# ---------------------------------------------------------------------------
# Tipo de capacidade
# ---------------------------------------------------------------------------

class CapabilityType(str, Enum):
    """Tipos válidos de capacidade (contrato de test_capability_types)."""
    PRODUCT = "product"
    SERVICE = "service"
    PLATFORM = "platform"
    VERTICAL = "vertical"
    INFRASTRUCTURE = "infrastructure"
    INTERNAL_CAPABILITY = "internal_capability"


# ---------------------------------------------------------------------------
# Capability
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Capability:
    """Capacidade real da PUB Holding, derivada de evidência de auditoria."""
    id: str
    name: str
    domain: str  # value do Domain enum
    description: str
    status: str  # implemented | partial (ativas)
    type: str  # CapabilityType value
    evidence: list[str]  # NUNCA vazio
    problems_solved: list[str]
    opportunity_signals: list[str]
    commercial_models: list[str]
    dependencies: list[str]
    confidence: float
    source_repository: str
    source_document: str


# ---------------------------------------------------------------------------
# Capacidades ativas (IMPLEMENTED/PARTIAL) — extraídas da auditoria
# ---------------------------------------------------------------------------

_CAPABILITIES: list[Capability] = [
    Capability(
        id="pdl",
        name="PUB DEV LOOP (PDL)",
        domain=Domain.AUTONOMIA.value,
        description=(
            "Execução autônoma de código com governança: PostgreSQL Task Queue, "
            "Worker daemon, Continuous Scheduler (bounded/serial), Execution "
            "Governance (fail-closed), Kill Switch (3 fontes), Retry/DLQ/Reaper, "
            "Repository Identity fail-closed, Workspace Isolation, Task Finalizer "
            "e Remote Delivery Gate (PR → CI → merge)."
        ),
        status="implemented",
        type=CapabilityType.PLATFORM.value,
        evidence=[
            "PUB DEV LOOP/MASTER_CONTEXT.md (814 linhas)",
            "src/pdl/governance/",
            "src/pdl/scheduler/",
            "src/pdl/retry/",
            "src/pdl/reaper/",
            "src/pdl/delivery/product-delivery-service.ts",
        ],
        problems_solved=[
            "autonomous_code_execution_with_governance",
            "kill_switch_3_sources",
            "continuous_delivery_with_remote_gate",
        ],
        opportunity_signals=[
            "governed_autonomous_execution",
            "delivery_automation",
        ],
        commercial_models=["platform internal"],
        dependencies=["postgresql"],
        confidence=0.9,
        source_repository="PUB DEV LOOP",
        source_document="PUB DEV LOOP/MASTER_CONTEXT.md",
    ),
    Capability(
        id="prototype",
        name="PUB PROTOTYPE (PP)",
        domain=Domain.PROTOTYPING.value,
        description=(
            "Runtime próprio de prototipação (API + Worker + PostgreSQL) com "
            "VerificationGate V0–V5, VerificationRecoveryOrchestrator, "
            "Checkpoints SHA-bound, promoção idempotente por promotionId, "
            "Preview runtime e Dual Gateway (OpenRouter + 9Router Cloud)."
        ),
        status="implemented",
        type=CapabilityType.PLATFORM.value,
        evidence=[
            "PUB PROTOTYPE/MASTER_CONTEXT.md (466 linhas)",
            "src/pp/api/entry.ts",
            "src/pp/worker/entry.ts",
            "src/pp/verification/verification-gate.ts",
        ],
        problems_solved=[
            "rapid_prototyping_with_verification_gate",
            "idempotent_promotion_to_pdl",
            "dual_gateway_free_model_access",
        ],
        opportunity_signals=[
            "prototype_to_production_pipeline",
            "preview_runtime_comparison",
        ],
        commercial_models=["platform internal"],
        dependencies=["postgresql", "9router"],
        confidence=0.9,
        source_repository="PUB PROTOTYPE",
        source_document="PUB PROTOTYPE/MASTER_CONTEXT.md",
    ),
    Capability(
        id="neural",
        name="PUB NEURAL",
        domain=Domain.MEMORIA_CONHECIMENTO.value,
        description=(
            "Memória/conhecimento operacional: PostgreSQL 16+ pgvector/pgcrypto, "
            "event store append-only, Knowledge Graph, HybridSearch (FTS + pgvector "
            "RRF + abstention), GraphSearch bounded, Neural Knowledge Gate (CQRS), "
            "ingestão (BlobVault, ScoutWorker, SourceIngestor) e console React 19."
        ),
        status="implemented",
        type=CapabilityType.INFRASTRUCTURE.value,
        evidence=[
            "PUB NEURAL/MASTER_CONTEXT.md",
            "PUBNEURALRESEARCHMASTERCONTEXT.md",
            "src/gate/",
            "src/retrieval/",
            "src/ingestion/",
            "src/invalidation/",
            "runtime/backend/",
            "console/frontend/",
        ],
        problems_solved=[
            "operational_knowledge_memory",
            "hybrid_search_with_abstention",
            "provenance_tracked_knowledge_graph",
        ],
        opportunity_signals=[
            "knowledge_retrieval_service",
            "experience_gates_for_agents",
        ],
        commercial_models=["infrastructure internal"],
        dependencies=["postgresql 16+ pgvector"],
        confidence=0.9,
        source_repository="PUB NEURAL",
        source_document="PUB NEURAL/MASTER_CONTEXT.md",
    ),
    Capability(
        id="9router",
        name="9ROUTER",
        domain=Domain.ROUTING_LLM.value,
        description=(
            "Gateway de roteamento LLM OpenAI-compatible (/v1/chat/completions) "
            "com provider-key vault, SQLite WAL, usage tracking token-level, "
            "failover dual-gateway e deploy Cloudflare Containers."
        ),
        status="implemented",
        type=CapabilityType.INFRASTRUCTURE.value,
        evidence=[
            "pub-9router-cloud/9ROUTER_MASTER_CONTEXT.md (380 linhas)",
            "pub-9router-cloud/docs/MASTER_CONTEXT.md (340 linhas)",
            "Dockerfile",
            "restore-db.js",
            "entrypoint-wrapper.sh",
            ".github/workflows/deploy-cloudflare.yml",
        ],
        problems_solved=[
            "llm_inference_routing",
            "provider_key_vault",
            "token_level_usage_tracking",
        ],
        opportunity_signals=[
            "managed_llm_gateway",
            "multi_provider_failover",
        ],
        commercial_models=["gateway saas"],
        dependencies=["cloudflare containers"],
        confidence=0.9,
        source_repository="pub-9router-cloud",
        source_document="pub-9router-cloud/9ROUTER_MASTER_CONTEXT.md",
    ),
    Capability(
        id="pub-leads",
        name="PUB LEADS (LeadCore)",
        domain=Domain.CRM_PROSPECCAO.value,
        description=(
            "SaaS CRM B2B de prospecção: Next.js 15 + Supabase + Turso, pipeline "
            "3 camadas (Apify Google Maps → enriquecimento web → qualificação), "
            "Evolution API/WhatsApp Native com derriço anti-bloqueio e planos "
            "via webhook Stripe/Asaas."
        ),
        status="implemented",
        type=CapabilityType.SERVICE.value,
        evidence=[
            "pub-leads/MASTER_CONTEXT.md (133 linhas)",
            "src/lib/lead-sources/enrichment-pipeline.ts",
            "src/lib/whatsapp/evolution-client.ts",
            "app/api/",
        ],
        problems_solved=[
            "sem_crm_estruturado",
            "sem_canal_comercial_digital",
        ],
        opportunity_signals=[
            "b2b_lead_scout",
            "multi_channel_outreach",
        ],
        commercial_models=["saas crm b2b"],
        dependencies=["supabase", "turso", "apify"],
        confidence=0.9,
        source_repository="pub-leads",
        source_document="pub-leads/MASTER_CONTEXT.md",
    ),
    Capability(
        id="pub-machine",
        name="PUB MACHINE",
        domain=Domain.INTELIGENCIA_COMERCIAL.value,
        description=(
            "Inteligência comercial vertical: Signal/Capture (GPS, BLE, Wi-Fi, "
            "Haversine, Ray-Casting), Audience Intelligence (perfis pseudonimizados, "
            "SegmentaçãoEngine, IntentBridge), Physical → Lead Intent, Lead & "
            "Conversion Intelligence e Execution Intelligence (V0)."
        ),
        status="partial",
        type=CapabilityType.VERTICAL.value,
        evidence=[
            "PUB MACHINE/MASTER_CONTEXT.md (89 linhas)",
            "src/signal/",
            "src/audience/",
            "src/prospecting/",
            "src/autonomous/",
            "commit b8c97d8 (E2E vertical slice validado)",
        ],
        problems_solved=[
            "sem_scoring_comercial",
        ],
        opportunity_signals=[
            "physical_to_lead_intent",
            "deal_probability_forecasting",
        ],
        commercial_models=["vertical saas"],
        dependencies=[],
        confidence=0.6,
        source_repository="PUB MACHINE",
        source_document="PUB MACHINE/MASTER_CONTEXT.md",
    ),
    Capability(
        id="pub-acp",
        name="PUB-ACP",
        domain=Domain.TRANSPORTE_ORQUESTRACAO.value,
        description=(
            "Transporte/orquestração ACP entre orquestrador e agentes: GPT "
            "Self-Agent Mode, Browser Input Dispatcher (porta 5055) e Injector "
            "(CDP 9555), Local Capabilities, Session Persistence e "
            "ClosedLoopEngine (zero copy/paste)."
        ),
        status="implemented",
        type=CapabilityType.INFRASTRUCTURE.value,
        evidence=[
            "pub-acp-lab/MASTER_CONTEXT.md (589 linhas)",
            "pub-acp-standalone/MASTER_CONTEXT.md",
            "PUB-ACP-POC/README.md",
            "src/transport/",
            "src/bridge/",
            "src/cli/",
            "scripts/run-gpt-executor-proof.ts",
        ],
        problems_solved=[
            "agent_client_protocol_transport",
            "browser_input_injection",
            "session_persistence_and_recovery",
        ],
        opportunity_signals=[
            "cross_orchestrator_agent_bridge",
            "self_agent_closed_loop",
        ],
        commercial_models=["infrastructure internal"],
        dependencies=["node.js", "chrome devtools protocol"],
        confidence=0.9,
        source_repository="pub-acp-lab",
        source_document="pub-acp-lab/MASTER_CONTEXT.md",
    ),
    Capability(
        id="pub-ecom",
        name="PUB ECOM",
        domain=Domain.ECOMMERCE.value,
        description=(
            "Plataforma e-commerce: Node.js HTTP API + PostgreSQL (transaction "
            "boundaries, inventory reservation), migrations 00001–00015, checkout "
            "com expiração, secure RPC, strict RLS, Catalog Worker, Shopee "
            "Scraper e frontend TanStack Start/React 19 em Cloudflare Workers."
        ),
        status="implemented",
        type=CapabilityType.PRODUCT.value,
        evidence=[
            "pub-ecom/pub-ecom-real/README.md",
            "pdl_credentials_quarantine_20261010/projects/pub-ecom/MASTER_CONTEXT.md",
        ],
        problems_solved=[
            "sem_presenca_ecommerce",
        ],
        opportunity_signals=[
            "shopee_ingestion_engine",
            "marketplace_scaffold",
        ],
        commercial_models=["plataforma e-commerce"],
        dependencies=["postgresql", "supabase", "cloudflare workers"],
        confidence=0.9,
        source_repository="pub-ecom",
        source_document="pub-ecom/pub-ecom-real/README.md",
    ),
    Capability(
        id="feira-virtual",
        name="FEIRA VIRTUAL",
        domain=Domain.MARKETPLACE_REGIONAL.value,
        description=(
            "Marketplace regional (Região dos Lagos): Node.js 22 + Express, SPA "
            "HTML5, checkout multi-produtor, controle de estoque atômico, taxa 5% "
            "e entrega determinística, com CI/CD GitHub Actions e Dockerfile."
        ),
        status="implemented",
        type=CapabilityType.PRODUCT.value,
        evidence=[
            "pub-feira-virtual/README.md (57 linhas)",
            "src/domain/",
            "src/api/",
            "tests/",
        ],
        problems_solved=[
            "sem_presenca_ecommerce",
        ],
        opportunity_signals=[
            "deterministic_local_delivery",
            "producer_fee_model",
        ],
        commercial_models=["marketplace regional", "taxa 5%"],
        dependencies=["node.js 22", "postgresql"],
        confidence=0.9,
        source_repository="pub-feira-virtual",
        source_document="pub-feira-virtual/README.md",
    ),
    Capability(
        id="radar-pub",
        name="RADAR PUB",
        domain=Domain.INTELIGENCIA.value,
        description=(
            "Business intelligence de oportunidades (MVP): pipeline Discovery → "
            "Research → Analysis → Scoring → Opportunity, persistência SQLite, "
            "daemon 24/7 com loops discovery/research/qualification, HTTP API e "
            "outreach (Instagram, WhatsApp, Email SMTP)."
        ),
        status="partial",
        type=CapabilityType.INFRASTRUCTURE.value,
        evidence=[
            "radar-pub/README.md (184 linhas)",
            "radar-pub/ROADMAP.md",
            "core/",
            "scripts/",
            "tests/",
        ],
        problems_solved=[
            "opportunity_discovery_scoring",
            "structured_lead_outreach",
            "autonomous_monitoring_daemon",
        ],
        opportunity_signals=[
            "real_data_source_integration",
            "learning_loop_autonomous_prospecting",
        ],
        commercial_models=["bi saas"],
        dependencies=["sqlite", "hermes", "pdl"],
        confidence=0.6,
        source_repository="radar-pub",
        source_document="radar-pub/README.md",
    ),
    Capability(
        id="agentes-pub",
        name="AGENTES PUB",
        domain=Domain.AUTONOMIA.value,
        description=(
            "Skills internas de autonomia: pdl-evidence-reality-checker, "
            "pdl-code-reviewer, pdl-minimal-change-engineer e "
            "pdl-software-architect."
        ),
        status="implemented",
        type=CapabilityType.INTERNAL_CAPABILITY.value,
        evidence=[
            "AGENTES PUB/.agents/skills/ (4 SKILL.md files)",
        ],
        problems_solved=[
            "evidence_reality_check",
            "code_review_assisted",
            "minimal_change_engineering",
            "software_architecture_review",
        ],
        opportunity_signals=["agent_skill_pack"],
        commercial_models=[],  # internal_capability SEM commercial_models
        dependencies=["pdl"],
        confidence=0.9,
        source_repository="AGENTES PUB",
        source_document="AGENTES PUB/.agents/skills/",
    ),
    Capability(
        id="pub-pulse-saas",
        name="PUB PULSE SAAS",
        domain=Domain.LANDING_PAGES.value,
        description=(
            "Landing pages SaaS (V0) em React 19 + Vite + Tailwind + aceternity "
            "+ lucide-react; build dist/ e evidências de design presentes "
            "(sem README/Master Context/testes)."
        ),
        status="partial",
        type=CapabilityType.PRODUCT.value,
        evidence=[
            "pub-pulse-saas/ (code only)",
            "pub-pulse-saas/dist/ (build exists)",
            "pub-pulse-saas/design/evidence/ (design screenshots)",
        ],
        problems_solved=["falta_de_website"],
        opportunity_signals=["landing_page_generation"],
        commercial_models=["serviço de landing page"],
        dependencies=[],
        confidence=0.6,
        source_repository="pub-pulse-saas",
        source_document="pub-pulse-saas/ (sem README/Master Context)",
    ),
]


# ---------------------------------------------------------------------------
# Capacidades descartadas (PLANNED/UNKNOWN/HISTORICAL sem código ativo)
# Extraído literalmente da tabela "CAPACIDADES DESCARTADAS" da auditoria.
# ---------------------------------------------------------------------------

CATALOG_EXCLUDED: list[tuple[str, str]] = [
    ("SAGAZ FARM OS", "README vazio (template Vite), sem código, sem docs"),
    ("PUB PULSE SAAS (doc-only)", "Apenas código React, sem README, sem Master Context, sem testes"),
    ("Campaign orchestration (PDL)", "BLOQUEADO / NÃO COMPLETO (explícito no MASTER_CONTEXT)"),
    ("Autonomia 24/7 irrestrita (PDL)", "NÃO ATIVA (explícito no MASTER_CONTEXT)"),
    ("Closed Loop Learner (PUB MACHINE)", "ARQUITETURA-ALVO / EMBRIONÁRIO"),
    ("Media Providers (9Router)", "NOT IMPLEMENTED IN REPO"),
    ("Headroom/Caveman/Ponytail (9Router)", "CONFIGURED but DISABLED"),
    ("Free Pool Scheduler (9Router)", "PLANNED (Fase B)"),
    ("SaaS multi-tenant (9Router)", "PLANNED (Fase C)"),
    ("Community Reports (PUB Neural)", "Schema only, no worker"),
    ("Leiden Worker (PUB Neural)", "FUTURE"),
    ("Production HTTP/MCP transport (PUB Neural)", "NOT IMPLEMENTED"),
    ("Autonomous Cognitive Loop (PUB Neural)", "NOT IMPLEMENTED"),
    ("Neural SaaS / Neural Cloud", "NOT IMPLEMENTED"),
    ("CNPJ público fallback (PUB Leads)", "PLANNED"),
    ("Validação ativa WhatsApp (PUB Leads)", "PLANNED"),
    ("Webhooks resposta WhatsApp (PUB Leads)", "PLANNED"),
    ("Paginação cursor Turso (PUB Leads)", "PLANNED"),
    ("Real Data Sources (Radar PUB)", "PLANNED (Fase 8)"),
    ("Learning Loop (Radar PUB)", "PLANNED (Fase 9)"),
    ("Autonomous Prospecting 24/7 (Radar PUB)", "PLANNED (Fase 10)"),
    ("MCP validation (ACP)", "NOT_RUN"),
    ("Browser Extension physical validation (ACP)", "PENDING"),
]


# ---------------------------------------------------------------------------
# API pública
# ---------------------------------------------------------------------------

ACTIVE_STATUSES = {"implemented", "partial"}


def get_catalog() -> list[Capability]:
    """Retorna capacidades ativas (IMPLEMENTED/PARTIAL) da auditoria."""
    return list(_CAPABILITIES)


def get_capability(cap_id: str) -> Capability | None:
    """Busca capability pelo id."""
    for cap in _CAPABILITIES:
        if cap.id == cap_id:
            return cap
    return None