"""RADAR PUB — configuração de ambiente (.env).

Usado para injetar valores em runtime via environment variables.
Sempre use .env.example como referência; nunca commit .env.
"""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class EnvConfig:
    """Configuração lida de variáveis de ambiente."""

    # Database
    RADAR_DB_PATH: str = os.getenv("RADAR_DB_PATH", "radar.db")

    # Daemon intervals (seconds)
    RADAR_DISCOVERY_INTERVAL: int = int(os.getenv("RADAR_DISCOVERY_INTERVAL", "300"))
    RADAR_RESEARCH_INTERVAL: int = int(os.getenv("RADAR_RESEARCH_INTERVAL", "180"))
    RADAR_QUALIFICATION_INTERVAL: int = int(os.getenv("RADAR_QUALIFICATION_INTERVAL", "120"))

    # API
    RADAR_API_HOST: str = os.getenv("RADAR_API_HOST", "127.0.0.1")
    RADAR_API_PORT: int = int(os.getenv("RADAR_API_PORT", "8787"))

    # Hermes integration
    HERMES_URL: str = os.getenv("HERMES_URL", "http://localhost:8080")
    HERMES_TOKEN: str | None = os.getenv("HERMES_TOKEN")

    # PDL/Harness integration
    PDL_URL: str = os.getenv("PDL_URL", "http://localhost:8081")
    PDL_TOKEN: str | None = os.getenv("PDL_TOKEN")

    # Outreach
    INSTAGRAM_USERNAME: str | None = os.getenv("INSTAGRAM_USERNAME")
    INSTAGRAM_PASSWORD: str | None = os.getenv("INSTAGRAM_PASSWORD")
    WHATSAPP_PHONE: str | None = os.getenv("WHATSAPP_PHONE")
    WHATSAPP_API_TOKEN: str | None = os.getenv("WHATSAPP_API_TOKEN")
    SMTP_HOST: str | None = os.getenv("SMTP_HOST")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str | None = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASSWORD")
    SMTP_FROM: str | None = os.getenv("SMTP_FROM")


ENV = EnvConfig()


def get_env() -> EnvConfig:
    """Retorna a configuração de ambiente atual."""
    return ENV