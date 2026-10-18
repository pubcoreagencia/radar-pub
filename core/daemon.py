"""RADAR PUB — daemon 24/7.

Fase 4: loops contínuos com scheduler, graceful shutdown, persistência.
Fase futura: integração com Hermes/PDL como orquestrador externo.
"""
from __future__ import annotations

import signal
import time
import json
from datetime import datetime

from core.entities import LeadStatus
from core.pipeline import Pipeline
from core.persistence import Database
from core.logging import log_event


class RadarDaemon:
    """Daemon contínuo do Radar PUB.

    Executa loops:
      - Discovery Loop: descobre novos leads periodicamente
      - Research Loop: pesquisa leads descobertos
      - Qualification Loop: qualifica e pontua
      - Opportunity Loop: gera oportunidades
      - Learning Loop: registra decisões (preparado p/ feedback futuro)
    """

    def __init__(
        self,
        db_path: str = "radar.db",
        discovery_interval: int = 300,   # 5 min
        research_interval: int = 180,    # 3 min
        qualification_interval: int = 120,  # 2 min
    ) -> None:
        self.db = Database(db_path)
        self.pipeline = Pipeline()
        self.discovery_interval = discovery_interval
        self.research_interval = research_interval
        self.qualification_interval = qualification_interval
        self._running = False
        self._last_discovery = 0.0
        self._last_research = 0.0
        self._last_qualification = 0.0

    def start(self) -> None:
        """Inicia o daemon 24/7."""
        self._running = True
        log_event("daemon_started", discovery_interval=self.discovery_interval,
                  research_interval=self.research_interval,
                  qualification_interval=self.qualification_interval)

        # Registra handlers de shutdown
        signal.signal(signal.SIGINT, self._handle_shutdown)
        signal.signal(signal.SIGTERM, self._handle_shutdown)

        log_event("daemon_running")
        while self._running:
            now = time.time()
            try:
                if now - self._last_discovery >= self.discovery_interval:
                    self._discovery_loop()
                    self._last_discovery = now
                if now - self._last_research >= self.research_interval:
                    self._research_loop()
                    self._last_research = now
                if now - self._last_qualification >= self.qualification_interval:
                    self._qualification_loop()
                    self._last_qualification = now
            except Exception as e:
                log_event("daemon_loop_error", error=str(e))
            time.sleep(1)

    def stop(self) -> None:
        """Para o daemon graciosamente."""
        self._running = False
        log_event("daemon_stopped")
        self.db.close()

    def _handle_shutdown(self, signum, frame) -> None:
        log_event("daemon_shutdown_signal", signal=signum)
        self.stop()

    def _discovery_loop(self) -> None:
        log_event("discovery_loop_started")
        leads = self.pipeline.run()
        for r in leads:
            self.db.save_lead(r["lead"])
        log_event("discovery_loop_completed", leads_processed=len(leads))

    def _research_loop(self) -> None:
        log_event("research_loop_started")
        leads = self.db.get_leads()
        for lead_row in leads:
            try:
                from core.entities import Lead
                lead = Lead(
                    lead_id=lead_row["lead_id"],
                    empresa=lead_row["empresa"],
                    segmento=lead_row["segmento"],
                    localizacao=lead_row["localizacao"],
                    website=lead_row["website"],
                    redes_sociais=json.loads(lead_row["redes_sociais"]) if lead_row["redes_sociais"] else [],
                    fonte=lead_row["fonte"],
                    status=LeadStatus(lead_row["status"]),
                    criado_em=lead_row["criado_em"],
                )
                from core.research.engine import research_lead
                research = research_lead(lead)
                self.db.save_research(research)
            except Exception as e:
                log_event("research_loop_error", lead_id=lead_row.get("lead_id"), error=str(e))
        log_event("research_loop_completed", leads_researched=len(leads))

    def _qualification_loop(self) -> None:
        log_event("qualification_loop_started")
        leads = self.db.get_leads()
        for lead_row in leads:
            try:
                from core.entities import Lead, Score, Opportunity
                from core.research.engine import research_lead
                from core.analysis.engine import analyze
                from core.qualification.engine import qualify
                lead = Lead(
                    lead_id=lead_row["lead_id"],
                    empresa=lead_row["empresa"],
                    segmento=lead_row["segmento"],
                    localizacao=lead_row["localizacao"],
                    website=lead_row["website"],
                    redes_sociais=json.loads(lead_row["redes_sociais"]) if lead_row["redes_sociais"] else [],
                    fonte=lead_row["fonte"],
                    status=LeadStatus(lead_row["status"]),
                    criado_em=lead_row["criado_em"],
                )
                research = research_lead(lead)
                analysis = analyze(lead, research)
                opp = qualify(lead, research, analysis)
                self.db.save_analysis(analysis)
                self.db.save_opportunity(opp)
            except Exception as e:
                log_event("qualification_loop_error", lead_id=lead_row.get("lead_id"), error=str(e))
        log_event("qualification_loop_completed", leads_qualified=len(leads))