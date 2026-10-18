"""Radar API para Hermes e PDL.

Permite que o Hermes chame o Radar PUB como um serviço.
Permite que o PDL/Harness execute tarefas no Radar PUB.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from core.pipeline import Pipeline
from core.persistence import Database
from core.logging import log_event


class HermesClient:
    """Cliente do Hermes para API do Radar."""

    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip("/")

    def discover(self) -> list[dict]:
        import urllib.request
        url = f"{self.base_url}/radar/discover"
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                return json.loads(resp.read())
        except Exception as e:
            log_event("hermes_client_error", error=str(e), url=url)
            return []

    def find_opportunities(self, prioridade: str | None = None) -> list[dict]:
        base = f"{self.base_url}/radar/opportunities"
        url = f"{base}?prioridade={prioridade}" if prioridade else base
        import urllib.request
        try:
            with urllib.request.urlopen(url, timeout=10) as resp:
                return json.loads(resp.read())
        except Exception as e:
            log_event("hermes_client_error", error=str(e), url=url)
            return []


class PDLClient:
    """Cliente do PDL/Harness para API do Radar."""

    def __init__(self, base_url: str = "http://localhost:8081"):
        self.base_url = base_url.rstrip("/")

    def execute(self, task: str) -> dict[str, Any]:
        import urllib.request, urllib.error
        url = f"{self.base_url}/radar/execute"
        data = json.dumps({"task": task}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            log_event("pdl_client_error", error=f"HTTP {e.code}: {e.reason}", url=url)
            return {"status": "error", "message": e.reason}
        except Exception as e:
            log_event("pdl_client_error", error=str(e), url=url)
            return {"status": "error", "message": str(e)}