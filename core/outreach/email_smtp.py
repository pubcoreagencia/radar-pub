"""Radicionário de Email — versão suportada pelo stdlib.

SMTP via padrão de contexto gerenciado (Python 3.11) se disponível,
 caso contrário, fallback para smtplib convencional.
Não persiste senhas/tokens em disco.
"""
from __future__ import annotations

import smtplib
from email.message import EmailMessage
from typing import Any, Callable

from .channels import EmailChannel


def send_email_via_smtp(
    host: str,
    port: int,
    username: str,
    password: str,
    from_addr: str,
    to_addrs: str,
    subject: str,
    body: str,
) -> dict[str, Any]:
    """Envio de email via SMTP simples (sem TLS forte para simplicidade)."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addrs
    msg.set_content(body)
    try:
        with smtplib.SMTP(host, port, timeout=10) as server:
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
        return {"success": True, "message": f"Email enviado para {to_addrs}"}
    except Exception as e:
        return {"success": False, "error": f"smtp_error: {e}"}


class EmailChannelSMTP(EmailChannel):
    """Implementação de EmailChannel usando SMTP."""

    def __init__(
        self,
        smtp_host: str | None = None,
        smtp_port: int = 587,
        username: str | None = None,
        password: str | None = None,
        from_addr: str | None = None,
        send_func: Callable[..., dict[str, Any]] | None = None,
    ) -> None:
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_addr = from_addr
        self.send_func = send_func or send_email_via_smtp

    def is_configured(self) -> bool:
        return bool(self.smtp_host and self.username and self.password and self.from_addr)

    def send(self, lead_id: str, message: str) -> dict[str, Any]:
        if not self.is_configured():
            return {"success": False, "error": "email_not_configured", "channel": "email"}
        return self.send_func(
            host=self.smtp_host,
            port=self.smtp_port,
            username=self.username,
            password=self.password,
            from_addr=self.from_addr,
            to_addrs="contato@exemplo.com",  # placeholder — futuro: extrair do lead
            subject=f"Oportunidade do RADAR PUB — lead {lead_id}",
            body=message,
        )