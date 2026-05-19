/* SKILLNAV — Données fictives pour le prototype hi-fi.
   Volumétries calées sur le brief : 42 318 offres, 1 847 skills,
   36 mois (Jan 2023 → Mai 2026) + 12 mois prévisionnels.
*/

export type FamilyKey =
  | "ml-classique"
  | "deep-learning"
  | "nlp"
  | "cv"
  | "data-eng"
  | "mlops"
  | "cloud"
  | "ai-ethics"
  | "stats"
  | "tools";

export interface FamilyDef {
  lbl: string;
  cls: string;
  short: string;
  color: string;
}

export const FAMILIES: Record<FamilyKey, FamilyDef> = {
  "ml-classique": { lbl: "ML classique", cls: "fpill-ml", short: "ML cl.", color: "#2251FF" },
  "deep-learning": { lbl: "Deep Learning", cls: "fpill-dl", short: "Deep L.", color: "#7C3AED" },
  nlp: { lbl: "NLP / LLM", cls: "fpill-nlp", short: "NLP", color: "#0891B2" },
  cv: { lbl: "Computer Vision", cls: "fpill-cv", short: "CV", color: "#C77700" },
  "data-eng": { lbl: "Data Engineering", cls: "fpill-data", short: "Data E.", color: "#1F4868" },
  mlops: { lbl: "MLOps", cls: "fpill-mlops", short: "MLOps", color: "#0F8F65" },
  cloud: { lbl: "Cloud / Big Data", cls: "fpill-cloud", short: "Cloud", color: "#1A3FCC" },
  "ai-ethics": { lbl: "AI Ethics", cls: "fpill-ethics", short: "Ethics", color: "#4A1D6E" },
  stats: { lbl: "Stats", cls: "fpill-stats", short: "Stats", color: "#5C7E2A" },
  tools: { lbl: "Outils", cls: "fpill-tools", short: "Tools", color: "#6B7280" },
};

function seededRandom(seed: number): () => number {
  let s = seed;
  return () => {
    s = (s * 9301 + 49297) % 233280;
    return s / 233280;
  };
}

export function trendSeries(seed: number, n: number, base = 50, slope = 0.5, vol = 5): number[] {
  const r = seededRandom(seed);
  const out: number[] = [];
  for (let i = 0; i < n; i++) {
    const v = base + slope * i + (r() - 0.5) * vol * 2;
    out.push(Math.max(0, v));
  }
  return out;
}

export interface TopSkill {
  rank: number;
  nm: string;
  fam: FamilyKey;
  score: number;
  delta: number;
  series: number[];
}

export const TOP_SKILLS: TopSkill[] = [
  { rank: 1, nm: "LLM Engineering", fam: "deep-learning", score: 0.94, delta: 47, series: trendSeries(11, 24, 35, 2.1, 4) },
  { rank: 2, nm: "RAG · Vector DB", fam: "nlp", score: 0.91, delta: 38, series: trendSeries(12, 24, 30, 1.8, 3) },
  { rank: 3, nm: "LangChain", fam: "nlp", score: 0.88, delta: 29, series: trendSeries(13, 24, 28, 1.5, 3) },
  { rank: 4, nm: "Fine-tuning (LoRA)", fam: "deep-learning", score: 0.87, delta: 22, series: trendSeries(14, 24, 25, 1.2, 3) },
  { rank: 5, nm: "MLOps · MLflow", fam: "mlops", score: 0.84, delta: 19, series: trendSeries(15, 24, 40, 1.0, 4) },
  { rank: 6, nm: "Prompt Engineering", fam: "nlp", score: 0.82, delta: 18, series: trendSeries(16, 24, 22, 1.1, 3) },
  { rank: 7, nm: "Pydantic AI", fam: "tools", score: 0.79, delta: 14, series: trendSeries(17, 24, 18, 0.8, 3) },
  { rank: 8, nm: "CrewAI / Agents", fam: "deep-learning", score: 0.77, delta: 12, series: trendSeries(18, 24, 16, 0.7, 3) },
];

