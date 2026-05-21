"use client";

import { Fragment } from "react";
import data from "@/lib/gap_multi_ensa.json";

interface EnsaCol {
  slug: string;
  school: string;
  filiere: string;
}

interface HeatRow {
  family: string;
  ensa: number[];
  marche: number;
}

interface MultiEnsaDataset {
  meta: {
    n_ensa_exploitables: number;
    n_ensa_placeholder: number;
    n_familles: number;
    n_top_skills_marche: number;
    n_skills_couverts: number;
    n_ensa_total: number;
    source_notebook: string;
    source_commit: string;
    generated_at: string;
    perimetre_marche: string;
  };
  ensa_columns: EnsaCol[];
  heatmap_familles: { rows: HeatRow[] };
  matrice_top_skills: {
    skills: string[];
    matrix: boolean[][];
    totaux: number[];
  };
}

const DATA = data as unknown as MultiEnsaDataset;

const COL_MARCHE = "#B91C1C";
const COL_FG3 = "var(--fg3)";

// ───────── helpers couleur heatmap (YlOrBr) ─────────
function heatBg(v: number): string {
  const t = Math.min(1, v / 60);
  if (t <= 0.001) return "#FFFBEB";
  // light yellow -> orange -> deep brown
  if (t < 0.5) {
    const u = t * 2;
    return interp("#FEF3C7", "#F59E0B", u);
  }
  const u = (t - 0.5) * 2;
  return interp("#F59E0B", "#78350F", u);
}
function heatText(v: number): string {
  return v >= 25 ? "#FFFFFF" : "#3F1A04";
}
function interp(a: string, b: string, t: number): string {
  const [ar, ag, ab] = hexToRgb(a);
  const [br, bg, bb] = hexToRgb(b);
  return `rgb(${Math.round(ar + (br - ar) * t)}, ${Math.round(ag + (bg - ag) * t)}, ${Math.round(ab + (bb - ab) * t)})`;
}
function hexToRgb(hex: string): [number, number, number] {
  const m = hex.replace("#", "");
  return [parseInt(m.slice(0, 2), 16), parseInt(m.slice(2, 4), 16), parseInt(m.slice(4, 6), 16)];
}
function fmtPct(v: number): string {
  return v.toFixed(1).replace(".", ",");
}

export function MultiEnsaView() {
  const meta = DATA.meta;
  const cols = DATA.ensa_columns;
  const rows = DATA.heatmap_familles.rows;
  const { skills, matrix, totaux } = DATA.matrice_top_skills;

  return (
    <>
      {/* Hero */}
      <section style={{ marginBottom: 28 }}>
        <h1
          style={{
            fontFamily: "var(--serif-display)",
            fontSize: 32,
            fontWeight: 600,
            color: "var(--fg1)",
            lineHeight: 1.2,
            margin: "0 0 10px 0",
          }}
        >
          Désalignement marché ↔ formations IA du réseau ENSA
        </h1>
        <p
          style={{
            fontSize: 15,
            color: "var(--fg2)",
            lineHeight: 1.65,
            maxWidth: 880,
            margin: 0,
          }}
        >
          Croisement entre les <strong>{meta.n_top_skills_marche} compétences</strong> les plus
          demandées par les recruteurs IA et les programmes officiels de{" "}
          <strong>{meta.n_ensa_exploitables} ENSA</strong> publiant un cursus Data Science / Big
          Data / IA (sur {meta.n_ensa_total} écoles du réseau).
        </p>
      </section>

      {/* KPI strip */}
      <div
        className="kpi-grid"
        style={{ gridTemplateColumns: "repeat(4, minmax(0, 1fr))", marginBottom: 32 }}
      >
        <KPI
          label="ENSA"
          value={`${meta.n_ensa_exploitables}`}
          sub=""
        />
        <KPI
          label="Top skills marché couverts"
          value={`${meta.n_skills_couverts} / ${meta.n_top_skills_marche}`}
          sub=""
          accent={COL_MARCHE}
        />
        <KPI
          label="Gap structurel GenAI"
          value="34,5 %"
          sub=""
          accent="#7C3AED"
        />
        <KPI
          label="Familles analysées"
          value={`${meta.n_familles}`}
          sub=""
        />
      </div>

      {/* Section A — Heatmap famille */}
      <section style={{ marginBottom: 40 }}>
        <SectionHeader
          eyebrow=""
          title="Recouvrement par famille de compétences"
        />

        <div className="card" style={{ padding: "20px 22px" }}>
          <div className="me-heat-wrap">
            {/* Bloc 6 ENSA */}
            <div
              className="me-heat-grid"
              style={{ gridTemplateColumns: `170px repeat(${cols.length}, minmax(64px, 1fr))` }}
            >
              <div className="me-corner" />
              {cols.map((c) => (
                <ColHead key={c.slug} school={c.school} filiere={c.filiere} />
              ))}

              {rows.map((r) => (
                <Fragment key={r.family}>
                  <RowLabel>{r.family}</RowLabel>
                  {r.ensa.map((v, i) => (
                    <HeatCell key={i} v={v} />
                  ))}
                </Fragment>
              ))}
            </div>

            {/* Bloc Marché — séparé, encadré rouge */}
            <div className="me-heat-marche">
              <div
                className="me-heat-grid"
                style={{ gridTemplateColumns: "minmax(74px, 1fr)" }}
              >
                <ColHead school="MARCHÉ" filiere="(top 200)" marche />
                {rows.map((r) => (
                  <HeatCell key={r.family} v={r.marche} marche />
                ))}
              </div>
            </div>
          </div>

        </div>
      </section>

      {/* Section B — Matrice top 10 skills marché */}
      <section style={{ marginBottom: 40 }}>
        <SectionHeader
          eyebrow="Top 10 skills marché"
          title="Matrice de couverture · skill ↔ ENSA"
          right="OUI = compétence enseignée · NON = non identifiée"
        />

        <div className="card" style={{ padding: "20px 22px" }}>
          <div
            className="me-cov-grid"
            style={{ gridTemplateColumns: `200px repeat(${cols.length}, minmax(80px, 1fr))` }}
          >
            <div className="me-corner" />
            {cols.map((c) => (
              <ColHead key={c.slug} school={c.school} filiere={c.filiere} />
            ))}

            {skills.map((s, i) => {
              const row = matrix[i] ?? [];
              return (
                <Fragment key={s}>
                  <RowLabel>{s}</RowLabel>
                  {row.map((yes, j) => (
                    <CovCell key={j} yes={yes} />
                  ))}
                </Fragment>
              );
            })}

            {/* TOTAL */}
            <div className="me-cov-total-label">TOTAL / {skills.length}</div>
            {totaux.map((t, i) => (
              <TotalCell key={i} value={t} max={skills.length} />
            ))}
          </div>

          <p className="me-lecture">
            <strong>Constat brut</strong> : 8 des 10 compétences les plus demandées par le marché
            (RAG, LangChain, LLMs, prompt engineering, LangGraph, fine-tuning, OpenAI API,
            embeddings) ne figurent dans <em>aucun</em> programme officiel des 6 ENSA. Seuls{" "}
            <strong>pytorch</strong> et <strong>tensorflow</strong> sont enseignés — et uniquement
            à Fès, Khouribga et Tétouan. Aucune ENSA ne dépasse 20 % de couverture sur ce top 10.
          </p>
        </div>
      </section>
    </>
  );
}

