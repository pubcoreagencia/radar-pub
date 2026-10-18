#!/usr/bin/env python3
"""Demo run of Radar PUB pipeline with capability-fit scoring.

Executes the full pipeline (Discovery -> Research -> Analysis -> Scoring -> Opportunity)
for each lead fixture and prints:
- company name, pipeline score, capability_fit, commercial_fit, confidence
- matches for this lead (capability_id, problem, offers)
"""
import sys
import os

# project root on Windows path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import Pipeline


def main() -> None:
    pipeline = Pipeline()
    results = pipeline.run()

    if not results:
        print("Nenhum lead processado.")
        return

    print(f"=== DEMO — {len(results)} leads ===\n")
    for i, r in enumerate(results, 1):
        lead = r["lead"]
        empresa = lead["empresa"]
        opportunity = r["opportunity"]
        score = r["score"]
        analysis = r["analysis"]

        print(f"{i}. Empresa: {empresa}")
        print(f"   Score Geral: {opportunity['score_geral']:.3f}")
        print(f"   Capability Fit: {score['dimensoes'].get('capability_fit', 0):.2f}")
        print(f"   Commercial Fit: {score['dimensoes'].get('commercial_fit', 0):.2f}")
        print(f"   Confidence: {score['dimensoes'].get('confidence', 0):.2f}")
        print(f"   Prioridade: {opportunity['prioridade']}")
        print(f"   Hipótese: {opportunity['hipotese']}")

        # Reconstruir analysis para matcher
        from core.entities import Lead, Research, Analysis
        lead_obj = Lead(
            empresa=empresa,
            segmento=lead.get("segmento", ""),
            localizacao=lead.get("localizacao", ""),
            website=lead.get("website"),
            redes_sociais=lead.get("redes_sociais", []),
            fonte=lead.get("fonte", "unknown"),
            lead_id=lead.get("lead_id", ""),
        )
        research_obj = Research(
            lead_id=lead_obj.lead_id,
            presenca_digital=analysis.get("presenca_digital", "AUSENTE"),
            sinais_encontrados=analysis.get("sinais_encontrados", []),
            problemas_detectados=analysis.get("problemas_detectados", []),
            research_id=analysis.get("research_id", ""),
        )
        analysis_obj = Analysis(
            lead_id=analysis["lead_id"],
            research_id=analysis["research_id"],
            strengths=analysis.get("strengths", []),
            weaknesses=analysis.get("weaknesses", []),
            opportunities=analysis.get("opportunities", []),
            hypotheses=analysis.get("hypotheses", []),
            analysis_id=analysis.get("analysis_id", ""),
        )

        from core.capabilities.capability_matcher import match_capabilities
        matches = match_capabilities(lead_obj, research_obj, analysis_obj)
        print(f"   Matches de capabilities: {len(matches)}")
        for m in matches:
            offers = m.offers
            offers_str = f" ({len(offers)} ofertas)" if offers else ""
            print(f"      - {m.capability_id} ({m.fit_level}, conf={m.confidence:.2f}) problem={m.problem}{offers_str}")
        print()


if __name__ == "__main__":
    main()