"""RADAR PUB — canais de outreach.

Fase 6: slots para Instagram, WhatsApp, email, etc.
Credenciais e login são configuração pessoal — não implementadas aqui.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


class OutreachChannel(ABC):
    """Canal de outreach abstrato."""

    @abstractmethod
    def send(self, lead_id: str, message: str) -> dict[str, Any]:
        """Envia mensagem para o lead."""
        ...

    @abstractmethod
    def is_configured(self) -> bool:
        """Verifica se o canal está configurado (credenciais presentes)."""
        ...


@dataclass
class OutreachResult:
    channel: str
    lead_id: str
    success: bool
    message: str
    error: str | None = None


class InstagramChannel(OutreachChannel):
    """Canal Instagram (DM).

    Fase 6: slot preparado. Login/credenciais = config pessoal.
    """

    def __init__(self, username: str | None = None, password: str | None = None) -> None:
        self.username = username
        self.password = password

    def is_configured(self) -> bool:
        return bool(self.username and self.password)

    def send(self, lead_id: str, message: str) -> dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "instagram_not_configured", "channel": "instagram"}
        # Fase futura: implementar envio real via API/browser automation
        return {"success": True, "channel": "instagram", "lead_id": lead_id, "message": message}


class WhatsAppChannel(OutreachChannel):
    """Canal WhatsApp (mensagem).

    Fase 6: slot preparado. Login/credenciais = config pessoal.
    """

    def __init__(self, phone_number: str | None = None, api_token: str | None = None) -> None:
        self.phone_number = phone_number
        self.api_token = api_token

    def is_configured(self) -> bool:
        return bool(self.phone_number and self.api_token)

    def send(self, lead_id: str, message: str) -> dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "whatsapp_not_configured", "channel": "whatsapp"}
        # Fase futura: implementar envio real via API (Twilio, EvolutionAPI, etc.)
        return {"success": True, "channel": "whatsapp", "lead_id": lead_id, "message": message}


class EmailChannel(OutreachChannel):
    """Canal email."""

    def __init__(self, smtp_host: str | None = None, smtp_port: int = 587, username: str | None = None, password: str | None = None) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def is_configured(self) -> bool:
        return bool(self.smtp_host and self.username and self.password)

    def send(self, lead_id: str, message: str) -> dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "email_not_configured", "channel": "email"}
        return {"success": True, "channel": "email", "lead_id": lead_id, "message": message}


class OutreachManager:
    """Gerenciador de canais de outreach."""

    def __init__(self) -> None:
        self.channels: dict[str, OutreachChannel] = {}

    def register(self, name: str, channel: OutreachChannel) -> None:
        self.channels[name] = channel

    def send(self, channel_name: str, lead_id: str, message: str) -> dict[str, Any]:
        channel = self.channels.get(channel_name)
        if not channel:
            return {"success": False, "error": f"channel_not_found: {channel_name}"}
        return channel.send(lead_id, message)

    def configured_channels(self) -> list[str]:
        return [name for name, ch in self.channels.items() if ch.is_configured()]