"use client";

import { useMemo, useState } from "react";
import { ChevronDown, ChevronUp, Search } from "lucide-react";
import { CheckRow, KPICard, Segmented } from "@/components/atoms";
import { SkillFamilyCard } from "@/components/SkillFamilyCard";
import dataset from "@/lib/skills_distribution.json";

type Origine = "Maroc" | "International" | "Tous";

type FamilleKey =
  | "genai"
  | "ml"
  | "web"
  | "databases"
  | "data"
  | "cloud"
  | "ops"
  | "languages"
  | "domains"
  | "other";

interface CatalogueRow {
  skill: string;
  count: number;
  family: FamilleKey;
  share_pct: number;
  series: number[];
  score: number;
}

interface DominantStat {
  code: string;
  label: string;
  count: number;
  pct: number;
}

interface Dataset {
  meta: {
    n_total: number;
    n_maroc: number;
    n_international: number;
    generated_at: string;
    method: string;
    sparkline_months: string[];
    periode: Record<Origine, { debut: string; fin: string; n_mois: string }>;
    type_poste_dominant: Record<Origine, DominantStat>;
    metier_dominant: Record<Origine, DominantStat>;
  };
  familles: Record<FamilleKey, string>;
  family_counts: Record<Origine, Record<FamilleKey, number>>;
  source_counts: Record<Origine, Record<string, number>>;
  top_par_famille: Record<Origine, Record<FamilleKey, { skill: string; count: number }[]>>;
  catalogue: Record<Origine, CatalogueRow[]>;
  insights: { title: string; body: string }[];
}

const DATA = dataset as unknown as Dataset;

const FAMILY_ORDER: FamilleKey[] = [
  "genai",
  "ml",
  "web",
  "databases",
  "data",
  "cloud",
  "ops",
  "languages",
  "domains",
  "other",
];

const FAMILY_COLOR: Record<FamilleKey, string> = {
  genai: "#7C3AED",
  ml: "#2251FF",
  web: "#0891B2",
  databases: "#1F4868",
  data: "#1A3FCC",
  cloud: "#0F8F65",
  ops: "#C77700",
  languages: "#6B7280",
  domains: "#4A1D6E",
  other: "#5C7E2A",
};

function RealFamilyPill({ famille, dense = false }: { famille: FamilleKey; dense?: boolean }) {
  const color = FAMILY_COLOR[famille];
  const label = DATA.familles[famille];
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        height: dense ? 22 : 26,
        padding: dense ? "0 10px" : "0 12px",
        border: `1.5px solid ${color}`,
        borderRadius: 9999,
        color,
        fontFamily: "var(--sans-body)",
        fontSize: dense ? 11 : 12,
        fontWeight: 500,
        whiteSpace: "nowrap",
      }}
    >
      <span style={{ width: 7, height: 7, borderRadius: "50%", background: color }} />
      {label}
    </span>
  );
}

function formatFR(n: number): string {
  return n.toLocaleString("fr-FR").replace(/ /g, " ");
}

const SOURCE_LABELS: Record<string, string> = {
  "intl-ai-corpus": "LinkedIn International",
  "linkedin-ma": "LinkedIn Maroc",
  "glassdoor-ma": "Glassdoor Maroc",
  "indeed-ma": "Indeed Maroc",
  "rekrute": "Rekrute",
  "pages-carrieres-ma": "Pages carrières (MA)",
  "anapec": "ANAPEC",
};

function sourceLabel(key: string): string {
  return SOURCE_LABELS[key] ?? key;
}

const PAGE_SIZE = 12;