export interface CatalogRow {
  idx: number;
  nm: string;
  fam: FamilyKey;
  volume: number;
  score: number;
  conf: number;
  series: number[];
}

export const CATALOG: CatalogRow[] = [
  { idx: 1, nm: "LLM Engineering", fam: "deep-learning", volume: 3240, score: 0.94, conf: 0.93, series: trendSeries(21, 18, 35, 2.2, 4) },
  { idx: 2, nm: "RAG / Vector DB", fam: "nlp", volume: 2815, score: 0.91, conf: 0.89, series: trendSeries(22, 18, 30, 1.9, 3) },
  { idx: 3, nm: "LangChain", fam: "nlp", volume: 2102, score: 0.88, conf: 0.86, series: trendSeries(23, 18, 26, 1.6, 3) },
  { idx: 4, nm: "Fine-tuning LoRA", fam: "deep-learning", volume: 1932, score: 0.87, conf: 0.84, series: trendSeries(24, 18, 24, 1.3, 3) },
  { idx: 5, nm: "MLflow", fam: "mlops", volume: 1718, score: 0.84, conf: 0.88, series: trendSeries(25, 18, 32, 1.1, 3) },
  { idx: 6, nm: "Prompt Eng.", fam: "nlp", volume: 1605, score: 0.82, conf: 0.80, series: trendSeries(26, 18, 22, 1.1, 3) },
  { idx: 7, nm: "Pydantic AI", fam: "tools", volume: 1421, score: 0.79, conf: 0.74, series: trendSeries(27, 18, 18, 0.9, 3) },
  { idx: 8, nm: "dbt", fam: "data-eng", volume: 1318, score: 0.77, conf: 0.83, series: trendSeries(28, 18, 28, 0.8, 3) },
  { idx: 9, nm: "Vector embeddings", fam: "ml-classique", volume: 1240, score: 0.74, conf: 0.81, series: trendSeries(29, 18, 22, 0.7, 3) },
  { idx: 10, nm: "LlamaIndex", fam: "nlp", volume: 1098, score: 0.71, conf: 0.78, series: trendSeries(30, 18, 18, 0.8, 3) },
  { idx: 11, nm: "Kubernetes", fam: "cloud", volume: 2020, score: 0.64, conf: 0.85, series: trendSeries(31, 18, 38, 0.4, 4) },
  { idx: 12, nm: "Apache Spark", fam: "data-eng", volume: 2410, score: 0.66, conf: 0.91, series: trendSeries(32, 18, 42, 0.3, 4) },
];

function totalsSeries(): { m: number; v: number }[] {
  const r = seededRandom(99);
  const months = 48;
  const out: { m: number; v: number }[] = [];
  for (let i = 0; i < months; i++) {
    const base = 800 + 12 * i;
    out.push({ m: i, v: Math.round(base + (r() - 0.5) * 80) });
  }
  return out;
}
export const TOTAL_OFFERS_SERIES = totalsSeries();

function famSeries(seed: number, base: number, slope: number, n = 48): number[] {
  const r = seededRandom(seed);
  const out: number[] = [];
  for (let i = 0; i < n; i++) {
    out.push(Math.max(0, base + slope * i + (r() - 0.5) * (base * 0.18)));
  }
  return out;
}

export interface FamilySeries {
  fam: FamilyKey;
  series: number[];
  name?: string;
}

export const DOMINANT_FAMILIES: FamilySeries[] = [
  { fam: "nlp", series: famSeries(41, 80, 4.0) },
  { fam: "deep-learning", series: famSeries(42, 60, 3.2) },
  { fam: "mlops", series: famSeries(43, 50, 2.4) },
];

export const DECLINING_FAMILIES: FamilySeries[] = [
  { fam: "tools", series: famSeries(44, 90, -0.8), name: "jQuery / vanilla" },
  { fam: "data-eng", series: famSeries(45, 70, -0.4), name: "Hadoop" },
  { fam: "ml-classique", series: famSeries(46, 55, -0.3), name: "XGBoost (relatif)" },
];

