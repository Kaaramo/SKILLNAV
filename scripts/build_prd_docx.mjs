#!/usr/bin/env node
/**
 * SKILLNAV — PRD CONDENSÉ — Generator DOCX premium
 *
 * Adapte la direction artistique de la charte (Navy + Royal Blue, Georgia / Calibri /
 * Consolas) au contenu structurel du PRD condensé : cover full-bleed, TOC numérotée,
 * sections eyebrow + titre serif, tables compactes, schémas ASCII en boxes monospace.
 *
 * Cible : 18-24 pages premium A4.
 */

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");
const OUT_DOCX = resolve(REPO_ROOT, "docs", "PRD_CONDENSE_SKILLNAV.docx");

const require = createRequire(import.meta.url);
const GLOBAL = "C:/Users/ksthe/AppData/Roaming/npm/node_modules";
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  Header,
  Footer,
  AlignmentType,
  BorderStyle,
  WidthType,
  ShadingType,
  VerticalAlign,
  PageNumber,
  PageBreak,
  TabStopType,
  TabStopPosition,
  HeightRule,
  TableLayoutType,
} = require(`${GLOBAL}/docx`);

// --- Tokens charte SKILLNAV ----------------------------------------------------
const C = {
  navy: "051C2C",
  navy900: "0A2540",
  navy800: "133553",
  navy700: "1F4868",
  royal: "2251FF",
  royalLight: "4F73FF",
  royalDark: "1A3FCC",
  royalSoft: "E5EBFF",
  white: "FFFFFF",
  cream: "FAF8F3",
  bone: "F5F1EB",
  border: "E5E7EB",
  borderSoft: "F0F2F5",
  ink: "1A1A1A",
  inkSoft: "4A4A4A",
  muted: "6B7280",
  mutedLight: "8FA3B8",
  success: "0F8F65",
  warning: "C77700",
  error: "B42318",
  monoBg: "F7F8FA",
};

const FONT_DISPLAY = "Georgia"; // proxy serif éditorial Fraunces
const FONT_BODY = "Calibri"; // proxy Inter
const FONT_MONO = "Consolas"; // proxy JetBrains Mono

// --- Page geometry (A4) --------------------------------------------------------
const PAGE_W = 11906;
const PAGE_H = 16838;
const MARGIN = 1080; // 0.75"
const CONTENT_W = PAGE_W - 2 * MARGIN; // 9746

// --- Helpers -------------------------------------------------------------------
const noneB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const NO_BORDER_ALL = {
  top: noneB, bottom: noneB, left: noneB, right: noneB,
  insideHorizontal: noneB, insideVertical: noneB,
};

const thin = (color = C.border) => ({ style: BorderStyle.SINGLE, size: 4, color });
const allBorders = (color = C.border) => ({
  top: thin(color), bottom: thin(color), left: thin(color), right: thin(color),
  insideHorizontal: thin(color), insideVertical: thin(color),
});

function tr(text, opts = {}) {
  const {
    font = FONT_BODY,
    size = 21,
    color = C.ink,
    bold = false,
    italics = false,
  } = opts;
  return new TextRun({ text, font, size, color, bold, italics });
}

function p(content, opts = {}) {
  const {
    align = AlignmentType.LEFT,
    spaceBefore = 0,
    spaceAfter = 100,
    indent,
    line = 300,
    pageBreakBefore = false,
  } = opts;
  return new Paragraph({
    alignment: align,
    indent,
    pageBreakBefore,
    spacing: { before: spaceBefore, after: spaceAfter, line, lineRule: "auto" },
    children: content === null ? []
      : Array.isArray(content) ? content
        : typeof content === "string" ? [tr(content, opts)]
          : [content],
  });
}

function spacer(h = 200) {
  return new Paragraph({
    spacing: { before: 0, after: h, line: 240, lineRule: "auto" },
    children: [tr(" ", { size: 2, color: C.white })],
  });
}

function rule(color = C.border, sizePt = 6, after = 240) {
  return new Paragraph({
    spacing: { before: 0, after, line: 200, lineRule: "auto" },
    border: { bottom: { style: BorderStyle.SINGLE, size: sizePt, color, space: 1 } },
    children: [],
  });
}

// Section title : eyebrow (NN · LABEL UPPER) + serif title + optional sublabel
function sectionTitle(num, label, sub = null, opts = {}) {
  const { breakBefore = true } = opts;
  const items = [];
  if (breakBefore) items.push(p(null, { pageBreakBefore: true, spaceAfter: 0 }));
  items.push(new Paragraph({
    spacing: { before: 0, after: 120, line: 280 },
    children: [
      tr(num + "  ", { font: FONT_BODY, size: 18, color: C.royal, bold: true }),
      tr(label.toUpperCase(), { font: FONT_BODY, size: 18, color: C.navy700, bold: true }),
    ],
  }));
  items.push(new Paragraph({
    spacing: { before: 0, after: 120, line: 360 },
    children: [tr(sub || label, { font: FONT_DISPLAY, size: 44, color: C.navy, bold: false })],
  }));
  items.push(rule(C.royal, 12, 360));
  return items;
}

// Lead paragraph after section title
function lead(text) {
  return p(text, { spaceAfter: 200, line: 320 });
}

// Code/ASCII box : light Navy soft background, Consolas, no wrap
function asciiBox(text, opts = {}) {
  const { size = 13, color = C.navy900, bg = C.monoBg, height } = opts;
  const lines = text.replace(/\r\n/g, "\n").split("\n");
  return new Table({
    layout: TableLayoutType.FIXED,
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    borders: allBorders(C.borderSoft),
    rows: [
      new TableRow({
        cantSplit: false,
        ...(height ? { height: { value: height, rule: HeightRule.ATLEAST } } : {}),
        children: [
          new TableCell({
            width: { size: CONTENT_W, type: WidthType.DXA },
            margins: { top: 200, bottom: 200, left: 280, right: 240 },
            shading: { fill: bg, type: ShadingType.CLEAR },
            verticalAlign: VerticalAlign.TOP,
            borders: allBorders(C.borderSoft),
            children: lines.map((ln) =>
              new Paragraph({
                spacing: { before: 0, after: 0, line: 240, lineRule: "auto" },
                children: [tr(ln === "" ? " " : ln, { font: FONT_MONO, size, color })],
              })
            ),
          }),
        ],
      }),
    ],
  });
}

// Inline pill (eyebrow callout)
function pill(text, color = C.royal) {
  return new TextRun({
    text: " " + text + " ",
    font: FONT_BODY,
    size: 16,
    color: C.white,
    bold: true,
    shading: { type: ShadingType.CLEAR, fill: color, color: "auto" },
  });
}

// Standard data table : column widths in DXA
function dataTable({ widths, headers, rows, headerFill = C.navy900, headerColor = C.white, zebra = true }) {
  const totalW = widths.reduce((a, b) => a + b, 0);
  const headerRow = new TableRow({
    tableHeader: true,
    cantSplit: true,
    height: { value: 480, rule: HeightRule.ATLEAST },
    children: headers.map((h, i) =>
      new TableCell({
        width: { size: widths[i], type: WidthType.DXA },
        margins: { top: 120, bottom: 120, left: 160, right: 160 },
        shading: { fill: headerFill, type: ShadingType.CLEAR },
        verticalAlign: VerticalAlign.CENTER,
        borders: allBorders(headerFill),
        children: [
          new Paragraph({
            spacing: { before: 0, after: 0, line: 240 },
            children: [tr(h, { font: FONT_BODY, size: 18, color: headerColor, bold: true })],
          }),
        ],
      })
    ),
  });
  const bodyRows = rows.map((row, ri) => new TableRow({
    cantSplit: false,
    children: row.map((cell, i) => {
      const isObj = cell !== null && typeof cell === "object" && !Array.isArray(cell);
      const text = isObj ? cell.text : cell;
      const align = isObj && cell.center ? AlignmentType.CENTER : AlignmentType.LEFT;
      const bold = isObj && cell.bold;
      const color = isObj && cell.color ? cell.color : C.ink;
      const fill = isObj && cell.fill ? cell.fill : (zebra && ri % 2 === 1 ? C.borderSoft : C.white);
      return new TableCell({
        width: { size: widths[i], type: WidthType.DXA },
        margins: { top: 100, bottom: 100, left: 160, right: 160 },
        shading: { fill, type: ShadingType.CLEAR },
        verticalAlign: VerticalAlign.CENTER,
        borders: allBorders(C.border),
        children: [
          new Paragraph({
            alignment: align,
            spacing: { before: 0, after: 0, line: 280 },
            children: [tr(text, { font: FONT_BODY, size: 19, color, bold })],
          }),
        ],
      });
    }),
  }));
  return new Table({
    layout: TableLayoutType.FIXED,
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: widths,
    rows: [headerRow, ...bodyRows],
    borders: allBorders(C.border),
  });
}