/* ───────── sous-composants locaux ───────── */

function KPI({
  label,
  value,
  sub,
  accent,
}: {
  label: string;
  value: string;
  sub: string;
  accent?: string;
}) {
  return (
    <div className="kpi-card">
      <div
        style={{
          fontFamily: "var(--mono)",
          fontSize: 10.5,
          color: COL_FG3,
          textTransform: "uppercase",
          letterSpacing: "0.08em",
          marginBottom: 6,
        }}
      >
        {label}
      </div>
      <div
        style={{
          fontFamily: "var(--serif-display)",
          fontSize: 24,
          fontWeight: 600,
          color: accent ?? "var(--fg1)",
          lineHeight: 1.1,
          wordBreak: "break-word",
        }}
      >
        {value}
      </div>
      {sub ? (
        <div style={{ fontSize: 11.5, color: "var(--fg2)", marginTop: 6, lineHeight: 1.4 }}>
          {sub}
        </div>
      ) : null}
    </div>
  );
}

function SectionHeader({
  eyebrow,
  title,
  right,
}: {
  eyebrow: string;
  title: string;
  right?: string;
}) {
  return (
    <div
      style={{
        marginBottom: 18,
        display: "flex",
        justifyContent: "space-between",
        alignItems: "baseline",
        flexWrap: "wrap",
        gap: 12,
      }}
    >
      <div>
        <div
          style={{
            fontFamily: "var(--mono)",
            fontSize: 11,
            color: COL_FG3,
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            marginBottom: 4,
          }}
        >
          {eyebrow}
        </div>
        <h2
          style={{
            fontFamily: "var(--serif-display)",
            fontSize: 22,
            fontWeight: 600,
            color: "var(--fg1)",
            margin: 0,
            lineHeight: 1.25,
          }}
        >
          {title}
        </h2>
      </div>
      {right && (
        <div className="mono" style={{ fontSize: 11, color: COL_FG3 }}>
          {right}
        </div>
      )}
    </div>
  );
}

function ColHead({
  school,
  filiere,
  marche = false,
}: {
  school: string;
  filiere: string;
  marche?: boolean;
}) {
  return (
    <div className={marche ? "me-col-head me-col-head-marche" : "me-col-head"}>
      <span className="me-col-school">{school}</span>
      <span className="me-col-filiere">{filiere}</span>
    </div>
  );
}

function RowLabel({ children }: { children: React.ReactNode }) {
  return <div className="me-row-label">{children}</div>;
}

function HeatCell({ v, marche = false }: { v: number; marche?: boolean }) {
  return (
    <div
      className={marche ? "me-heat-cell me-heat-cell-marche" : "me-heat-cell"}
      style={{ background: heatBg(v), color: heatText(v) }}
    >
      {fmtPct(v)}
    </div>
  );
}

function CovCell({ yes }: { yes: boolean }) {
  return (
    <div className={yes ? "me-cov-cell me-cov-yes" : "me-cov-cell me-cov-no"}>
      {yes ? "OUI" : "NON"}
    </div>
  );
}

function TotalCell({ value, max }: { value: number; max: number }) {
  const ratio = value / max;
  const cls = value === 0 ? "me-total-cell me-total-zero" : "me-total-cell me-total-some";
  return (
    <div className={cls} title={`${value} / ${max}`}>
      <span style={{ opacity: 0.35 + ratio * 0.65 }}>{value}</span>
    </div>
  );
}