export interface ForecastModel {
  key: "arima" | "prophet" | "lstm";
  name: string;
  badge: string;
  params: Record<string, string | number>;
  metrics: { mape: number; rmse: number; mae: number; r2: number };
  justification: string;
  retained: boolean;
  series: number[];
  forecast: number[];
}

export const FORECAST_MODELS: ForecastModel[] = [
  {
    key: "arima",
    name: "ARIMA",
    badge: "Statistique",
    params: { p: 2, d: 1, q: 2, seasonal: "(0,1,1,12)" },
    metrics: { mape: 12.4, rmse: 47.8, mae: 38.2, r2: 0.84 },
    justification: "Référence — capture la saisonnalité mais sous-estime le shift LLM 2024.",
    retained: false,
    series: famSeries(51, 80, 4.5, 36),
    forecast: famSeries(52, 250, 1.2, 12),
  },
  {
    key: "prophet",
    name: "Prophet",
    badge: "Décomposition",
    params: { changepoint: 0.08, seasonality: "auto", holidays: "FR + MA" },
    metrics: { mape: 9.7, rmse: 38.1, mae: 30.4, r2: 0.89 },
    justification: "Robuste sur les ruptures — manque de réactivité en sortie de plateau.",
    retained: false,
    series: famSeries(53, 80, 4.5, 36),
    forecast: famSeries(54, 280, 2.4, 12),
  },
  {
    key: "lstm",
    name: "LSTM",
    badge: "Réseau récurrent",
    params: { layers: 2, units: 64, dropout: 0.2, lookback: 18, optimizer: "adam" },
    metrics: { mape: 6.7, rmse: 24.3, mae: 19.6, r2: 0.94 },
    justification: "Modèle retenu — meilleur MAPE et capture la non-linéarité LLM.",
    retained: true,
    series: famSeries(55, 80, 4.5, 36),
    forecast: famSeries(56, 305, 4.1, 12),
  },
];

export interface Community {
  id: string;
  nm: string;
  size: number;
  fam: FamilyKey;
  active?: boolean;
}

export const COMMUNITIES: Community[] = [
  { id: "C1", nm: "LLM & RAG", size: 38, fam: "deep-learning", active: true },
  { id: "C2", nm: "Data Eng.", size: 32, fam: "data-eng" },
  { id: "C3", nm: "MLOps / Cloud", size: 28, fam: "mlops" },
  { id: "C4", nm: "ML classique", size: 24, fam: "ml-classique" },
  { id: "C5", nm: "Computer Vision", size: 19, fam: "cv" },
  { id: "C6", nm: "Stats & Math", size: 14, fam: "stats" },
  { id: "C7", nm: "AI Ethics", size: 8, fam: "ai-ethics" },
];

export interface DivergingRow {
  fam: FamilyKey;
  lbl: string;
  ma: number;
  in_: number;
}

export const DIVERGING: DivergingRow[] = [
  { fam: "nlp", lbl: "NLP / LLM", ma: 18, in_: 28 },
  { fam: "deep-learning", lbl: "Deep Learning", ma: 14, in_: 24 },
  { fam: "mlops", lbl: "MLOps", ma: 11, in_: 19 },
  { fam: "data-eng", lbl: "Data Engineering", ma: 21, in_: 14 },
  { fam: "ml-classique", lbl: "ML classique", ma: 18, in_: 10 },
  { fam: "cloud", lbl: "Cloud / Big Data", ma: 10, in_: 12 },
  { fam: "cv", lbl: "Computer Vision", ma: 6, in_: 9 },
  { fam: "stats", lbl: "Stats", ma: 8, in_: 6 },
  { fam: "ai-ethics", lbl: "AI Ethics", ma: 2, in_: 6 },
  { fam: "tools", lbl: "Outils", ma: 6, in_: 4 },
];

