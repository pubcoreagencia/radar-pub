"""RADAR PUB — logging estruturado.

Fornece logging consistente para observabilidade em execução 24/7.
Sem dependências externas.
"""
from __future__ import annotations

import logging
import sys
from typing import Any


def setup_logging(level: str = "INFO") -> logging.Logger:
    """Configura logging estruturado para o RADAR PUB."""
    logger = logging.getLogger("radar-pub")
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Evita duplicação de handlers.
    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


# Logger global.
_logger: logging.Logger | None = None


def get_logger() -> logging.Logger:
    """Retorna logger global, inicializando se necessário."""
    global _logger
    if _logger is None:
        _logger = setup_logging()
    return _logger


def log_event(event: str, **fields: Any) -> None:
    """Registra um evento estruturado."""
    logger = get_logger()
    extra = " ".join(f"{k}={v}" for k, v in fields.items())
    logger.info(f"{event} {extra}".strip())


def log_error(event: str, error: Exception, **fields: Any) -> None:
    """Registra um erro estruturado."""
    logger = get_logger()
    extra = " ".join(f"{k}={v}" for k, v in fields.items())
    logger.error(f"{event} error={type(error).__name__}: {error} {extra}".strip())