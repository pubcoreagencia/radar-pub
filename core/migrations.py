"""RADAR PUB — migrations: versão 1 → 2.

Cria tabelas adicionais: opportunities_explicacao, opportunities_motivos, opportunities_proxima_acao.
"""
from __future__ import annotations

from core.persistence import Database


def migrate_v1_to_v2(db_path: str = "radar.db") -> None:
    """Executa migração do schema v1 para v2.

    Neste MVP, as tabelas principais já suportam os campos:
    - opportunities: prioridade, hipotese, motivo, proxima_acao, criado_em
    - scores: dimensoes, pesos, score_geral
    - analysis: strengths, weaknesses, opportunities, hypotheses, criado_em

    Esta migration é um placeholder para futuras versões (ex.: adicionar índices, constraints).
    """
    # No MVP atual, o schema já suporta os campos necessários.
    # Executa SELECT dummy para garantir que o banco existe.
    db = Database(db_path)
    cur = db.conn.cursor()
    cur.execute("SELECT COUNT(*) FROM opportunities")
    count = cur.fetchone()[0]
    # Nada para migrar — apenas um stub para fronteiras futuras.
    db.close()