export const CONF_CLASSES = ["SKILL", "TOOL", "FIELD", "LOC", "J.LEV", "SAL", "CONT"] as const;
export const CONF_MATRIX: number[][] = [
  [89, 7, 7, 7, 7, 7, 7],
  [7, 97, 1, 6, 6, 0, 6],
  [7, 1, 91, 6, 1, 7, 5],
  [7, 6, 6, 96, 5, 4, 3],
  [7, 6, 1, 5, 93, 4, 1],
  [1, 4, 3, 6, 5, 95, 3],
  [5, 3, 4, 3, 2, 4, 92],
];

export interface PerClassRow {
  cls: string;
  n: number;
  prec: number;
  rec: number;
  f1: number;
}

export const PERCLASS: PerClassRow[] = [
  { cls: "SKILL", n: 8412, prec: 0.94, rec: 0.92, f1: 0.93 },
  { cls: "TOOL", n: 6218, prec: 0.91, rec: 0.89, f1: 0.90 },
  { cls: "FIELD", n: 2102, prec: 0.93, rec: 0.91, f1: 0.92 },
  { cls: "LOC", n: 3014, prec: 0.95, rec: 0.93, f1: 0.94 },
  { cls: "JOB_LEVEL", n: 1482, prec: 0.88, rec: 0.85, f1: 0.86 },
  { cls: "SALARY", n: 612, prec: 0.84, rec: 0.78, f1: 0.81 },
  { cls: "CONTRACT", n: 418, prec: 0.92, rec: 0.88, f1: 0.90 },
];

export interface GapCoverage {
  fam: FamilyKey;
  lbl: string;
  marche: number;
  ensa: number;
  delta: number;
}

export const GAP_COVERAGE: GapCoverage[] = [
  { fam: "nlp", lbl: "NLP / LLM", marche: 92, ensa: 42, delta: -50 },
  { fam: "deep-learning", lbl: "Deep Learning", marche: 89, ensa: 68, delta: -21 },
  { fam: "mlops", lbl: "MLOps", marche: 81, ensa: 34, delta: -47 },
  { fam: "cloud", lbl: "Cloud / Big Data", marche: 78, ensa: 58, delta: -20 },
  { fam: "data-eng", lbl: "Data Engineering", marche: 84, ensa: 71, delta: -13 },
  { fam: "ai-ethics", lbl: "AI Ethics", marche: 42, ensa: 18, delta: -24 },
  { fam: "ml-classique", lbl: "ML classique", marche: 75, ensa: 92, delta: 17 },
  { fam: "cv", lbl: "Computer Vision", marche: 62, ensa: 78, delta: 16 },
  { fam: "stats", lbl: "Stats", marche: 58, ensa: 95, delta: 37 },
  { fam: "tools", lbl: "Outils", marche: 48, ensa: 62, delta: 14 },
];

export interface GapLack {
  rank: number;
  nm: string;
  fam: FamilyKey;
  score: number;
  schools: string;
}

export const GAP_TOP_LACKS: GapLack[] = [
  { rank: 1, nm: "LLM Engineering", fam: "deep-learning", score: 0.94, schools: "0 / 8" },
  { rank: 2, nm: "RAG / Vector DB", fam: "nlp", score: 0.91, schools: "0 / 8" },
  { rank: 3, nm: "LangChain", fam: "nlp", score: 0.88, schools: "1 / 8" },
  { rank: 4, nm: "LoRA / PEFT", fam: "deep-learning", score: 0.87, schools: "0 / 8" },
  { rank: 5, nm: "MLflow", fam: "mlops", score: 0.84, schools: "2 / 8" },
  { rank: 6, nm: "Prompt Engineering", fam: "nlp", score: 0.82, schools: "0 / 8" },
];

export interface GapSchool {
  nm: string;
  fil: number;
  cov: number;
}