// Bullet (no manual unicode, simple indent + en-dash)
function bullet(text) {
  return new Paragraph({
    spacing: { before: 0, after: 60, line: 280 },
    indent: { left: 360, hanging: 200 },
    children: [
      tr("— ", { font: FONT_BODY, size: 21, color: C.royal, bold: true }),
      tr(text, { font: FONT_BODY, size: 21, color: C.ink }),
    ],
  });
}

// Two-column meta line (label · value)
function metaLine(label, value) {
  return new Paragraph({
    spacing: { before: 0, after: 60, line: 280 },
    tabStops: [{ type: TabStopType.LEFT, position: 2400 }],
    children: [
      tr(label.toUpperCase(), { font: FONT_BODY, size: 16, color: C.muted, bold: true }),
      tr("\t", {}),
      tr(value, { font: FONT_BODY, size: 21, color: C.ink }),
    ],
  });
}

// --- COVER PAGE ----------------------------------------------------------------
function coverPage() {
  const inner = [
    // Top label
    new Paragraph({
      spacing: { before: 0, after: 360, line: 240 },
      children: [tr("PRD CONDENSÉ — V2.0", {
        font: FONT_BODY, size: 18, color: C.royalLight, bold: true,
      })],
    }),
    // Display title
    new Paragraph({
      spacing: { before: 0, after: 120, line: 360 },
      children: [tr("SKILLNAV", {
        font: FONT_DISPLAY, size: 144, color: C.white, bold: false,
      })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 720, line: 360 },
      children: [tr("Skills Navigator", {
        font: FONT_DISPLAY, size: 56, color: C.royalLight, italics: true,
      })],
    }),
    // Subtitle / promesse
    new Paragraph({
      spacing: { before: 0, after: 100, line: 360 },
      children: [tr("Observatoire des compétences IA & Data Science", {
        font: FONT_BODY, size: 32, color: C.white, bold: true,
      })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 4200, line: 320 },
      children: [tr("par le Web Mining — Maroc + International", {
        font: FONT_BODY, size: 24, color: "C7D5E5",
      })],
    }),
    // Footer
    new Paragraph({
      spacing: { before: 0, after: 0 },
      children: [
        tr("M242 · ENSA-Tétouan", { font: FONT_BODY, size: 18, color: C.royalLight, bold: true }),
        tr("        ", { font: FONT_BODY, size: 18 }),
        tr("Karamo Sylla & Bachirou Konaté", { font: FONT_BODY, size: 18, color: C.mutedLight }),
        tr("        ", { font: FONT_BODY, size: 18 }),
        tr("Mai 2026", { font: FONT_BODY, size: 18, color: C.mutedLight }),
      ],
    }),
  ];
  return new Table({
    layout: TableLayoutType.FIXED,
    width: { size: CONTENT_W, type: WidthType.DXA },
    columnWidths: [CONTENT_W],
    borders: NO_BORDER_ALL,
    rows: [
      new TableRow({
        cantSplit: false,
        height: { value: 13800, rule: HeightRule.ATLEAST },
        children: [
          new TableCell({
            width: { size: CONTENT_W, type: WidthType.DXA },
            margins: { top: 1800, bottom: 1200, left: 720, right: 720 },
            shading: { fill: C.navy, type: ShadingType.CLEAR },
            verticalAlign: VerticalAlign.TOP,
            borders: NO_BORDER_ALL,
            children: inner,
          }),
        ],
      }),
    ],
  });
}

// --- TOC ----------------------------------------------------------------------
function tocLine(num, title, page) {
  return new Paragraph({
    spacing: { before: 0, after: 100, line: 320 },
    tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W - 100, leader: "dot" }],
    children: [
      tr(num, { font: FONT_BODY, size: 18, color: C.royal, bold: true }),
      tr("   ", {}),
      tr(title, { font: FONT_BODY, size: 21, color: C.navy900 }),
      tr("\t", {}),
      tr(page, { font: FONT_BODY, size: 18, color: C.muted }),
    ],
  });
}

function tocBlock() {
  return [
    p(null, { pageBreakBefore: true, spaceAfter: 0 }),
    new Paragraph({
      spacing: { before: 240, after: 80, line: 280 },
      children: [tr("SOMMAIRE", { font: FONT_BODY, size: 18, color: C.royal, bold: true })],
    }),
    new Paragraph({
      spacing: { before: 0, after: 360, line: 360 },
      children: [tr("Table des matières", { font: FONT_DISPLAY, size: 44, color: C.navy })],
    }),
    rule(C.royal, 12, 360),
    tocLine("01", "Sujet → sections du PRD", "4"),
    tocLine("02", "Mapping projet ↔ 3 axes Web Mining", "5"),
    tocLine("03", "Parcours interne du binôme", "6"),
    tocLine("04", "Fonctionnalités MVP → V1.5 → V2", "8"),
    tocLine("05", "Sources de données", "10"),
    tocLine("06", "Architecture technique", "12"),
    tocLine("07", "Stack technique + coûts MVP", "15"),
    tocLine("08", "Étude comparative algorithmique (§N2)", "16"),
    tocLine("09", "RGPD + robots.txt (§N4)", "17"),
    tocLine("10", "Livrables (6 livrables Pr. Sassi) + Détail L5", "18"),
    tocLine("11", "Dashboard Next.js — 8 pages", "19"),
    tocLine("12", "Structure du repository", "20"),
    tocLine("13", "Calendrier — 18 jours, 3 sprints", "21"),
    tocLine("14", "Soutenance — 25 minutes", "22"),
    tocLine("15", "Indicateurs de succès", "23"),
    tocLine("16", "Plans B (sprints sous tension)", "23"),
    tocLine("17", "RACI — répartition Karamo / Bachirou Konaté", "24"),
  ];
}

// =============================================================================
// SECTIONS
// =============================================================================

// --- 01 — Sujet → PRD ---------------------------------------------------------
function s01() {
  return [
    ...sectionTitle("01", "Sujet", "Sujet du Pr. Sassi → sections du PRD"),
    lead("Six exigences structurent le sujet imposé. Chacune est couverte par une ou plusieurs sections de ce document — la table ci-dessous est la lecture la plus rapide pour le jury."),
    asciiBox(
`┌──────────────────────────────────────────────────────────────────┐
│  SUJET PR. SASSI — 6 EXIGENCES                                   │
│                                                                  │
│  E1 ─ 3 axes Web Mining (Content / Structure / Usage) ─→ §2 + §6 │
│  E2 ─ NoSQL hybride justifiée ──────────────────────────→ §5     │
│  E3 ─ Pipeline IA + HuggingFace Transformers ──────────→ §6.B    │
│  E4 ─ Étude comparative ≥ 3 algos par tâche ───────────→ §8      │
│  E5 ─ RGPD + robots.txt + anonymisation ───────────────→ §9      │
│  E6 ─ 6 livrables (scripts, BD, IA, dashboard, rapport, soutenance)│
│                                                          → §10   │
└──────────────────────────────────────────────────────────────────┘`,
      { size: 14 }
    ),
    spacer(160),
    p([
      tr("Volume cible MVP ", { bold: true, color: C.navy700 }),
      tr("· 500–2 000 offres analysées · Maroc + International · sur 3–6 mois.", { color: C.inkSoft }),
    ], { spaceAfter: 60 }),
    p([
      tr("Architecture ", { bold: true, color: C.navy700 }),
      tr("· NoSQL polyglotte — MongoDB Atlas (source of truth) + Neo4j AuraDB (graphe) + Elasticsearch Cloud (recherche).", { color: C.inkSoft }),
    ], { spaceAfter: 60 }),
    p([
      tr("Coût MVP ", { bold: true, color: C.navy700 }),
      tr("· < $50 (free tiers + Anthropic + Apify).", { color: C.inkSoft }),
    ]),
  ];
}

