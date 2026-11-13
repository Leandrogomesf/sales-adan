# Sales ADAN Hub — v3 (React + TypeScript + Vite)

Catálogo de produtos de dados do portfólio Sales ADAN (PepsiCo Brasil), reconstruído em React a partir da v1 (Streamlit), com visual inspirado no app de referência "Sales Intelligence v1".

## Rodar localmente

```bash
npm install
npm run dev
```

## Build de produção

```bash
npm run build
```

Gera a pasta `dist/` com os arquivos estáticos (HTML/CSS/JS) prontos para servir.

## Dados

Os dados ficam em `src/data/*.json`, convertidos a partir dos YAML da v1 (`../v1/data/*.yaml`). Para atualizar os dados depois de editar os YAML da v1, reconverta manualmente (não há automação deste passo ainda).

## Estrutura

- `src/pages/` — as 3 telas (Visão Geral, Produtos de Dados, Detalhe do Algoritmo)
- `src/components/` — componentes reutilizáveis (Sidebar, KpiCard, ProductCard, RoadmapBanner, etc.)
- `src/types.ts` — tipos TypeScript do schema de dados