export const GAP_SCHOOLS: GapSchool[] = [
  { nm: "ENSA Tétouan", fil: 2, cov: 0.71 },
  { nm: "ENSA Marrakech", fil: 2, cov: 0.68 },
  { nm: "ENSA Tanger", fil: 2, cov: 0.62 },
  { nm: "ENSA Agadir", fil: 2, cov: 0.58 },
  { nm: "ENSA Khouribga", fil: 1, cov: 0.54 },
  { nm: "ENSA Al Hoceima", fil: 1, cov: 0.51 },
  { nm: "ENSA Oujda", fil: 1, cov: 0.49 },
  { nm: "ENSA Safi", fil: 1, cov: 0.46 },
];

export type NerEntityType = "SKILL" | "TOOL" | "FIELD" | "LOC" | "JOB_LEVEL" | "SALARY" | "CONTRACT";

export interface NerToken {
  text: string;
  type: NerEntityType;
  conf: number;
}

export interface NerOffer {
  source: string;
  date: string;
  id: string;
  tokens: (string | NerToken)[];
}

export const NER_OFFER: NerOffer = {
  source: "LinkedIn",
  date: "12/05/2026",
  id: "LI-2026-04-2841",
  tokens: [
    "Nous recherchons un ",
    { text: "Data Scientist Senior", type: "JOB_LEVEL", conf: 0.96 },
    " basé à ",
    { text: "Casablanca", type: "LOC", conf: 0.98 },
    " ou en remote depuis le ",
    { text: "Maroc", type: "LOC", conf: 0.97 },
    ". Vous maîtrisez le ",
    { text: "Python", type: "TOOL", conf: 0.99 },
    " et le ",
    { text: "SQL", type: "TOOL", conf: 0.97 },
    " ainsi que les frameworks ",
    { text: "PyTorch", type: "TOOL", conf: 0.95 },
    " et ",
    { text: "TensorFlow", type: "TOOL", conf: 0.94 },
    ". Une expérience en ",
    { text: "LLM Engineering", type: "SKILL", conf: 0.92 },
    ", ",
    { text: "RAG", type: "SKILL", conf: 0.89 },
    " et ",
    { text: "fine-tuning", type: "SKILL", conf: 0.91 },
    " sur des modèles transformeurs est indispensable. Vous interviendrez sur des sujets de ",
    { text: "NLP", type: "FIELD", conf: 0.95 },
    " et de ",
    { text: "vision par ordinateur", type: "FIELD", conf: 0.88 },
    ". Salaire ",
    { text: "18 000 — 24 000 MAD", type: "SALARY", conf: 0.94 },
    " · contrat ",
    { text: "CDI", type: "CONTRACT", conf: 0.99 },
    ".",
  ],
};

export const NER_ENTITY_COLORS: Record<NerEntityType, string> = {
  SKILL: "#2251FF",
  TOOL: "#0F8F65",
  FIELD: "#7C3AED",
  LOC: "#C77700",
  JOB_LEVEL: "#0891B2",
  SALARY: "#B42318",
  CONTRACT: "#4A1D6E",
};

export interface GraphNode {
  x: number;
  y: number;
  fam: FamilyKey;
  size: number;
}
export interface GraphEdge {
  s: number;
  t: number;
  w: number;
}

function makeGraphNodes(): GraphNode[] {
  const r = seededRandom(7);
  const nodes: GraphNode[] = [];
  const centers: { x: number; y: number; fam: FamilyKey }[] = [
    { x: 250, y: 220, fam: "nlp" },
    { x: 380, y: 320, fam: "deep-learning" },
    { x: 520, y: 260, fam: "mlops" },
    { x: 470, y: 420, fam: "data-eng" },
    { x: 620, y: 380, fam: "cloud" },
    { x: 300, y: 420, fam: "ml-classique" },
    { x: 660, y: 200, fam: "cv" },
    { x: 170, y: 350, fam: "stats" },
    { x: 700, y: 480, fam: "ai-ethics" },
    { x: 220, y: 480, fam: "tools" },
  ];
  for (const ct of centers) {
    const cnt = 8 + Math.floor(r() * 4);
    for (let i = 0; i < cnt; i++) {
      const ang = r() * Math.PI * 2;
      const rad = 22 + r() * 60;
      nodes.push({
        x: ct.x + Math.cos(ang) * rad,
        y: ct.y + Math.sin(ang) * rad,
        fam: ct.fam,
        size: 3 + r() * 9,
      });
    }
  }
  return nodes;
}