// --- 02 — Mapping 3 axes ------------------------------------------------------
function s02() {
  return [
    ...sectionTitle("02", "Mapping", "Projet ↔ 3 axes Web Mining"),
    lead("Couverture équilibrée des trois axes canoniques (Content, Structure, Usage). C'est la section que le jury lit en premier."),
    dataTable({
      widths: [1900, 900, 2700, 2300, 1946],
      headers: ["Axe", "Pondé.", "Technique", "Algos comparés", "Livrable principal"],
      rows: [
        ["Content", { text: "35 %", center: true, bold: true, color: C.royal }, "NER + extraction structurée", "BERT-multi · CamemBERT-NER · DistilBERT (+ baseline)", "Notebook 02_ner_comparison · /ner-explorer"],
        ["Structure", { text: "30 %", center: true, bold: true, color: C.royal }, "Graphe Skill ↔ Job ↔ Family + communautés", "Louvain · Label Propagation · Leiden", "Neo4j AuraDB · /graph"],
        ["Usage", { text: "30 %", center: true, bold: true, color: C.royal }, "Forecasting + détection émergence", "ARIMA · Prophet · LSTM", "Notebook 04_forecasting_comparison · /forecasting"],
        ["Transverse", { text: "5 %", center: true, color: C.muted }, "Data Quality · Pipeline · Dashboard", "—", "Pages /quality, /methodology, /comparative-study"],
      ],
    }),
  ];
}

// --- 03 — Parcours interne ----------------------------------------------------
function s03() {
  return [
    ...sectionTitle("03", "Parcours", "Parcours interne — binôme Karamo + Bachirou Konaté"),
    lead("Pipeline optimisé exécuté à chaque sprint. Tout tourne en local + DBs cloud free tier. Sept étapes de la collecte au rapport L5."),
    asciiBox(
`┌─────────────────────────────────────────────────────────────────┐
│  DÉBUT DE SPRINT — Karamo & Bachirou Konaté                     │
│  Repo cloné · Poetry installé · DBs cloud free tier             │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 1 — COLLECTE                          (Karamo lead)      │
│  Scrapy + Playwright + Apify MCP + Firecrawl                    │
│   • Maroc        : Rekrute, EmploiTIC, LinkedIn MA              │
│   • International: LinkedIn, Indeed, builtin.com, WTTJ          │
│   • Signaux      : Google Trends, GitHub, HuggingFace           │
│   • Persistence  : MongoDB Atlas — collection raw_jobs          │
│  ~30 min / 500 offres                                           │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 2 — EXTRACTION IA + NER               (Karamo lead)      │
│  $ poetry run skillnav extract --batch=last                     │
│   • Pydantic AI + Claude Sonnet 4.5  → extracted_jobs           │
│   • HF Transformers × 3 modèles      → ner_annotations          │
│   • Quarantaine auto si confidence < 0.75                       │
│  ~30 min / 500 offres · coût ~$5–10                             │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 3 — GRAPHE                  (Bachirou Konaté lead)       │
│  $ poetry run skillnav graph build                              │
│   • Co-occurrences Skill ↔ Skill ↔ Job ↔ Family                 │
│   • Neo4j AuraDB (nœuds + arêtes)                               │
│   • Algos : PageRank, Louvain, Label Propagation                │
│  ~10 min                                                        │
└─────────────────────────────────────────────────────────────────┘`,
      { size: 13 }
    ),
    spacer(120),
    asciiBox(
`                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 4 — INDEX + FORECASTING              (Karamo lead)       │
│  $ poetry run skillnav index push                               │
│  $ poetry run skillnav forecast run                             │
│   • Elasticsearch : jobs_search + skills_timeseries             │
│   • ARIMA / Prophet / LSTM sur skill_count(time)                │
│  ~15 min                                                        │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 5 — NOTEBOOKS + DATA QUALITY         (binôme)            │
│   01_data_quality          (Bachirou Konaté)                    │
│   02_ner_comparison        (Karamo)                             │
│   03_graph_analysis        (Bachirou Konaté)                    │
│   04_forecasting_comparison(Karamo)                             │
│   05_dashboard_data_prep   (Karamo)                             │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 6 — DASHBOARD NEXT.JS                (Karamo lead)       │
│  $ cd web && pnpm dev                                           │
│   • 8 pages : /, /skills, /graph, /forecasting,                 │
│     /ner-explorer, /methodology, /comparative-study, /quality   │
│   • Données : FastAPI + JSON pré-calculés                       │
│   • Visu : Recharts, Tremor, react-force-graph, Plotly          │
└─────────────────────────────────────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  ÉTAPE 7 — RAPPORT L5 + DECK                                    │
│   • Bachirou Konaté : rédaction L5 intégrale                    │
│   • Karamo          : captures dashboard, schémas archi, deck   │
└─────────────────────────────────────────────────────────────────┘`,
      { size: 13 }
    ),
  ];
}

// --- 04 — Fonctionnalités MVP / V1.5 / V2 -------------------------------------
function s04() {
  const fRow = (id, axe, name, mvp, v15, v2) => [
    { text: id, center: true, bold: true, color: C.navy700 },
    { text: axe, center: true, color: C.royal, bold: true },
    name,
    { text: mvp, center: true, color: mvp === "✅" ? C.success : C.muted, bold: mvp === "✅" },
    { text: v15, center: true, color: v15 === "✅" ? C.success : C.muted, bold: v15 === "✅" },
    { text: v2, center: true, color: v2 === "✅" ? C.success : C.muted, bold: v2 === "✅" },
  ];
  const widths = [780, 580, 5806, 860, 860, 860];
  return [
    ...sectionTitle("04", "Fonctionnalités", "MVP → V1.5 → V2"),
    lead("Vingt-neuf fonctionnalités rattachées chacune à un axe Web Mining (C = Content, S = Structure, U = Usage, T = Transverse)."),
    dataTable({
      widths,
      headers: ["#", "Axe", "Fonctionnalité", "MVP", "V1.5", "V2"],
      rows: [
        fRow("F01", "T", "Scraping Maroc (Rekrute, EmploiTIC, LinkedIn MA)", "✅", "✅", "✅"),
        fRow("F02", "T", "Scraping International (LinkedIn, Indeed, builtin, WTTJ)", "✅", "✅", "✅"),
        fRow("F03", "T", "Signaux faibles (Google Trends, GitHub, HF)", "✅", "✅", "✅"),
        fRow("F04", "C", "Extraction Pydantic AI (skills + responsibilities)", "✅", "✅", "✅"),
        fRow("F05", "C", "NER comparatif 3 modèles HF", "✅", "✅", "✅"),
        fRow("F06", "C", "Normalisation taxonomique (sentence-transformers)", "✅", "✅", "✅"),
        fRow("F07", "C", "Classification 10 familles IA / DS", "✅", "✅", "✅"),
        fRow("F08", "S", "Graphe Neo4j (Skill / Job / Family / Source)", "✅", "✅", "✅"),
        fRow("F09", "S", "PageRank — top compétences-pivot", "✅", "✅", "✅"),
        fRow("F10", "S", "Communautés (Louvain · Label Propag · Leiden)", "✅", "✅", "✅"),
        fRow("F11", "U", "Séries temporelles skill_count(time) mensuelles", "✅", "✅", "✅"),
        fRow("F12", "U", "Forecasting (ARIMA · Prophet · LSTM)", "✅", "✅", "✅"),
        fRow("F13", "U", "Détection émergence (3 méthodes comparées)", "✅", "✅", "✅"),
        fRow("F14", "T", "Indexation Elasticsearch", "✅", "✅", "✅"),
        fRow("F15", "T", "API FastAPI typée OpenAPI", "✅", "✅", "✅"),
        fRow("F16", "T", "Dashboard Next.js (8 pages)", "✅", "✅", "✅"),
        fRow("F17", "T", "5 notebooks Jupyter numérotés", "✅", "✅", "✅"),
        fRow("F18", "T", "Rapport méthodologique L5 (PDF)", "✅", "✅", "✅"),
        fRow("F19", "T", "Deck soutenance + démo live", "✅", "✅", "✅"),
        fRow("F20", "T", "Exports datasets anonymisés", "✅", "✅", "✅"),
        fRow("F25", "C", "Fine-tuning CamemBERT sur gold set SKILLNAV", "—", "✅", "✅"),
        fRow("F26", "T", "Déploiement public skillnav.ma", "—", "✅", "✅"),
        fRow("F27", "T", "Pipeline live (Celery + APScheduler)", "—", "—", "✅"),
        fRow("F28", "C", "Agents prospectifs (Claude Agent SDK)", "—", "—", "✅"),
        fRow("F29", "T", "API publique versionnée", "—", "—", "✅"),
      ],
    }),
  ];
}