export default function SkillsPage() {
  const [origine, setOrigine] = useState<Origine>("Maroc");
  const [page, setPage] = useState(1);
  const [familleActive, setFamilleActive] = useState<Record<FamilleKey, boolean>>(
    () => Object.fromEntries(FAMILY_ORDER.map((f) => [f, true])) as Record<FamilleKey, boolean>,
  );
  const [query, setQuery] = useState("");
  const [showFigures, setShowFigures] = useState(false);

  const familyCounts = DATA.family_counts[origine];
  const sourceCounts = DATA.source_counts[origine];
  const catalogueComplet = DATA.catalogue[origine];
  const sources = Object.keys(sourceCounts);

  const n_origine =
    origine === "Maroc"
      ? DATA.meta.n_maroc
      : origine === "International"
        ? DATA.meta.n_international
        : DATA.meta.n_total;

  const catalogueFiltre = useMemo(() => {
    const q = query.trim().toLowerCase();
    return catalogueComplet
      .filter((r) => familleActive[r.family] && (q === "" || r.skill.toLowerCase().includes(q)))
      .sort((a, b) => b.count - a.count);
  }, [catalogueComplet, familleActive, query]);

  const totalPages = Math.max(1, Math.ceil(catalogueFiltre.length / PAGE_SIZE));
  const pageNorm = Math.min(page, totalPages);
  const visibleRows = catalogueFiltre.slice((pageNorm - 1) * PAGE_SIZE, pageNorm * PAGE_SIZE);

  const top1Global = catalogueComplet[0];

  const metierDom = DATA.meta.metier_dominant[origine];

  const sourcePrincipale = sources[0] ?? "";

  const activeFamiliesCount = FAMILY_ORDER.filter((f) => familleActive[f]).length;

  const toggleFamille = (f: FamilleKey) => {
    setFamilleActive((s) => ({ ...s, [f]: !s[f] }));
    setPage(1);
  };

  return (
    <>
      <div className="row-split" style={{ marginTop: 8 }}>
        {/* Filter panel */}
        <aside className="filter-panel">
          <div className="filter-search">
            <Search size={14} strokeWidth={1.5} />
            <span>Filtres</span>
          </div>

          <div className="filter-block">
            <div className="filter-head">
              <span>Familles de compétences</span>
              <span>
                {activeFamiliesCount} / {FAMILY_ORDER.length}
              </span>
            </div>
            {FAMILY_ORDER.map((f) => (
              <CheckRow
                key={f}
                label={DATA.familles[f]}
                count={formatFR(familyCounts[f])}
                on={!!familleActive[f]}
                onToggle={() => toggleFamille(f)}
              />
            ))}
          </div>

          <div className="filter-block">
            <div className="filter-head">
              <span>Géographie</span>
            </div>
            <Segmented<Origine>
              options={[
                { value: "Maroc", label: "Maroc" },
                { value: "International", label: "International" },
                { value: "Tous", label: "Tous" },
              ]}
              value={origine}
              onChange={(v) => {
                setOrigine(v);
                setPage(1);
              }}
            />
          </div>

          <div className="filter-block">
            <div className="filter-head">
              <span>Période</span>
              <span>{DATA.meta.periode[origine].n_mois} mois</span>
            </div>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: 6,
                fontFamily: "var(--mono)",
                fontSize: 12,
                color: "var(--fg2)",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--fg3)" }}>début</span>
                <span>{DATA.meta.periode[origine].debut}</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <span style={{ color: "var(--fg3)" }}>fin</span>
                <span>{DATA.meta.periode[origine].fin}</span>
              </div>
            </div>
          </div>

          <div className="filter-block">
            <div className="filter-head">
              <span>Sources</span>
              <span>{sources.length}</span>
            </div>
            {sources.map((s) => {
              const cnt = sourceCounts[s] ?? 0;
              const pct = n_origine > 0 ? (cnt / n_origine) * 100 : 0;
              return (
                <div
                  key={s}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                    fontSize: 13,
                    padding: "5px 0",
                    gap: 8,
                  }}
                >
                  <span
                    style={{
                      display: "inline-flex",
                      alignItems: "center",
                      gap: 8,
                      overflow: "hidden",
                      textOverflow: "ellipsis",
                      whiteSpace: "nowrap",
                    }}
                  >
                    <span
                      style={{
                        width: 8,
                        height: 8,
                        borderRadius: "50%",
                        background: "var(--hl)",
                        flexShrink: 0,
                      }}
                    />
                    <span style={{ overflow: "hidden", textOverflow: "ellipsis" }} title={s}>
                      {sourceLabel(s)}
                    </span>
                  </span>
                  <span
                    className="mono"
                    style={{
                      fontSize: 11.5,
                      color: "var(--fg2)",
                      flexShrink: 0,
                      whiteSpace: "nowrap",
                    }}
                  >
                    {formatFR(cnt)}{" "}
                    <span style={{ color: "var(--fg3)" }}>· {pct.toFixed(0)}%</span>
                  </span>
                </div>
              );
            })}
          </div>
        </aside>

        {/* Main column */}
        <div style={{ flex: 1, minWidth: 0, display: "flex", flexDirection: "column", gap: 24 }}>
          <div className="kpi-grid" style={{ marginTop: 0 }}>
            <KPICard
              eyebrow="Offres analysées"
              value={formatFR(n_origine)}
              size="md"
              foot={<span>· {origine}</span>}
            />
            <KPICard
              eyebrow="Compétence #1"
              value={top1Global ? top1Global.skill : "—"}
              size="sm"
              accent
              foot={
                top1Global ? (
                  <span>
                    {formatFR(top1Global.count)} mentions ·{" "}
                    {top1Global.share_pct.toFixed(1).replace(".", ",")} % du corpus
                  </span>
                ) : null
              }
            />
            <KPICard
              eyebrow="Métier dominant"
              value={metierDom.label}
              size="sm"
              foot={
                <span>
                  {formatFR(metierDom.count)} offres ·{" "}
                  {metierDom.pct.toFixed(1).replace(".", ",")} % du corpus
                </span>
              }
            />
            <KPICard
              eyebrow="Sources de collecte"
              value={formatFR(sources.length)}
              size="md"
              foot={
                sourcePrincipale ? (
                  <span>principale · {sourceLabel(sourcePrincipale)}</span>
                ) : null
              }
            />
          </div>

          <div className="tbl-shell">
            <div className="tbl-toolbar">
              <span className="tbl-search">
                <Search size={14} strokeWidth={1.5} />
                <input
                  placeholder="Rechercher : LLM, RAG, SQL, Python…"
                  value={query}
                  onChange={(e) => {
                    setQuery(e.target.value);
                    setPage(1);
                  }}
                />
              </span>
            </div>

            <table className="tbl">
              <thead>
                <tr>
                  <th>#</th>
                  <th>Compétence</th>
                  <th>Famille</th>
                  <th className="num">Volume</th>
                </tr>
              </thead>
              <tbody>
                {visibleRows.length === 0 ? (
                  <tr>
                    <td colSpan={4} style={{ textAlign: "center", padding: 32, color: "var(--fg3)" }}>
                      Aucun résultat — élargir la recherche, cocher d&apos;autres familles ou changer
                      d&apos;origine.
                    </td>
                  </tr>
                ) : (
                  visibleRows.map((r, idx) => {
                    const rank = (pageNorm - 1) * PAGE_SIZE + idx + 1;
                    return (
                      <tr key={r.skill}>
                        <td className="idx mono">{String(rank).padStart(2, "0")}</td>
                        <td className="name">{r.skill}</td>
                        <td>
                          <RealFamilyPill famille={r.family} dense />
                        </td>
                        <td className="num">{formatFR(r.count)}</td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>

            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                marginTop: 18,
                fontFamily: "var(--mono)",
                fontSize: 12,
                color: "var(--fg3)",
              }}
            >
              <span>
                {visibleRows.length === 0
                  ? "0 — 0"
                  : `${(pageNorm - 1) * PAGE_SIZE + 1} — ${(pageNorm - 1) * PAGE_SIZE + visibleRows.length}`}{" "}
                sur {formatFR(catalogueFiltre.length)} résultats
              </span>
              <div style={{ display: "flex", gap: 6 }}>
                <button
                  className="btn sm"
                  disabled={pageNorm === 1}
                  onClick={() => setPage((p) => Math.max(1, p - 1))}
                >
                  ← préc.
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((n) => (
                  <button
                    key={n}
                    className="btn sm"
                    onClick={() => setPage(n)}
                    style={
                      n === pageNorm
                        ? {
                            background: "var(--hl)",
                            color: "var(--fg-on-accent)",
                            borderStyle: "solid",
                            borderColor: "var(--hl)",
                          }
                        : undefined
                    }
                  >
                    {n}
                  </button>
                ))}
                <button
                  className="btn sm"
                  disabled={pageNorm === totalPages}
                  onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                >
                  suiv. →
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <section
        style={{
          marginTop: 56,
          borderTop: "1px dashed var(--line-dashed)",
          paddingTop: 32,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "flex-end",
            justifyContent: "space-between",
            gap: 16,
            marginBottom: showFigures ? 28 : 0,
          }}
        >
          <div>
            <div className="eyebrow">Cartographie comparée</div>
            <h2
              style={{
                fontFamily: "var(--serif-display)",
                fontSize: 22,
                fontWeight: 600,
                fontVariationSettings: '"opsz" 36',
                letterSpacing: "-0.005em",
                lineHeight: 1.2,
                marginTop: 4,
              }}
            >
              Top 8 compétences par famille
            </h2>
            <div
              className="mono muted"
              style={{ fontSize: 11.5, marginTop: 6, color: "var(--fg3)" }}
            >
              10 familles · Maroc ↔ International · ordre décroissant
            </div>
          </div>
          <button
            className="btn sm"
            onClick={() => setShowFigures((s) => !s)}
            aria-expanded={showFigures}
            aria-controls="figures-reference-panel"
          >
            {showFigures ? (
              <ChevronUp size={14} strokeWidth={1.5} />
            ) : (
              <ChevronDown size={14} strokeWidth={1.5} />
            )}
            {showFigures ? "Masquer" : "Afficher"}
          </button>
        </div>

        {showFigures ? (
          <div
            id="figures-reference-panel"
            style={{ display: "flex", flexDirection: "column", gap: 16 }}
          >
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "1fr 1fr",
                gap: 24,
                marginBottom: 4,
              }}
            >
              <div
                style={{
                  fontFamily: "var(--sans-body)",
                  fontSize: 13,
                  color: "var(--fg1)",
                  fontWeight: 600,
                  borderBottom: "2px solid #2251FF",
                  paddingBottom: 8,
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "baseline",
                  letterSpacing: "0.02em",
                }}
              >
                <span style={{ color: "#2251FF", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                  Maroc
                </span>
                <span className="mono tabular" style={{ color: "var(--fg3)", fontSize: 11.5 }}>
                  n = {formatFR(DATA.meta.n_maroc)}
                </span>
              </div>
              <div
                style={{
                  fontFamily: "var(--sans-body)",
                  fontSize: 13,
                  color: "var(--fg1)",
                  fontWeight: 600,
                  borderBottom: "2px solid #C77700",
                  paddingBottom: 8,
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "baseline",
                  letterSpacing: "0.02em",
                }}
              >
                <span style={{ color: "#C77700", textTransform: "uppercase", letterSpacing: "0.08em" }}>
                  International
                </span>
                <span className="mono tabular" style={{ color: "var(--fg3)", fontSize: 11.5 }}>
                  n = {formatFR(DATA.meta.n_international)}
                </span>
              </div>
            </div>

            {FAMILY_ORDER.map((f) => (
              <div
                key={f}
                style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}
              >
                <SkillFamilyCard
                  familleLabel={DATA.familles[f]}
                  items={DATA.top_par_famille.Maroc[f]}
                  accent="#2251FF"
                />
                <SkillFamilyCard
                  familleLabel={DATA.familles[f]}
                  items={DATA.top_par_famille.International[f]}
                  accent="#C77700"
                />
              </div>
            ))}
          </div>
        ) : null}
      </section>
    </>
  );
}
