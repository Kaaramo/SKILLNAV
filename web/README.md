# SKILLNAV Web

> Dashboard Next.js 15 du projet SKILLNAV — observatoire des compétences IA & Data Science.

**Stack** : Next.js 15 · React 19 · TypeScript 5.6 · Tailwind v4 · Shadcn/ui · TanStack Query · Recharts · Tremor · react-force-graph-2d.

**Owner** : Karamo Sylla (cf. PRD §11).

---

## Setup

```bash
# Prérequis
node --version   # >= 20
pnpm --version   # >= 9

# Installation
pnpm install

# Variables d'environnement
cp .env.example .env.local
# Éditer .env.local avec l'URL de l'API FastAPI

# Dev server
pnpm dev          # http://localhost:3000
```

L'API FastAPI doit tourner en parallèle (`make api` à la racine du repo).

---

## Scripts

| Commande | Action |
|---|---|
| `pnpm dev` | Dev server avec Turbopack |
| `pnpm build` | Build production |
| `pnpm start` | Serveur production local |
| `pnpm lint` | ESLint Next.js 15 |
| `pnpm typecheck` | `tsc --noEmit` strict |
| `pnpm format` | Prettier write |
| `pnpm format:check` | Prettier check (CI) |
| `pnpm generate-types` | Génère `src/lib/api/types.ts` depuis `/openapi.json` |

---

## Pages prévues (PRD §11.2)

| Route | Contenu |
|---|---|
| `/` | KPIs marché IA (Maroc + International) · top compétences |
| `/skills` | Tableau filtrable · score émergence · family · growth |
| `/graph` | Graphe Neo4j interactif (`react-force-graph-2d`) · filtres Louvain |
| `/forecasting` | ARIMA + Prophet + LSTM superposés · MAPE chiffré |
| `/ner-explorer` | Texte annoté side-by-side 3 modèles |
| `/methodology` | 3 axes · sources · RGPD · glossaire |
| `/comparative-study` | 4 tableaux N2.1 – N2.4 chiffrés |
| `/quality` | Complétude · bruit · biais (Data Quality Framework) |

Dark mode par défaut (Navy 1000) — cohérence avec la charte McKinsey.

---

## Conventions

- **Composants** : Shadcn/ui d'abord (copier-coller, pas de dépendance), Tremor pour dashboards rapides
- **Charts** : Recharts pour KPIs simples, Plotly pour interactif lourd, react-force-graph pour le graphe
- **Types API** : générés automatiquement via `pnpm generate-types` (jamais à la main)
- **State serveur** : TanStack Query exclusivement
- **Pas d'`any`** : ESLint strict

---

**SKILLNAV — M242 ENSA-Tétouan · Mai 2026**