// --- 05 — Sources de données --------------------------------------------------
function s05() {
  return [
    ...sectionTitle("05", "Sources", "Sources de données — 3 catégories"),
    lead("Chaque source est inscrite au registre YAML avec robots.txt vérifié, TOS revu, rate-limit. Toutes nourrissent la collection MongoDB raw_jobs."),
    p([tr("5.1 Maroc — national", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    dataTable({
      widths: [2400, 2900, 4446],
      headers: ["Source", "Mode collecte", "Particularité"],
      rows: [
        ["Rekrute", "Scrapy (HTML statique)", "Premier portail MA · sitemap accessible"],
        ["EmploiTIC", "Scrapy + Playwright (JS)", "Spécialisé IT — IA / DS / dev"],
        ["LinkedIn MA", "Apify MCP linkedin-jobs-scraper", "Plafond 200 offres / session"],
        ["Pages carrières", "Firecrawl MCP", "OCP, INWI, banques, scale-ups"],
      ],
    }),
    spacer(160),
    p([tr("5.2 International", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    dataTable({
      widths: [2400, 2900, 4446],
      headers: ["Source", "Mode collecte", "Particularité"],
      rows: [
        ["LinkedIn International", "Apify (FR + EU + US)", "Volume principal compétences mondiales"],
        ["Indeed (.fr / .com)", "Scrapy + Playwright", "HTML stable, FR + EN"],
        ["builtin.com", "Scrapy", "Tech-only US, IA pointue"],
        ["Welcome to the Jungle", "Playwright (SPA)", "Marché tech FR, descriptions denses"],
        ["Otta (si bandwidth)", "Firecrawl", "Tech jobs UK / EU"],
      ],
    }),
    spacer(160),
    p([tr("5.3 Signaux faibles (validation Usage Mining)", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    dataTable({
      widths: [2700, 3200, 3846],
      headers: ["Source", "Type", "Library"],
      rows: [
        ["Google Trends", "Recherches publiques (proxy intérêt)", "pytrends"],
        ["GitHub Trending", "Repos tendance (langages / topics IA)", "API GitHub"],
        ["HuggingFace Trending", "Modèles / datasets tendance", "API HF Hub"],
        ["Papers With Code", "Papers IA tendance par benchmark", "Scraping"],
      ],
    }),
    spacer(160),
    p([tr("5.4 Volume cible MVP", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    asciiBox(
`Maroc national       :   300 –   500 offres
International (FR/EN):   800 – 1 500 offres
Signaux faibles      :    50 –   100 séries temporelles
                      ─────────────────────────────────
TOTAL                :         500 – 2 000 offres`,
      { size: 14 }
    ),
    spacer(160),
    p([tr("5.5 Conformité — registre source (extrait)", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    asciiBox(
`- id: rekrute_ma
  name: Rekrute
  base_url: https://www.rekrute.com
  robots_txt_compliant: true
  tos_reviewed_at: 2026-05-08
  rate_limit_seconds: 5
  user_agent: "SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)"`,
      { size: 14 }
    ),
  ];
}

// --- 06 — Architecture --------------------------------------------------------
function s06() {
  return [
    ...sectionTitle("06", "Architecture", "Architecture technique"),
    lead("Trois schémas : pipeline global, pipeline NER détaillé, architecture des données polyglotte. Pydantic v2 reste la source de vérité unique — un changement de schéma casse au type-check tous les converters."),
    p([tr("6.A Pipeline global", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    asciiBox(
`   ┌──────────────────────────────────────────┐
   │  COLLECTE  (Karamo)                      │
   │  Scrapy · Playwright · Apify · Firecrawl │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  data/raw/{source}_{date}.jsonl          │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INGESTION (Pydantic) → MongoDB raw_jobs │
   │  Dédup SHA-256 (company+title+location)  │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  CONTENT  (Karamo)                       │
   │  ┌──────────────────────────────────────┐│
   │  │ Pydantic AI + Claude Sonnet 4.5      ││
   │  │  → extracted_jobs                    ││
   │  └──────────────────────────────────────┘│
   │  ┌──────────────────────────────────────┐│
   │  │ HF Transformers × 3 modèles          ││
   │  │  → ner_annotations                   ││
   │  └──────────────────────────────────────┘│
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  STRUCTURE  (Bachirou Konaté)            │
   │  Graphe → Neo4j AuraDB                   │
   │  PageRank · Louvain · Label Propag       │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  USAGE  (Karamo)                         │
   │  Séries temporelles skill_count(time)    │
   │  ARIMA · Prophet · LSTM                  │
   │  Détection émergentes (3 méthodes)       │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  INDEXATION → Elasticsearch              │
   │  jobs_search · skills_timeseries         │
   └─────────────────┬────────────────────────┘
                     ▼
   ┌──────────────────────────────────────────┐
   │  API + DASHBOARD                         │
   │  FastAPI ↔ Mongo / Neo4j / ES            │
   │  Next.js 15 ↔ FastAPI                    │
   │  Render (API) + Vercel (UI)              │
   └──────────────────────────────────────────┘`,
      { size: 13 }
    ),
    spacer(200),
    p([tr("6.B Pipeline NER détaillé", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    asciiBox(
`   raw_text + lang
        │
        ▼
   ┌────────────────────────────────┐
   │  Cleaning                      │
   │   BeautifulSoup → text propre  │
   │   fasttext-langdetect (lang)   │
   │   spaCy (tokenization)         │
   └────────┬───────────────────────┘
            │
   ┌────────▼─────────────────────────┐
   │  Pydantic AI + Claude Sonnet 4.5 │
   │  → extracted_jobs (BSON)         │
   │  Confidence ≥ 0.75 sinon quaran. │
   └────────┬─────────────────────────┘
            │
   ┌────────▼───────────────────────┐
   │  HF Transformers (parallèle)   │
   │   • bert-multi  → tous langues │
   │   • camembert   → fr seulement │
   │   • distilbert  → en seulement │
   │  Mapping → SKILL/TOOL/FRAMEWORK│
   │           /MODEL/LANGUAGE/ROLE │
   └────────┬───────────────────────┘
            │
   ┌────────▼───────────────────────┐
   │  Normalisation taxonomique     │
   │   sentence-transformers        │
   │   cosine sim ≥ 0.85 → alias    │
   └────────────────────────────────┘`,
      { size: 13 }
    ),
    spacer(200),
    p([tr("6.C Architecture des données — polyglot", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    asciiBox(
`MONGODB ATLAS  (source of truth)
   sources              ─→ registre des origines + conformité
   raw_jobs             ─→ HTML brut + metadata
       │1
       ▼N
   extracted_jobs       ─→ Pydantic AI structuré
       │1
       ▼N
   ner_annotations      ─→ 3 docs/offre (1 par modèle NER)
   skills_taxonomy      ─→ canoniques + aliases
   skills_timeseries    ─→ volumes mensuels
   forecasts            ─→ ARIMA / Prophet / LSTM + IC
   graph_metrics        ─→ PageRank, Louvain modularité

NEO4J AURADB   (dérivé)
   (:Skill)-[:CO_OCCURS_WITH {weight}]->(:Skill)
   (:Job)-[:REQUIRES {confidence}]->(:Skill)
   (:Skill)-[:BELONGS_TO]->(:SkillFamily)
   (:Job)-[:FROM_SOURCE]->(:Source)

ELASTICSEARCH  (dérivé)
   jobs_search          ─→ full-text + filtres pays/famille/période
   skills_timeseries    ─→ agrégations mensuelles`,
      { size: 13 }
    ),
  ];
}

// --- 07 — Stack technique + coûts ---------------------------------------------
function s07() {
  return [
    ...sectionTitle("07", "Stack", "Stack technique + coûts MVP"),
    lead("Une stack assumée : Python 3.12 + Poetry côté pipeline IA, Next.js 15 + TypeScript côté front. Tous les services backend sur free tiers."),
    dataTable({
      widths: [2200, 5500, 2046],
      headers: ["Couche", "Outil", "Version"],
      rows: [
        ["Language", "Python", "3.12"],
        ["Package", "Poetry", "1.8+"],
        ["Scraping", "Scrapy · Playwright · Apify MCP · Firecrawl MCP", "latest"],
        ["Extraction IA", "pydantic-ai · anthropic (Claude Sonnet 4.5 + Haiku 4.5)", "latest"],
        ["NLP", "transformers · sentence-transformers · spaCy · fasttext-langdetect", "4.40+"],
        ["Graph", "neo4j-driver · networkx · python-louvain · igraph · neo4j-GDS", "5.20+"],
        ["Time series", "statsmodels · prophet · neuralforecast (Nixtla) · pytrends", "latest"],
        ["Storage", "MongoDB Atlas (M0) · Neo4j AuraDB Free · Elastic Cloud Free", "—"],
        ["Drivers", "motor · neo4j · elasticsearch", "latest"],
        ["API", "FastAPI · uvicorn", "0.110+"],
        ["Front", "Next.js 15 · TypeScript 5.4 · Tailwind v4 · Shadcn/ui · TanStack Query 5", "—"],
        ["Charts", "Recharts · Tremor · react-force-graph-2d · Plotly", "latest"],
        ["DevOps", "GitHub · Render (API) · Vercel (UI)", "—"],
        ["Quality", "ruff · mypy · black · pytest", "latest"],
      ],
    }),
    spacer(200),
    p([tr("7.1 Coûts MVP (18 jours)", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    asciiBox(
`Apify (LinkedIn)        $5–10
Anthropic Claude        $10–20
MongoDB Atlas           $0       (Free M0)
Neo4j AuraDB            $0       (Free)
Elastic Cloud           $0       (Free 14j → couvre soutenance)
Vercel · Render · GH    $0       (Hobby / Free)
HuggingFace             $0       (inférence locale)
                        ──────
TOTAL MVP            < $50`,
      { size: 14 }
    ),
  ];
}

// --- 08 — Étude comparative §N2 -----------------------------------------------
function s08() {
  return [
    ...sectionTitle("08", "Étude", "Étude comparative algorithmique (§N2)"),
    lead("Quatre tableaux chiffrés — c'est la preuve d'évaluation principale pour le jury. Toutes les comparaisons sont quantitatives, jamais purement qualitatives."),
    p([tr("8.1 NER (axe Content)", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    dataTable({
      widths: [3300, 1700, 1500, 3246],
      headers: ["Modèle", "Langues", "Poids", "F1 attendu (gold 30 offres)"],
      rows: [
        ["Baseline règles (regex)", "toutes", "0 MB", { text: "témoin", color: C.muted }],
        ["bert-base-multilingual-cased", "toutes", "700 MB", "0.62 – 0.68"],
        ["Jean-Baptiste/camembert-ner", "FR", "440 MB", "0.78 – 0.85 (FR)"],
        ["distilbert-conll03-english", "EN", "260 MB", "0.80 – 0.87 (EN)"],
      ],
    }),
    p([
      tr("Choix MVP : ", { bold: true, color: C.royal }),
      tr("routage par langue détectée (camembert FR / distilbert EN / bert-multi fallback). Notebook 02_ner_comparison.ipynb chiffre le gain réel.", { color: C.inkSoft }),
    ], { spaceBefore: 120, spaceAfter: 200 }),

    p([tr("8.2 Communautés (axe Structure)", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    dataTable({
      widths: [2600, 3200, 2200, 1746],
      headers: ["Algo", "Bibliothèque", "Modularité attendue", "Stabilité"],
      rows: [
        ["Louvain", "python-louvain / Neo4j GDS", "0.45 – 0.60", "Moyenne"],
        ["Label Propagation", "networkx", "0.40 – 0.55", { text: "Faible", color: C.warning, bold: true }],
        ["Leiden", "igraph", "0.45 – 0.62", { text: "Élevée", color: C.success, bold: true }],
      ],
    }),
    p([
      tr("Choix MVP : ", { bold: true, color: C.royal }),
      tr("Louvain par défaut (équilibre qualité / stabilité). Leiden = validateur. Label Propagation = baseline rapide.", { color: C.inkSoft }),
    ], { spaceBefore: 120, spaceAfter: 200 }),

    p([tr("8.3 Forecasting (axe Usage)", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    dataTable({
      widths: [3000, 3500, 3246],
      headers: ["Modèle", "Famille", "MAPE attendu (top 10 skills)"],
      rows: [
        ["ARIMA", "Statistique classique", "18 – 28 %"],
        ["Prophet", "Décomposition Meta", "12 – 18 %"],
        ["LSTM (neuralforecast)", "Deep learning", "10 – 22 %"],
      ],
    }),
    p([
      tr("Protocole : ", { bold: true, color: C.royal }),
      tr("train/test split 9 mois / 3 mois, MAPE médian top 10 skills, intervalles de confiance affichés sur /forecasting.", { color: C.inkSoft }),
    ], { spaceBefore: 120, spaceAfter: 200 }),

    p([tr("8.4 Détection émergence", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    dataTable({
      widths: [2700, 3200, 1900, 1946],
      headers: ["Méthode", "Approche", "Force", "Faiblesse"],
      rows: [
        ["Heuristique pondérée", "Score = f(growth, recency, vol.)", "Interprétable", "Seuils arbitraires"],
        ["Supervisé XGBoost", "Train sur 50 skills annotés", "Précision ↑", "Coût annotation"],
        ["Clustering temporel", "KMeans sur trajectoires", "Non supervisé", "Bruité"],
      ],
    }),
    p([
      tr("Synthèse → page /comparative-study : ", { bold: true, color: C.royal }),
      tr("4 tableaux chiffrés + interprétations + choix justifiés.", { color: C.inkSoft }),
    ], { spaceBefore: 120 }),
  ];
}

// --- 09 — RGPD ----------------------------------------------------------------
function s09() {
  return [
    ...sectionTitle("09", "RGPD", "RGPD + robots.txt + anonymisation (§N4)"),
    lead("Périmètre minimal et défendable : aucune donnée personnelle de candidat collectée. Base légale art. 6.1.f RGPD — intérêt légitime de recherche académique."),
    asciiBox(
`┌──────────────────────────────────────────────────────────────────┐
│  BASE LÉGALE   art. 6.1.f RGPD — intérêt légitime                │
│  CADRE         Recherche académique encadrée (ENSA-Tétouan)      │
│  PÉRIMÈTRE     Données publiques d'entités JURIDIQUES uniquement │
│                Aucune donnée personnelle de candidat collectée   │
└──────────────────────────────────────────────────────────────────┘`,
      { size: 14 }
    ),
    spacer(200),
    dataTable({
      widths: [5800, 3946],
      headers: ["Donnée", "Statut"],
      rows: [
        ["Nom employeur, ville, secteur", { text: "✅ Collecté (entité morale)", color: C.success, bold: true }],
        ["Description offre, compétences, salaire", { text: "✅ Collecté (donnée publique)", color: C.success, bold: true }],
        ["Nom recruteur, email, téléphone", { text: "❌ Jamais collecté", color: C.error, bold: true }],
        ["URL profil candidat, photo, parcours", { text: "❌ Jamais collecté", color: C.error, bold: true }],
      ],
    }),
    spacer(200),
    p([
      tr("Protocole robots.txt : ", { bold: true, color: C.navy700 }),
      tr("parsing systématique, log compliance, respect ", { color: C.inkSoft }),
      tr("Crawl-delay", { font: FONT_MONO, size: 19, color: C.navy900 }),
      tr(", rate limiting 5 s minimum sur sources statiques. User-Agent identifié ", { color: C.inkSoft }),
      tr("SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)", { font: FONT_MONO, size: 19, color: C.navy900 }),
      tr(". Voir RGPD_DPIA.md pour le DPIA complet.", { color: C.inkSoft }),
    ]),
  ];
}

// --- 10 — Livrables ----------------------------------------------------------
function s10() {
  return [
    ...sectionTitle("10", "Livrables", "6 livrables imposés par le Pr. Sassi"),
    lead("Alignement strict sur les six livrables imposés. La colonne « Owner » identifie la personne accountable du livrable."),
    dataTable({
      widths: [780, 2400, 4400, 2166],
      headers: ["#", "Livrable imposé", "Forme livrée", "Owner"],
      rows: [
        [{ text: "L1", center: true, bold: true, color: C.royal }, "Scripts de collecte documentés", "Repo skillnav/ (scrapers/, pipelines/) + README", "Karamo"],
        [{ text: "L2", center: true, bold: true, color: C.royal }, "Base de données hybride", "MongoDB Atlas + Neo4j AuraDB + Elastic Cloud (dumps fournis)", "Karamo + Bachirou Konaté"],
        [{ text: "L3", center: true, bold: true, color: C.royal }, "Pipeline IA validé par métriques", "Notebook 02_ner_comparison + page /comparative-study", "Karamo"],
        [{ text: "L4", center: true, bold: true, color: C.royal }, "Dashboard interactif", "skillnav.vercel.app (8 pages)", { text: "Karamo", bold: true, color: C.navy700 }],
        [{ text: "L5", center: true, bold: true, color: C.royal }, "Rapport méthodologique", "RAPPORT_METHODOLOGIQUE.md → PDF (25–40 pages)", { text: "Bachirou Konaté", bold: true, color: C.navy700 }],
        [{ text: "L6", center: true, bold: true, color: C.royal }, "Présentation soutenance", "PLAN_SOUTENANCE.md + deck PPTX + démo live", "Bachirou Konaté + Karamo"],
      ],
    }),
    spacer(240),
    p([tr("10.1 Détail L5 — Rapport méthodologique", { font: FONT_BODY, size: 22, bold: true, color: C.navy700 })], { spaceBefore: 120, spaceAfter: 120 }),
    asciiBox(
`1. Introduction         (contexte, problème, contribution)
2. État de l'art        (Web Mining, NER, graph mining, forecasting IA)
3. Méthodologie
   3.1 Sources et collecte
   3.2 Architecture polyglotte (MongoDB + Neo4j + ES)
   3.3 Pipeline Content (Pydantic AI + Transformers)
   3.4 Pipeline Structure (Neo4j + PageRank + Louvain)
   3.5 Pipeline Usage (ARIMA + Prophet + LSTM)
   3.6 Data Quality Framework
   3.7 RGPD + éthique
4. Résultats — Étude comparative
   4.1 NER comparé           (tableau N2.1)
   4.2 Communautés comparées (tableau N2.2)
   4.3 Forecasting comparé   (tableau N2.3)
   4.4 Émergence comparée    (tableau N2.4)
5. Discussion           (limites, biais, plans B)
6. Conclusion + V1.5 / V2
7. Bibliographie
8. Annexes (schéma Pydantic, ADRs, captures dashboard)`,
      { size: 13 }
    ),
    spacer(160),
    p([
      tr("Cible : ", { bold: true, color: C.navy700 }),
      tr("25–40 pages · Markdown + Pandoc + WeasyPrint · Auteur ", { color: C.inkSoft }),
      tr("Bachirou Konaté", { bold: true, color: C.navy900 }),
      tr(" (rédaction intégrale) · Contributions ", { color: C.inkSoft }),
      tr("Karamo", { bold: true, color: C.navy900 }),
      tr(" (captures dashboard, schémas, ADRs, données chiffrées).", { color: C.inkSoft }),
    ]),
  ];
}

// --- 11 — Dashboard 8 pages ---------------------------------------------------
function s11() {
  return [
    ...sectionTitle("11", "Dashboard", "Dashboard Next.js — 8 pages"),
    lead("Application Next.js 15 déployée sur Vercel. Dark mode par défaut (Navy 1000), cohérence McKinsey. Cible desktop prioritaire, public read-only en MVP."),
    dataTable({
      widths: [2100, 4500, 3146],
      headers: ["Route", "Contenu", "Lead"],
      rows: [
        ["/", "KPIs marché IA (Maroc + International) · top compétences", "Karamo"],
        ["/skills", "Tableau filtrable · score émergence · family · growth", "Karamo"],
        ["/graph", "Graphe Neo4j interactif (react-force-graph-2d) · Louvain", "Karamo (data : Bachirou Konaté)"],
        ["/forecasting", "ARIMA + Prophet + LSTM superposés · MAPE chiffré", "Karamo"],
        ["/ner-explorer", "Texte annoté side-by-side 3 modèles · badges confidence", "Karamo"],
        ["/methodology", "3 axes · sources · RGPD · glossaire", "Karamo (contenu : Bachirou Konaté)"],
        ["/comparative-study", "4 tableaux N2.1 – N2.4 chiffrés · choix justifiés", "Karamo"],
        ["/quality", "Complétude · bruit · biais (Data Quality Framework)", "Karamo (notebook : Bachirou Konaté)"],
      ],
    }),
  ];
}

// --- 12 — Repository structure -----------------------------------------------
function s12() {
  return [
    ...sectionTitle("12", "Repository", "Structure du repository"),
    lead("Un seul repo monolithique : pipeline IA (Python), front Next.js, notebooks Jupyter, données et documentation versionnée."),
    asciiBox(
`skillnav/
├── pyproject.toml
├── README.md
├── CLAUDE.md                      # consignes Claude Code
├── .env.example
│
├── docs/
│   ├── PRD.md                     # version exhaustive
│   ├── PRD_CONDENSE.md            # ce document
│   ├── CHARTE_GRAPHIQUE_SKILLNAV.{md,docx,pdf}
│   ├── RAPPORT_METHODOLOGIQUE.md  # L5 (Bachirou Konaté)
│   ├── PLAN_SOUTENANCE.md         # L6
│   ├── RGPD_DPIA.md
│   └── archive/                   # versions anciennes
│
├── skillnav/                      # package Python
│   ├── schemas/                   # Pydantic v2 — source de vérité
│   │   ├── job.py
│   │   ├── ner.py
│   │   ├── graph.py
│   │   ├── timeseries.py
│   │   └── converters/{mongo,neo4j,es}.py
│   ├── db/{mongodb,neo4j,elasticsearch}/
│   ├── pipelines/
│   │   ├── content_mining/        # NER + Pydantic AI
│   │   ├── structure_mining/      # Graph builder + algos
│   │   └── usage_mining/          # Time series + forecasting
│   ├── scrapers/{rekrute,emploitic,apify,indeed,builtin,weak_signals}/
│   ├── comparative_studies/
│   │   ├── ner.py
│   │   ├── communities.py
│   │   ├── forecasting.py
│   │   └── emerging.py
│   ├── api/                       # FastAPI endpoints
│   └── cli.py                     # commande "skillnav"
│
├── notebooks/
│   ├── 00_setup_dev.ipynb
│   ├── 01_data_quality.ipynb           (Bachirou Konaté)
│   ├── 02_ner_comparison.ipynb         (Karamo)
│   ├── 03_graph_analysis.ipynb         (Bachirou Konaté)
│   ├── 04_forecasting_comparison.ipynb (Karamo)
│   └── 05_dashboard_data_prep.ipynb    (Karamo)
│
├── web/                           # Next.js 15 (Karamo)
│   ├── package.json
│   └── src/
│       ├── app/                   # pages App router
│       ├── components/
│       └── lib/api/types.ts       # généré depuis OpenAPI
│
├── tests/
│   ├── fixtures/                  # 30 offres gold annotées
│   ├── unit/
│   └── integration/
│
├── data/
│   ├── raw/                       # JSONL (gitignored)
│   ├── gold_set/                  # annotations manuelles
│   ├── exports/                   # datasets publics anonymisés
│   └── audit/                     # logs RGPD
│
└── scripts/
    ├── build_charte_docx.mjs
    ├── build_prd_docx.mjs
    └── seed_taxonomy.py`,
      { size: 12 }
    ),
  ];
}

// --- 13 — Calendrier ----------------------------------------------------------
function s13() {
  return [
    ...sectionTitle("13", "Calendrier", "18 jours · 3 sprints · soutenance 28 mai"),
    lead("Trois sprints de 6 jours, avec répartition stricte par membre. Karamo possède le dashboard, Bachirou Konaté possède le rapport L5."),
    asciiBox(
`Sprint 1 — Fondations              J1 → J6   (10–16 mai)
Sprint 2 — Cœur Web Mining         J7 → J12  (17–22 mai)
Sprint 3 — Forecasting + Finition  J13 → J18 (23–28 mai)
SOUTENANCE                          J19       (28 mai 2026)`,
      { size: 14 }
    ),
    spacer(200),
    dataTable({
      widths: [1200, 4200, 4346],
      headers: ["Sprint", "Karamo focus", "Bachirou Konaté focus"],
      rows: [
        ["S1 J1–J6", "DBs · scrapers · schémas Pydantic · pipeline ingestion + extraction · dashboard skeleton + Vercel", "Charte PDF · notebook 01_data_quality · plan + chapitres 1–2 du rapport L5"],
        ["S2 J7–J12", "NER + tableau F1 · normalisation · pages /ner-explorer + /graph + /skills · dark mode", "Graph builder · PageRank · Louvain · Leiden · rédaction §N1 + N2.1 + N2.2 + N3 + N4 du L5"],
        ["S3 J13–J18", "Forecasting (ARIMA + Prophet + LSTM) · pages /forecasting + /comparative-study · polish · démo", "Rapport L5 final (PDF) · deck PPTX · répétitions"],
      ],
    }),
  ];
}

// --- 14 — Soutenance ----------------------------------------------------------
function s14() {
  return [
    ...sectionTitle("14", "Soutenance", "25 minutes · structure minute par minute"),
    lead("Quinze minutes de présentation (avec quatre minutes de démo live intégrées) puis dix minutes de Q&A. Karamo prend les douze premières minutes (architecture + démo + résultats), Bachirou Konaté les trois dernières (Data Quality, RGPD, conclusion)."),
    asciiBox(
`┌────────────────────────────────────────────────────────────────┐
│  15 min PRÉSENTATION  +  4 min DÉMO LIVE  +  10 min Q&A        │
└────────────────────────────────────────────────────────────────┘`,
      { size: 14 }
    ),
    spacer(200),
    dataTable({
      widths: [1100, 2400, 4500, 1746],
      headers: ["Min", "Section", "Contenu", "Lead"],
      rows: [
        [{ text: "M0–M1", center: true, bold: true, color: C.royal }, "Ouverture", "Titre, équipe, contexte M242", "Karamo"],
        [{ text: "M1–M2", center: true, bold: true, color: C.royal }, "Sujet + 3 axes", "Reformulation sujet + couverture 3 axes (§N1.2)", "Karamo"],
        [{ text: "M2–M4", center: true, bold: true, color: C.royal }, "Architecture", "Schéma global + justification 3 DBs (§7.0)", "Karamo"],
        [{ text: "M4–M5", center: true, bold: true, color: C.royal }, "Stack technique", "Tableau §14 condensé + 3 décisions clés (ADR)", "Karamo"],
        [{ text: "M5–M9", center: true, bold: true, color: C.royal }, "Démo live dashboard", "skillnav.vercel.app — /, /graph, /forecasting, /ner-explorer, /comparative-study", "Karamo"],
        [{ text: "M9–M12", center: true, bold: true, color: C.royal }, "Étude comparative", "4 tableaux chiffrés (N2.1 – N2.4)", "Karamo"],
        [{ text: "M12–M13", center: true, bold: true, color: C.royal }, "Data Quality", "Page /quality + transparence biais (§N3.5)", "Bachirou Konaté"],
        [{ text: "M13–M14", center: true, bold: true, color: C.royal }, "RGPD + robots.txt", "Base légale + protocole + DPIA disponible", "Bachirou Konaté"],
        [{ text: "M14–M15", center: true, bold: true, color: C.royal }, "Conclusion", "6 livrables remis + roadmap V1.5 / V2", "Bachirou Konaté"],
      ],
    }),
    spacer(160),
    p([
      tr("Plan B démo HS : ", { bold: true, color: C.warning }),
      tr("projeter web/screenshots/{page}.png (HD préparés) + verbaliser.", { color: C.inkSoft }),
    ]),
  ];
}

// --- 15 — Indicateurs --------------------------------------------------------
function s15() {
  return [
    ...sectionTitle("15", "Indicateurs", "Indicateurs de succès"),
    lead("Trois familles de KPIs : techniques (mesurables sur les notebooks et le pipeline), académiques (lus par le Pr. Sassi), et produit (qualité du dashboard)."),
    dataTable({
      widths: [1900, 5800, 2046],
      headers: ["Catégorie", "KPI", "Cible"],
      rows: [
        [{ text: "Technique", color: C.royal, bold: true }, "Volume offres collectées", "≥ 500 (idéal 2 000)"],
        [{ text: "Technique", color: C.royal, bold: true }, "F1 NER (gold set 30 offres)", "meilleur modèle ≥ 0.75"],
        [{ text: "Technique", color: C.royal, bold: true }, "MAPE forecasting top 10 skills", "≤ 15 %"],
        [{ text: "Technique", color: C.royal, bold: true }, "Modularité Louvain", "≥ 0.40"],
        [{ text: "Technique", color: C.royal, bold: true }, "Couverture tests", "≥ 70 % schemas/ + pipelines/"],
        [{ text: "Académique", color: C.success, bold: true }, "Couverture 3 axes", "≥ 25 % chacun"],
        [{ text: "Académique", color: C.success, bold: true }, "Algos comparés par tâche", "≥ 3"],
        [{ text: "Académique", color: C.success, bold: true }, "RGPD documenté", "DPIA séparée publiée"],
        [{ text: "Académique", color: C.success, bold: true }, "Livrables remis", "6 / 6"],
        [{ text: "Produit", color: C.warning, bold: true }, "Pages dashboard live", "≥ 7"],
        [{ text: "Produit", color: C.warning, bold: true }, "Chargement page", "< 3 s"],
        [{ text: "Produit", color: C.warning, bold: true }, "Dashboard accessible URL", "live à J17 + 3h (curl -I)"],
      ],
    }),
  ];
}

// --- 16 — Plans B ------------------------------------------------------------
function s16() {
  return [
    ...sectionTitle("16", "Plans B", "Plans B sprints sous tension"),
    lead("Six scénarios de dérapage anticipés, avec leur plan de repli explicite. Le but : ne jamais arriver à la soutenance avec un livrable manquant."),
    dataTable({
      widths: [1300, 3500, 4946],
      headers: ["Sprint", "Si dérapage", "Plan B"],
      rows: [
        [{ text: "S1", center: true, bold: true, color: C.warning }, "Pipeline complet pas prêt", "Scrape direct → MongoDB sans extraction IA. Notebook collecte stats brutes"],
        [{ text: "S2", center: true, bold: true, color: C.warning }, "Neo4j AuraDB instable", "Graphe NetworkX en mémoire + export GraphML. Démontre l'axe Structure"],
        [{ text: "S2", center: true, bold: true, color: C.warning }, "Elasticsearch coûte trop de temps", "MongoDB Atlas Search + $facet agrégations. ES = « évalué, plan B retenu »"],
        [{ text: "S3", center: true, bold: true, color: C.warning }, "LSTM bug", "ARIMA + Prophet seulement. Mention LSTM en « perspective »"],
        [{ text: "S3", center: true, bold: true, color: C.warning }, "Apify LinkedIn cassé", "Sources statiques (Rekrute + Indeed + builtin) à ≥ 800 offres"],
        [{ text: "J18", center: true, bold: true, color: C.error }, "Dashboard Vercel HS", "Screenshots HD préparés + démo locale pnpm dev projetée"],
      ],
    }),
  ];
}

// --- 17 — RACI ---------------------------------------------------------------
function s17() {
  return [
    ...sectionTitle("17", "RACI", "Répartition Karamo / Bachirou Konaté"),
    lead("Matrice RACI synthétique. R = Responsible · A = Accountable · C = Consulted · I = Informed."),
    asciiBox(
`R = Responsible · A = Accountable · C = Consulted · I = Informed`,
      { size: 14, color: C.muted }
    ),
    spacer(120),
    dataTable({
      widths: [5800, 1973, 1973],
      headers: ["Élément", "Karamo", "Bachirou Konaté"],
      rows: [
        ["§6 Architecture", { text: "A R", center: true, bold: true, color: C.royal }, { text: "R", center: true }],
        ["§6.B Pipeline IA", { text: "A R", center: true, bold: true, color: C.royal }, { text: "I", center: true, color: C.muted }],
        ["Structure Mining (Neo4j)", { text: "C", center: true, color: C.muted }, { text: "A R", center: true, bold: true, color: C.royal }],
        ["Notebook 01_data_quality", { text: "I", center: true, color: C.muted }, { text: "A R", center: true, bold: true, color: C.royal }],
        ["Notebook 02_ner_comparison", { text: "A R", center: true, bold: true, color: C.royal }, { text: "C", center: true }],
        ["Notebook 03_graph_analysis", { text: "C", center: true, color: C.muted }, { text: "A R", center: true, bold: true, color: C.royal }],
        ["Notebook 05_dashboard_data_prep", { text: "A R", center: true, bold: true, color: C.royal }, { text: "C", center: true }],
        ["Dashboard Next.js (L4)", { text: "A R", center: true, bold: true, color: C.royal }, { text: "C", center: true }],
        ["Rapport méthodologique (L5)", { text: "C", center: true, color: C.muted }, { text: "A R", center: true, bold: true, color: C.royal }],
        ["Charte graphique (PDF)", { text: "C", center: true, color: C.muted }, { text: "A R", center: true, bold: true, color: C.royal }],
        ["Deck soutenance", { text: "R", center: true }, { text: "A R", center: true, bold: true, color: C.royal }],
        ["RGPD + DPIA (§N4)", { text: "R", center: true }, { text: "A R", center: true, bold: true, color: C.royal }],
        ["Étude comparative (§N2)", { text: "A R", center: true, bold: true, color: C.royal }, { text: "R", center: true }],
      ],
    }),
    spacer(360),
    rule(C.royal, 12, 240),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 120, after: 60, line: 320 },
      children: [tr("Mai 2026 · Karamo Sylla & Bachirou Konaté · ENSA-Tétouan", {
        font: FONT_BODY, size: 18, color: C.muted, bold: true,
      })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 0, after: 0, line: 320 },
      children: [tr("Module M242 — Pr. Imad Sassi — Soutenance 28 mai 2026", {
        font: FONT_BODY, size: 16, color: C.mutedLight, italics: true,
      })],
    }),
  ];
}

// =============================================================================
// MAIN — assemble document
// =============================================================================
function buildDoc() {
  // Cover section (no header/footer/margin so the navy bleeds full)
  const coverSection = {
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H },
        margin: { top: 0, right: 0, bottom: 0, left: 0, header: 0, footer: 0, gutter: 0 },
      },
    },
    headers: {},
    footers: {},
    children: [coverPage(), new Paragraph({ children: [tr(" ", { size: 2, color: C.white })] })],
  };

  // Body sections — header + footer with page number
  const bodyHeader = new Header({
    children: [
      new Paragraph({
        spacing: { before: 0, after: 0, line: 240 },
        tabStops: [{ type: TabStopType.RIGHT, position: CONTENT_W }],
        children: [
          tr("SKILLNAV — PRD CONDENSÉ", { font: FONT_BODY, size: 16, color: C.muted, bold: true }),
          tr("\t", {}),
          tr("M242 · ENSA-Tétouan · Mai 2026", { font: FONT_BODY, size: 16, color: C.muted }),
        ],
      }),
      new Paragraph({
        spacing: { before: 60, after: 0, line: 200 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border, space: 1 } },
        children: [],
      }),
    ],
  });

  const bodyFooter = new Footer({
    children: [
      new Paragraph({
        spacing: { before: 60, after: 0, line: 240 },
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.border, space: 1 } },
        children: [],
      }),
      new Paragraph({
        spacing: { before: 100, after: 0, line: 240 },
        tabStops: [
          { type: TabStopType.CENTER, position: CONTENT_W / 2 },
          { type: TabStopType.RIGHT, position: CONTENT_W },
        ],
        children: [
          tr("Karamo Sylla & Bachirou Konaté", { font: FONT_BODY, size: 16, color: C.muted }),
          tr("\t", {}),
          tr("SKILLNAV — PRD CONDENSÉ", { font: FONT_BODY, size: 16, color: C.royal, bold: true }),
          tr("\t", {}),
          new TextRun({ children: ["Page ", PageNumber.CURRENT, " / ", PageNumber.TOTAL_PAGES],
            font: FONT_BODY, size: 16, color: C.muted }),
        ],
      }),
    ],
  });

  const bodyChildren = [
    ...tocBlock(),
    ...s01(),
    ...s02(),
    ...s03(),
    ...s04(),
    ...s05(),
    ...s06(),
    ...s07(),
    ...s08(),
    ...s09(),
    ...s10(),
    ...s11(),
    ...s12(),
    ...s13(),
    ...s14(),
    ...s15(),
    ...s16(),
    ...s17(),
  ];

  const bodySection = {
    properties: {
      page: {
        size: { width: PAGE_W, height: PAGE_H },
        margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN, header: 720, footer: 720 },
      },
    },
    headers: { default: bodyHeader },
    footers: { default: bodyFooter },
    children: bodyChildren,
  };

  return new Document({
    creator: "SKILLNAV — Karamo Sylla & Bachirou Konaté",
    title: "SKILLNAV — PRD condensé",
    description: "PRD condensé — Skills Navigator (M242 ENSA-Tétouan)",
    styles: {
      default: {
        document: { run: { font: FONT_BODY, size: 21, color: C.ink } },
      },
    },
    sections: [coverSection, bodySection],
  });
}

// --- Run ----------------------------------------------------------------------
mkdirSync(dirname(OUT_DOCX), { recursive: true });
console.log("[skillnav] Building PRD condensé DOCX (premium)...");
const doc = buildDoc();
const buf = await Packer.toBuffer(doc);
writeFileSync(OUT_DOCX, buf);
console.log(`[skillnav] Wrote ${OUT_DOCX}`);
