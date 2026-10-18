"""PDL/Harness client — consumindo API do Radar PUB."""
from __future__ import annotations

import json
from typing import Any

from integrations.hermes.client import HermesClient


class PDLClient:
    """Cliente do PDL/Harness."""

    def __init__(self, base_url: str = "http://localhost:8081") -> None:
        self.base_url = base_url.rstrip("/")
        self._hermes = HermesClient(self.base_url.replace(":8081", ":8080"))

    def execute(self, task: str) -> dict[str, Any]:
        """Executa tarefa via PDL/Harness.

        Exemplo: {"task": "discover"} ou {"task": "find_opportunities", "prioridade": "ALTA"}
        """
        import urllib.request, urllib.error
        url = f"{self.base_url}/radar/execute"
        data = json.dumps({"task": task}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            from core.logging import log_event
            log_event("pdl_client_error", error=f"HTTP {e.code}: {e.reason}", url=url)
            return {"status": "error", "message": e.reason}
        except Exception as e:
            from core.logging import log_event
            log_event("pdl_client_error", error=str(e), url=url)
            return {"status": "error", "message": str(e)}