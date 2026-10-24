"""RADAR PUB — API facade.

Interface estável para Hermes e outros orquestradores consumirem.
Fase 5: implementação de API HTTP mínima (http.server stdlib).
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from core.pipeline import Pipeline
from core.persistence import Database
from core.logging import log_event


class RadarAPI:
    """Facade de alto nível do Radar PUB.

    Hermes (ou qualquer orquestrador) consome estes métodos.
    """

    def __init__(self, pipeline: Pipeline | None = None, db: Database | None = None) -> None:
        self.pipeline = pipeline or Pipeline()
        self.db = db

    def discover(self, source: str | None = None) -> list[dict]:
        """Executa discovery + pipeline completo para a fonte."""
        log_event("api_discover", source=source or "all")
        return self.pipeline.run(source)

    def research(self, lead_id: str) -> dict | None:
        """Retorna research de um lead persistido (se houver db)."""
        if not self.db:
            return None
        return self.db.get_lead(lead_id)

    def analyze(self, lead_id: str) -> dict | None:
        """Retorna análise de um lead persistido."""
        if not self.db:
            return None
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM analysis WHERE lead_id = ?", (lead_id,))
        row = cur.fetchone()
        if not row:
            return None
        return {
            "analysis_id": row["analysis_id"],
            "lead_id": row["lead_id"],
            "research_id": row["research_id"],
            "strengths": json.loads(row["strengths"]),
            "weaknesses": json.loads(row["weaknesses"]),
            "opportunities": json.loads(row["opportunities"]),
            "hypotheses": json.loads(row["hypotheses"]),
            "criado_em": row["criado_em"],
        }

    def score(self, lead_id: str) -> dict | None:
        """Retorna score de um lead persistido."""
        if not self.db:
            return None
        cur = self.db.conn.cursor()
        cur.execute("SELECT * FROM scores WHERE lead_id = ?", (lead_id,))
        row = cur.fetchone()
        if not row:
            return None
        return {
            "score_id": row["score_id"],
            "lead_id": row["lead_id"],
            "dimensoes": json.loads(row["dimensoes"]),
            "pesos": json.loads(row["pesos"]),
            "score_geral": row["score_geral"],
            "criado_em": row["criado_em"],
        }

    def find_opportunities(self, prioridade: str | None = None) -> list[dict]:
        """Retorna oportunidades, opcionalmente filtradas por prioridade."""
        log_event("api_find_opportunities", prioridade=prioridade or "all")
        if self.db:
            return self.db.get_opportunities(prioridade)
        # Fallback: executa pipeline e filtra
        results = self.pipeline.run()
        opps = [r["opportunity"] for r in results]
        if prioridade:
            opps = [o for o in opps if o["prioridade"] == prioridade]
        return opps

    def get_priority_leads(self, min_score: float = 0.7) -> list[dict]:
        """Retorna leads com score >= min_score."""
        results = self.pipeline.run()
        return [r for r in results if r["opportunity"]["score_geral"] >= min_score]


class RadarHandler(BaseHTTPRequestHandler):
    """Handler HTTP mínimo para a API do Radar."""

    api: RadarAPI | None = None

    def _send_json(self, data: dict | list, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_GET(self) -> None:
        if not self.api:
            self._send_json({"error": "API não inicializada"}, 500)
            return
        parsed = urlparse(self.path)
        path = parsed.path
        if path == "/health":
            self._send_json({"status": "ok"})
        elif path == "/discover":
            self._send_json(self.api.discover())
        elif path == "/opportunities":
            qs = parse_qs(parsed.query)
            prioridade = qs.get("prioridade", [None])[0]
            self._send_json(self.api.find_opportunities(prioridade))
        elif path == "/priority-leads":
            qs = parse_qs(parsed.query)
            min_score = float(qs.get("min_score", ["0.7"])[0])
            self._send_json(self.api.get_priority_leads(min_score))
        else:
            self._send_json({"error": "not found", "path": path}, 404)

    def log_message(self, format, *args):
        log_event("http_request", method=self.command, path=self.path)


def serve(host: str = "127.0.0.1", port: int = 8787, db_path: str | None = None) -> None:
    """Sobe o servidor HTTP da API do Radar."""
    db = Database(db_path) if db_path else None
    api = RadarAPI(db=db)
    RadarHandler.api = api
    server = HTTPServer((host, port), RadarHandler)
    log_event("api_started", host=host, port=port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        log_event("api_stopped")
        server.server_close()