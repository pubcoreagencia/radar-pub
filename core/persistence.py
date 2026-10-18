"""RADAR PUB — persistência local (SQLite).

Fase 3: persistência simples de leads, opportunities e decisions.
Aceita dataclasses ou dicts (to_dict()).
Fase futura: Turso / Postgres.
Sem dependências externas — usa sqlite3 do stdlib.
"""
from __future__ import annotations

import json
import sqlite3
import os
from pathlib import Path
from typing import Any

from core.entities import Lead, Research, Analysis, Score, Opportunity, DecisionRecord


DB_PATH = Path(os.getenv("RADAR_DB_PATH", "radar.db"))


def _dict_factory(cursor, row):
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def _val(x: Any) -> Any:
    """Normaliza: Enum → .value, dict/list → json, resto → próprio valor."""
    if hasattr(x, "value"):
        return x.value
    return x


class Database:
    """Banco de dados SQLite para o Radar PUB."""

    def __init__(self, db_path: str | Path | None = None) -> None:
        self.db_path = Path(db_path) if db_path else DB_PATH
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = _dict_factory
        self._init_tables()

    def _init_tables(self) -> None:
        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS leads (
            lead_id TEXT PRIMARY KEY,
            empresa TEXT NOT NULL,
            segmento TEXT,
            localizacao TEXT,
            website TEXT,
            redes_sociais TEXT,
            fonte TEXT,
            status TEXT,
            criado_em TEXT
        );
        CREATE TABLE IF NOT EXISTS research (
            research_id TEXT PRIMARY KEY,
            lead_id TEXT NOT NULL,
            presenca_digital TEXT,
            sinais_encontrados TEXT,
            problemas_detectados TEXT,
            evidencias TEXT,
            observacoes TEXT,
            pesquisado_em TEXT
        );
        CREATE TABLE IF NOT EXISTS analysis (
            analysis_id TEXT PRIMARY KEY,
            lead_id TEXT NOT NULL,
            research_id TEXT NOT NULL,
            strengths TEXT,
            weaknesses TEXT,
            opportunities TEXT,
            hypotheses TEXT,
            criado_em TEXT
        );
        CREATE TABLE IF NOT EXISTS scores (
            score_id TEXT PRIMARY KEY,
            lead_id TEXT NOT NULL,
            dimensoes TEXT,
            pesos TEXT,
            score_geral REAL,
            criado_em TEXT
        );
        CREATE TABLE IF NOT EXISTS opportunities (
            opportunity_id TEXT PRIMARY KEY,
            lead_id TEXT NOT NULL,
            score_id TEXT NOT NULL,
            score_geral REAL,
            prioridade TEXT,
            hipotese TEXT,
            motivo TEXT,
            proxima_acao TEXT,
            criado_em TEXT
        );
        CREATE TABLE IF NOT EXISTS decisions (
            decision_id TEXT PRIMARY KEY,
            lead_id TEXT,
            decision_type TEXT,
            payload TEXT,
            criado_em TEXT
        );
        """)
        self.conn.commit()

    def save_lead(self, lead: Lead | dict) -> None:
        d = lead.to_dict() if hasattr(lead, "to_dict") else lead
        self.conn.execute("""
            INSERT OR REPLACE INTO leads (lead_id, empresa, segmento, localizacao, website, redes_sociais, fonte, status, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d["lead_id"], d["empresa"], d.get("segmento"), d.get("localizacao"),
            d.get("website"), json.dumps(d.get("redes_sociais", [])),
            d.get("fonte"), _val(d.get("status")), d.get("criado_em"),
        ))
        self.conn.commit()

    def save_research(self, research: Research | dict) -> None:
        d = research.to_dict() if hasattr(research, "to_dict") else research
        self.conn.execute("""
            INSERT OR REPLACE INTO research (research_id, lead_id, presenca_digital, sinais_encontrados, problemas_detectados, evidencias, observacoes, pesquisado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d["research_id"], d["lead_id"], _val(d.get("presenca_digital")),
            json.dumps(d.get("sinais_encontrados", [])),
            json.dumps(d.get("problemas_detectados", [])),
            json.dumps(d.get("evidencias", [])),
            json.dumps(d.get("observacoes", [])),
            d.get("pesquisado_em"),
        ))
        self.conn.commit()

    def save_analysis(self, analysis: Analysis | dict) -> None:
        d = analysis.to_dict() if hasattr(analysis, "to_dict") else analysis
        self.conn.execute("""
            INSERT OR REPLACE INTO analysis (analysis_id, lead_id, research_id, strengths, weaknesses, opportunities, hypotheses, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d["analysis_id"], d["lead_id"], d["research_id"],
            json.dumps(d.get("strengths", [])),
            json.dumps(d.get("weaknesses", [])),
            json.dumps(d.get("opportunities", [])),
            json.dumps(d.get("hypotheses", [])),
            d.get("criado_em"),
        ))
        self.conn.commit()

    def save_score(self, score: Score | dict) -> None:
        d = score.to_dict() if hasattr(score, "to_dict") else score
        self.conn.execute("""
            INSERT OR REPLACE INTO scores (score_id, lead_id, dimensoes, pesos, score_geral, criado_em)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            d["score_id"], d["lead_id"],
            json.dumps(d.get("dimensoes", {})),
            json.dumps(d.get("pesos", {})),
            d.get("score_geral"),
            d.get("criado_em"),
        ))
        self.conn.commit()

    def save_opportunity(self, opportunity: Opportunity | dict) -> None:
        d = opportunity.to_dict() if hasattr(opportunity, "to_dict") else opportunity
        self.conn.execute("""
            INSERT OR REPLACE INTO opportunities (opportunity_id, lead_id, score_id, score_geral, prioridade, hipotese, motivo, proxima_acao, criado_em)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d["opportunity_id"], d["lead_id"], d["score_id"],
            d.get("score_geral"), _val(d.get("prioridade")),
            d.get("hipotese"), d.get("motivo"),
            _val(d.get("proxima_acao")), d.get("criado_em"),
        ))
        self.conn.commit()

    def save_decision(self, decision: DecisionRecord | dict) -> None:
        d = decision.to_dict() if hasattr(decision, "to_dict") else decision
        self.conn.execute("""
            INSERT OR REPLACE INTO decisions (decision_id, lead_id, decision_type, payload, criado_em)
            VALUES (?, ?, ?, ?, ?)
        """, (
            d["decision_id"], d.get("lead_id"), d.get("decision_type"),
            json.dumps(d.get("payload", {})), d.get("criado_em"),
        ))
        self.conn.commit()

    def get_lead(self, lead_id: str) -> dict[str, Any] | None:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM leads WHERE lead_id = ?", (lead_id,))
        return cur.fetchone()

    def get_opportunities(self, prioridade: str | None = None) -> list[dict[str, Any]]:
        cur = self.conn.cursor()
        if prioridade:
            cur.execute("SELECT * FROM opportunities WHERE prioridade = ? ORDER BY score_geral DESC", (prioridade,))
        else:
            cur.execute("SELECT * FROM opportunities ORDER BY score_geral DESC")
        return cur.fetchall()

    def get_leads(self) -> list[dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM leads")
        return cur.fetchall()

    def get_all_decisions(self) -> list[dict[str, Any]]:
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM decisions ORDER BY criado_em DESC")
        return cur.fetchall()

    def close(self) -> None:
        self.conn.close()