export const GRAPH_NODES = makeGraphNodes();

function makeGraphEdges(nodes: GraphNode[]): GraphEdge[] {
  const r = seededRandom(8);
  const out: GraphEdge[] = [];
  for (let i = 0; i < nodes.length; i++) {
    for (let j = i + 1; j < nodes.length; j++) {
      const a = nodes[i]!;
      const b = nodes[j]!;
      const dx = a.x - b.x;
      const dy = a.y - b.y;
      const d = Math.sqrt(dx * dx + dy * dy);
      if (d < 80 && r() < 0.45) {
        out.push({ s: i, t: j, w: 1 - d / 80 });
      }
    }
  }
  return out;
}
export const GRAPH_EDGES = makeGraphEdges(GRAPH_NODES);

export interface Neighbor {
  nm: string;
  fam: FamilyKey;
  w: number;
}

export const NEIGHBORS: Neighbor[] = [
  { nm: "RAG", fam: "nlp", w: 0.78 },
  { nm: "Vector DB", fam: "nlp", w: 0.71 },
  { nm: "LangChain", fam: "nlp", w: 0.69 },
  { nm: "Fine-tuning", fam: "deep-learning", w: 0.63 },
  { nm: "Prompt Eng.", fam: "nlp", w: 0.61 },
  { nm: "LlamaIndex", fam: "nlp", w: 0.54 },
  { nm: "MLflow", fam: "mlops", w: 0.52 },
  { nm: "Pinecone", fam: "tools", w: 0.51 },
];

export interface ScatterPoint {
  x: number;
  y: number;
  fam: FamilyKey;
  size: number;
  hi: boolean;
}

function scatterPoints(): ScatterPoint[] {
  const r = seededRandom(73);
  const pts: ScatterPoint[] = [];
  const families: FamilyKey[] = [
    "nlp",
    "deep-learning",
    "mlops",
    "data-eng",
    "ml-classique",
    "cv",
    "cloud",
    "stats",
    "tools",
    "ai-ethics",
  ];
  for (let i = 0; i < 70; i++) {
    const fam = families[Math.floor(r() * families.length)]!;
    const x = r();
    const y = r() * 0.5 + 0.35;
    pts.push({ x, y, fam, size: 4 + r() * 8, hi: i < 5 });
  }
  return pts;
}
export const SCATTER = scatterPoints();

export interface TopGap {
  nm: string;
  ma: number;
  in_: number;
  delta: number;
}

export const TOP_GAPS: TopGap[] = [
  { nm: "LLM Engineering", ma: 2.1, in_: 9.8, delta: 7.7 },
  { nm: "RAG / Vector DB", ma: 1.4, in_: 7.2, delta: 5.8 },
  { nm: "MLflow", ma: 1.8, in_: 6.9, delta: 5.1 },
  { nm: "LangChain", ma: 0.9, in_: 5.8, delta: 4.9 },
  { nm: "Vector DB", ma: 0.8, in_: 4.6, delta: 3.8 },
];

export const METHO_TOC = [
  { num: 1, lbl: "Collecte" },
  { num: 2, lbl: "Normalisation" },
  { num: 3, lbl: "Content — NER" },
  { num: 4, lbl: "Structure — Graphe" },
  { num: 5, lbl: "Usage — Forecasting" },
  { num: 6, lbl: "Évaluation" },
  { num: 7, lbl: "Limites" },
  { num: 8, lbl: "Reproductibilité" },
  { num: 9, lbl: "Bibliographie" },
] as const;
