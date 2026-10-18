"""Scripts de ajuda para execução de demo do radar-pub MVP.

Permite iniciar pipeline, executar em modo rápido e ver resultado em terminal.
"""
import sys, os, json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.pipeline import Pipeline


def demo_run() -> None:
    pipe = Pipeline()
    print("[DEMO] Executando pipeline completo...")
    resultados = pipe.run()
    print(f"[DEMO] Processados {len(resultados)} leads.")
    for r in resultados:
        lead = r['lead']
        op = r['opportunity']
        print(f"[DEMO] {lead['empresa']} => {op['prioridade']} => {op['hipotese']}")


def demo_lead(empresa: str) -> None:
    from core.discovery.engine import discover
    pipe = Pipeline()
    for lead in discover():
        if empresa.lower() in lead.empresa.lower():
            print(f"[DEMO] Lead selecionado: {lead.empresa}")
            print(json.dumps(pipe.run_lead(lead), indent=2, ensure_ascii=False))
            return
    print(f"[DEMO] Nenhum lead encontrado com '{empresa}'")


def main() -> None:
    if len(sys.argv) > 1:
        if sys.argv[1] == 'run':
            demo_run()
        else:
            demo_lead(sys.argv[1])
    else:
        print("Uso:")
        print("  python scripts/demo.py run     # executar todos os leads")
        print("  python scripts/demo.py <empresa>  # executar lead específico")


if __name__ == "__main__":
    main()