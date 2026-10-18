# RADAR PUB

## Visão Geral

O Radar PUB é uma infraestrutura autônoma de prospecção comercial 24/7 para a PUB Holding. Uma máquina que continuamente descobre, pesquisa, qualifica e pontua oportunidades de negócios, gerando hipóteses acionáveis.

## Arquitetura

**RADAR PUB → business intelligence + opportunity engine**

---

**Hermes** (o orchestrator externo)

---

**PDL/Harness** (futuro executor)

---

**Agentes + Ferramentas + Execução**

## Fluxo Principal do MVP

```mermaid
graph LR
    A[Discovery] --> B[Research]
    B --> C[Analysis]
    C --> D[Scoring]
    D --> E[Opportunity]
</graph>
```

## Componentes Principais

- **Domínios** (entidades de negócios centrais): lead, research, score, opportunity
- **Módulos** (onde a lógica de negócios vive):
  - `core/discovery` - descoberta de leads
  - `core/research` - pesquisa de presença digital
  - `core/qualification` - qualificação de leads
  - `core/scoring` - pontuação baseada em critérios
  - `core/outreach` - (espaço reservado para futuro)
  - `core/followup` - (espaço reservado para futuro)
  - `core/memory` - histórico de decisões e aprendizado
- **Agentes** (dispositivos de processamento autônomos):
  - `agents/scout` - descobridor de leads
  - `agents/researcher` - pesquisador digital
  - `agents/analyst` - analista de dados
  - `agents/qualifier` - qualificador de oportunidades
  - `agents/outreach` - (espaço reservado para futuro)
  - `agents/followup` - (espaço reservado para futuro)

## Estrutura de Dados

### Lead
```json
{
  "empresa": "Nome da Empresa",
  "segmento": "SETOR",
  "localizacao": "CIDADE, PAÍS",
  "website": "https://example.com",
  "redes_sociais": ["linkedin", "twitter"]
}
```

### Research
```json
{
  "presenca_digital": "ALTA|MEDIA|BAIXA",
  "sinais_encontrados": ["website", "seo"],
  "problemas_detectados": ["falta_de_conversao"],
  "evidencias": []
}
```

### Score
```json
{
  "seo": 0.8,
  "website": 0.9,
  "social": 0.7,
  "tracking": 0.6,
  "conversion": 0.5,
  "commercial_potential": 0.8,
  "pontuacao_geral": 0.73,
  "prioridade": "ALTA|MEDIA|BAIXA",
  "hipotese": "TEXTO_DE_HIPOTESE",
  "motivo": "TEXTO_DO_MOTIVO",
  "proxima_acao": "CONTATO|EMAIL|MARKETING"
}
```

## Como Executar Localmente

```bash
# Instale dependências (se necessário)
# npm install ou python -m pip install -r requirements.txt

# Execute o radar
# node apps/radar/src/index.js

# Ou via docker (futuro)
# docker-compose up
```

## Documentação

- [`ARCHITECTURE.md`](./ARCHITECTURE.md) - arquitetura e design
- [`ROADMAP.md`](./ROADMAP.md) - roadmap do projeto
- [docs/conceitos](./docs/concepts/) - conceitos e fundamentos
- [docs/workflows](./docs/workflows/) - fluxos de trabalho
- [docs/decisions](./docs/decisions/) - decisões de design

## Licença

Proprietary