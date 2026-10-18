"""RADAR PUB — Merge reconciler: reconcilia múltiplos resultados de agente.

Útil para resolver divergências de agents autônomos (ex.: múltiplas análises de lead).
"""
from __future__ import annotations

from typing import Any, Dict, List


class MergeReconciler:
    """Reconciliation baseado em consenso.

    Funciona com:
    - ratings numéricos (média ponderada)
    - valores categóricos (primeiro wins)
    - estruturas aninhadas (mergão profundamente)
    """

    def merge_opportunities(self, opps: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not opps:
            return {}
        if len(opps) == 1:
            return opps[0]

        # score_geral numérico -> média
        scores = [o.get("score_geral", 0.0) for o in opps if isinstance(o.get("score_geral"), (int, float))]
        merged_score = sum(scores) / len(scores) if scores else 0.0

        # prioridade categórica -> mais comum
        prioridades = [o.get("prioridade") for o in opps if o.get("prioridade")]
        from collections import Counter
        prioridade_counts = Counter(prioridades)
        merged_prioridade = prioridade_counts.most_common(1)[0][0] if prioridade_counts else "BAIXA"

        # hipóteses: concatena unicidade
        hipo_set = set()
        for o in opps:
            hipo = o.get("hipotese")
            if hipo:
                hipo_set.add(hipo)
        merged_hipotese = list(hipo_set)[0] if hipo_set else ""

        # motivo: mais comum
        motivos = [o.get("motivo") for o in opps if o.get("motivo")]
        motivo_counts = Counter(motivos)
        merged_motivo = motivo_counts.most_common(1)[0][0] if motivo_counts else ""

        # próxima ação: primeira (fallback)
        proxima_acao = next((o.get("proxima_acao") for o in opps if o.get("proxima_acao")), "NUTRIÇÃO")

        # lead_id de qualquer um (comum)
        lead_id = opps[0].get("lead_id", "")

        return {
            "lead_id": lead_id,
            "score_geral": merged_score,
            "prioridade": merged_prioridade,
            "hipotese": merged_hipotese,
            "motivo": merged_motivo,
            "proxima_acao": proxima_acao,
        }

    def merge_scores(self, scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not scores:
            return {}
        if len(scores) == 1:
            return scores[0]
        # dimensões: média ponderada por peso (se houver)
        dimensoes_merged = {}
        for s in scores:
            dims = s.get("dimensoes", {})
            pesos = s.get("pesos", {})
            for k in set(dimensoes_merged) | set(dims):
                val1 = dimensoes_merged.get(k, 0.0)
                val2 = dims.get(k, 0.0)
                peso1 = pesos.get(k, 1.0)
                peso2 = pesos.get(k, 1.0)
                total_peso = peso1 + peso2
                if total_peso:
                    dimensoes_merged[k] = (val1 * peso1 + val2 * peso2) / total_peso
        # peso ponderado total
        pesos_merged = {}
        for s in scores:
            p = s.get("pesos", {})
            for k, v in p.items():
                pesos_merged[k] = pesos_merged.get(k, 0.0) + v
        # normaliza pesos para 1.0
        total = sum(pesos_merged.values()) or 1.0
        pesos_merged = {k: v / total for k, v in pesos_merged.items()}
        score_geral = sum((dimensoes_merged.get(k, 0.0) * pesos_merged.get(k, 0.0) for k in dimensoes_merged)) if pesos_merged else 0.0
        return {
            "score_geral": score_geral,
            "dimensoes": dimensoes_merged,
            "pesos": pesos_merged,
        }

    def merge_analyses(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not analyses:
            return {}
        if len(analyses) == 1:
            return analyses[0]
        # concatenação de conjuntos (unicidade)
        all_strengths = []
        all_weaknesses = []
        all_opps = []
        all_hypotheses = []
        for a in analyses:
            all_strengths.extend(a.get("strengths", []))
            all_weaknesses.extend(a.get("weaknesses", []))
            all_opps.extend(a.get("opportunities", []))
            all_hypotheses.extend(a.get("hypotheses", []))
        from collections import OrderedDict
        merged = {
            "strengths": list(OrderedDict.fromkeys(all_strengths)),
            "weaknesses": list(OrderedDict.fromkeys(all_weaknesses)),
            "opportunities": list(OrderedDict.fromkeys(all_opps)),
            "hypotheses": list(OrderedDict.fromkeys(all_hypotheses)),
        }
        return merged