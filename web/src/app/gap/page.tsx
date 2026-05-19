"use client";

import { useMemo, useState } from "react";
import { SkillFamilyCard } from "@/components/SkillFamilyCard";
import gapJson from "@/lib/gap_analysis_ensat.json";

interface ModuleCurriculum {
  code: string;
  title: string;
  volume_horaire: number;
  skills_taught: string[];
}

interface Semester {
  code: string;
  annee: number;
  n_modules: number;
  volume_total: number;
  modules: ModuleCurriculum[];
}

interface FamilyCoverage {
  couvertes: number;
  demanded: number;
  pct: number;
}

interface GapAnalysisDataset {
  meta: {
    school: string;
    school_code: string;
    filiere: string;
    filiere_code: string;
    n_modules: number;
    volume_total_h: number;
    n_skills_taught: number;
    n_skills_demanded_ma: number;
    n_skills_demanded_intl: number;
    generated_at: string;
  };
  couverture: Record<
    "Maroc" | "International",
    {
      n_demanded: number;
      n_couvertes: number;
      pct_skills: number;
      pct_offres_couvertes: number;
    }
  >;
  top_gaps: Record<"Maroc" | "International", { skill: string; demand_count: number }[]>;
  mismatch: string[];
  couverture_par_famille: Record<"Maroc" | "International", Record<string, FamilyCoverage>>;
  curriculum: { semesters: Semester[] };
}

const DATA = gapJson as unknown as GapAnalysisDataset;

const ACCENT_MA = "#2251FF";
const ACCENT_INTL = "#C77700";
const COL_OK = "#0F8F65";
const COL_WARN = "#C77700";
const COL_KO = "#E11D48";

function formatFR(n: number): string {
  return n.toLocaleString("fr-FR").replace(/ /g, " ");
}

// Couleur selon taux de couverture (vert ≥ 50 %, ambre ≥ 20 %, rouge < 20 %)
function coverageColor(pct: number): string {
  if (pct >= 50) return COL_OK;
  if (pct >= 20) return COL_WARN;
  return COL_KO;
}

export default function GapAnalysisPage() {
  const meta = DATA.meta;
  const couvMA = DATA.couverture.Maroc;
  const couvINTL = DATA.couverture.International;

  // Liste fusionnée des familles (union MA + INTL)
  const allFamilies = useMemo(() => {
    const set = new Set<string>([
      ...Object.keys(DATA.couverture_par_famille.Maroc),
      ...Object.keys(DATA.couverture_par_famille.International),
    ]);
    return Array.from(set).sort((a, b) => {
      const dMA = DATA.couverture_par_famille.Maroc[a]?.demanded ?? 0;
      const dMA2 = DATA.couverture_par_famille.Maroc[b]?.demanded ?? 0;
      return dMA2 - dMA;
    });
  }, []);

  const [openSemester, setOpenSemester] = useState<string | null>(null);

  // Recommandations dérivées des top gaps MA + INTL
  const reco = useMemo(() => {
    const top5MA = DATA.top_gaps.Maroc.slice(0, 5);
    const top5INTL = DATA.top_gaps.International.slice(0, 5);

    // Familles à 0 % côté MA
    const famZeroMA = Object.entries(DATA.couverture_par_famille.Maroc)
      .filter(([, v]) => v.pct === 0)
      .map(([k]) => k);

    return { top5MA, top5INTL, famZeroMA };
  }, []);

  return (
    <>
      {/* Hero compact */}
      <section style={{ marginBottom: 28 }}>
        <div
          style={{
            fontFamily: "var(--mono)",
            fontSize: 11,
            color: "var(--fg3)",
            textTransform: "uppercase",
            letterSpacing: "0.1em",
            marginBottom: 6,
          }}
        >
          {meta.school} · {meta.filiere_code}
        </div>
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
          Le programme ENSA Tétouan face au marché
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
          Pour chaque compétence demandée par les recruteurs IA, on vérifie si elle est enseignée
          dans le cursus officiel <strong>Sciences des Données, Big Data &amp; IA</strong> de l&apos;ENSA Tétouan
          ({meta.n_modules} modules, {formatFR(meta.volume_total_h)} heures, {meta.n_skills_taught} compétences
          enseignées).
        </p>
      </section>

      {/* Acte 1 — KPI strip (cursus + angle mort) */}
      <div className="kpi-grid" style={{ gridTemplateColumns: "repeat(2, minmax(0, 1fr))", marginBottom: 24 }}>
        <KPI
          label="Cursus officiel"
          value={`${meta.n_modules} modules`}
          sub={`${formatFR(meta.volume_total_h)} heures · 5 semestres + PFE`}
        />
        <KPI
          label="Top angle mort"
          value={reco.top5MA[0]?.skill ?? "—"}
          sub={`${reco.top5MA[0]?.demand_count ?? 0} offres MA · non enseigné`}
          accent={COL_KO}
        />
      </div>

      {/* Cartes Couverture Maroc / International — format détaillé */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "1fr 1fr",
          gap: 24,
          marginBottom: 32,
        }}
      >
        <div
          className="card"
          style={{ padding: "18px 22px", borderTop: "3px solid " + ACCENT_MA }}
        >
          <div
            style={{
              fontFamily: "var(--mono)",
              fontSize: 11,
              color: ACCENT_MA,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              marginBottom: 10,
            }}
          >
            Couverture Maroc
          </div>
          <div
            style={{
              fontSize: 14,
              color: "var(--fg2)",
              fontFamily: "var(--sans-body)",
              lineHeight: 1.5,
            }}
          >
            <span style={{ color: "var(--fg1)", fontWeight: 600, fontSize: 22 }}>
              {formatFR(couvMA.n_couvertes)} / {formatFR(couvMA.n_demanded)}
            </span>{" "}
            <span style={{ fontSize: 13, color: "var(--fg2)" }}>compétences enseignées</span>
            {" · "}
            <span
              className="mono tabular"
              style={{ color: ACCENT_MA, fontWeight: 700, fontSize: 18 }}
            >
              {couvMA.pct_skills.toFixed(1).replace(".", ",")} %
            </span>
          </div>
        </div>
        <div
          className="card"
          style={{ padding: "18px 22px", borderTop: "3px solid " + ACCENT_INTL }}
        >
          <div
            style={{
              fontFamily: "var(--mono)",
              fontSize: 11,
              color: ACCENT_INTL,
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              marginBottom: 10,
            }}
          >
            Couverture International
          </div>
          <div
            style={{
              fontSize: 14,
              color: "var(--fg2)",
              fontFamily: "var(--sans-body)",
              lineHeight: 1.5,
            }}
          >
            <span style={{ color: "var(--fg1)", fontWeight: 600, fontSize: 22 }}>
              {formatFR(couvINTL.n_couvertes)} / {formatFR(couvINTL.n_demanded)}
            </span>{" "}
            <span style={{ fontSize: 13, color: "var(--fg2)" }}>compétences enseignées</span>
            {" · "}
            <span
              className="mono tabular"
              style={{ color: ACCENT_INTL, fontWeight: 700, fontSize: 18 }}
            >
              {couvINTL.pct_skills.toFixed(1).replace(".", ",")} %
            </span>
          </div>
        </div>
      </div>

      {/* Acte 2 — Couverture par famille */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          eyebrow="Analyse par discipline"
          title="Où le programme brille, où il décroche"
          right={`${allFamilies.length} familles de compétences · marché Maroc vs International`}
        />

        <div className="card" style={{ padding: "22px 26px" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            {allFamilies.map((fam) => {
              const ma = DATA.couverture_par_famille.Maroc[fam] ?? { couvertes: 0, demanded: 0, pct: 0 };
              const intl = DATA.couverture_par_famille.International[fam] ?? { couvertes: 0, demanded: 0, pct: 0 };
              return (
                <div key={fam} style={{ display: "grid", gridTemplateColumns: "180px 1fr", gap: 18, alignItems: "center" }}>
                  <div style={{ fontSize: 13.5, color: "var(--fg1)", fontWeight: 500 }}>{fam}</div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                    <FamilyBar label="Maroc" coverage={ma} color={ACCENT_MA} />
                    <FamilyBar label="International" coverage={intl} color={ACCENT_INTL} />
                  </div>
                </div>
              );
            })}
          </div>

          <div
            style={{
              fontSize: 11.5,
              color: "var(--fg3)",
              fontStyle: "italic",
              marginTop: 18,
              lineHeight: 1.55,
            }}
          >
            Lecture : sur chaque ligne, longueur de barre = % de skills demandées dans cette famille
            qui sont enseignées au moins une fois dans le cursus. Vert ≥ 50 %, ambre ≥ 20 %, rouge &lt; 20 %.
          </div>
        </div>
      </section>

      {/* Acte 3 — Top gaps MA + INTL côte à côte */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          eyebrow="Les angles morts"
          title="Compétences demandées non enseignées · top 10"
          right="ordre par volume d'offres décroissant"
        />

        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 22 }}>
          <PairHeader label="Maroc" n={couvMA.n_demanded - couvMA.n_couvertes} color={ACCENT_MA}>
            <SkillFamilyCard
              familleLabel="Compétences à intégrer · priorité Maroc"
              items={DATA.top_gaps.Maroc.slice(0, 10).map((g) => ({
                skill: g.skill,
                count: g.demand_count,
              }))}
              accent={ACCENT_MA}
            />
          </PairHeader>
          <PairHeader label="International" n={couvINTL.n_demanded - couvINTL.n_couvertes} color={ACCENT_INTL}>
            <SkillFamilyCard
              familleLabel="Compétences à intégrer · priorité International"
              items={DATA.top_gaps.International.slice(0, 10).map((g) => ({
                skill: g.skill,
                count: g.demand_count,
              }))}
              accent={ACCENT_INTL}
            />
          </PairHeader>
        </div>
      </section>

      {/* Acte 4 — Carte du curriculum (5 semestres) */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          eyebrow="Le cursus exhaustif"
          title="Les 5 semestres · cliquer pour explorer les modules"
          right={`${meta.n_modules} modules · ${formatFR(meta.volume_total_h)} heures`}
        />

        <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 12 }}>
          {DATA.curriculum.semesters.map((sem) => {
            const isOpen = openSemester === sem.code;
            return (
              <button
                key={sem.code}
                onClick={() => setOpenSemester(isOpen ? null : sem.code)}
                style={{
                  textAlign: "left",
                  padding: "16px 16px",
                  borderRadius: 8,
                  border: `1px solid color-mix(in oklch, ${isOpen ? ACCENT_MA : "var(--fg3)"} ${isOpen ? 50 : 18}%, transparent)`,
                  background: isOpen
                    ? "color-mix(in oklch, " + ACCENT_MA + " 6%, transparent)"
                    : "color-mix(in oklch, var(--fg3) 3%, transparent)",
                  cursor: "pointer",
                  color: "inherit",
                  fontFamily: "var(--sans-body)",
                  transition: "all 150ms",
                }}
              >
                <div
                  className="mono"
                  style={{
                    fontSize: 10.5,
                    color: isOpen ? ACCENT_MA : "var(--fg3)",
                    fontWeight: 700,
                    letterSpacing: "0.1em",
                    textTransform: "uppercase",
                    marginBottom: 4,
                  }}
                >
                  {sem.code} · Année {sem.annee}
                </div>
                <div
                  style={{
                    fontFamily: "var(--serif-display)",
                    fontSize: 19,
                    fontWeight: 600,
                    color: "var(--fg1)",
                    lineHeight: 1.1,
                  }}
                >
                  {sem.n_modules} modules
                </div>
                <div className="mono tabular" style={{ fontSize: 12, color: "var(--fg2)", marginTop: 4 }}>
                  {sem.volume_total} h
                </div>
              </button>
            );
          })}
        </div>

        {/* Détail du semestre sélectionné */}
        {openSemester && (
          <div
            className="card"
            style={{
              padding: "20px 24px",
              marginTop: 16,
              borderLeft: `4px solid ${ACCENT_MA}`,
            }}
          >
            {(() => {
              const sem = DATA.curriculum.semesters.find((s) => s.code === openSemester);
              if (!sem) return null;
              return (
                <>
                  <div
                    className="mono"
                    style={{
                      fontSize: 11,
                      color: ACCENT_MA,
                      fontWeight: 700,
                      letterSpacing: "0.08em",
                      textTransform: "uppercase",
                      marginBottom: 12,
                    }}
                  >
                    Semestre {sem.code} · {sem.n_modules} modules · {sem.volume_total} h
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
                    {sem.modules.map((m) => (
                      <div
                        key={m.code}
                        style={{
                          display: "grid",
                          gridTemplateColumns: "60px 1fr 70px",
                          gap: 14,
                          padding: "10px 0",
                          borderBottom: "1px solid color-mix(in oklch, var(--fg3) 8%, transparent)",
                          alignItems: "baseline",
                        }}
                      >
                        <span className="mono tabular" style={{ fontSize: 12, color: "var(--fg3)", fontWeight: 600 }}>
                          {m.code}
                        </span>
                        <div>
                          <div style={{ fontSize: 13.5, fontWeight: 600, color: "var(--fg1)", marginBottom: 4 }}>
                            {m.title}
                          </div>
                          <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                            {m.skills_taught.map((s) => (
                              <span
                                key={s}
                                style={{
                                  fontSize: 11,
                                  padding: "2px 8px",
                                  borderRadius: 10,
                                  background: "color-mix(in oklch, var(--fg3) 8%, transparent)",
                                  color: "var(--fg2)",
                                }}
                              >
                                {s}
                              </span>
                            ))}
                          </div>
                        </div>
                        <span className="mono tabular" style={{ fontSize: 12, color: "var(--fg2)", textAlign: "right" }}>
                          {m.volume_horaire} h
                        </span>
                      </div>
                    ))}
                  </div>
                </>
              );
            })()}
          </div>
        )}
      </section>

      {/* Acte 5 — Recommandations dérivées */}
      <section style={{ marginBottom: 36 }}>
        <SectionHeader
          eyebrow="Synthèse opérationnelle"
          title="Trois pistes pour combler le gap"
          right="recommandations dérivées automatiquement des données"
        />

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 16 }}>
          <Recommendation
            n="01"
            color={COL_KO}
            title={`Créer un module Cloud Computing`}
            metric={`+${reco.top5MA.filter((g) => ["gcp", "azure", "aws"].includes(g.skill.toLowerCase())).reduce((a, g) => a + g.demand_count, 0)} offres MA couvertes`}
            desc={`Le Cloud (GCP, Azure, AWS) est en tête des angles morts. Famille « Cloud » à 0 % de couverture. Volume horaire recommandé ≈ 94 h en S3 ou S4.`}
          />
          <Recommendation
            n="02"
            color={COL_WARN}
            title="Renforcer DevOps / MLOps en S5"
            metric={`+${(reco.top5MA.find((g) => g.skill.toLowerCase().includes("ci/cd"))?.demand_count ?? 0) + (DATA.top_gaps.Maroc.find((g) => g.skill.toLowerCase() === "mlops")?.demand_count ?? 0)} offres MA`}
            desc={`CI/CD, MLOps, Kubernetes : ces compétences sont devenues incontournables en 2026 pour tout poste IA en production. À intégrer au module M235 (Systèmes d'exploitation avancés) ou créer un nouveau module.`}
          />
          <Recommendation
            n="03"
            color={ACCENT_INTL}
            title="Ouvrir un atelier GenAI / LLM Engineering"
            metric={`+${DATA.top_gaps.International.filter((g) => ["prompt engineering", "rag", "langchain", "agents ia"].includes(g.skill.toLowerCase())).reduce((a, g) => a + g.demand_count, 0)} offres INTL`}
            desc={`Prompt Engineering, RAG, LangChain, Agents IA dominent les offres internationales depuis ChatGPT (nov. 2022). Le cursus actuel précède cette vague et mérite un module ouvert post-PFE ou en option S5.`}
          />
        </div>
      </section>

    </>
  );
}

// ───────── helpers ─────────

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
          color: "var(--fg3)",
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
      <div style={{ fontSize: 11.5, color: "var(--fg2)", marginTop: 6, lineHeight: 1.4 }}>{sub}</div>
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
    <div style={{ marginBottom: 18, display: "flex", justifyContent: "space-between", alignItems: "baseline", flexWrap: "wrap", gap: 12 }}>
      <div>
        <div
          style={{
            fontFamily: "var(--mono)",
            fontSize: 11,
            color: "var(--fg3)",
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
        <div className="mono" style={{ fontSize: 11, color: "var(--fg3)" }}>
          {right}
        </div>
      )}
    </div>
  );
}

function FamilyBar({
  label,
  coverage,
  color,
}: {
  label: string;
  coverage: FamilyCoverage;
  color: string;
}) {
  const fillColor = coverageColor(coverage.pct);
  const width = Math.max(2, coverage.pct);
  return (
    <div style={{ display: "grid", gridTemplateColumns: "84px 1fr 110px", alignItems: "center", gap: 10 }}>
      <span style={{ fontSize: 11, color, fontWeight: 600, fontFamily: "var(--mono)", textTransform: "uppercase", letterSpacing: "0.06em" }}>
        {label}
      </span>
      <span
        style={{
          height: 12,
          background: "color-mix(in oklch, var(--fg3) 8%, transparent)",
          borderRadius: 3,
          position: "relative",
          overflow: "hidden",
        }}
      >
        <span
          style={{
            position: "absolute",
            inset: "0 auto 0 0",
            width: `${width}%`,
            background: `linear-gradient(90deg, ${fillColor} 0%, color-mix(in oklch, ${fillColor} 75%, transparent) 100%)`,
            borderRadius: 3,
            transition: "width 380ms cubic-bezier(0.22, 1, 0.36, 1)",
          }}
        />
      </span>
      <span
        className="mono tabular"
        style={{
          fontSize: 11.5,
          color: "var(--fg2)",
          textAlign: "right",
          fontVariantNumeric: "tabular-nums",
        }}
      >
        <span style={{ color: fillColor, fontWeight: 700 }}>{coverage.pct.toFixed(1).replace(".", ",")} %</span>
        <span style={{ color: "var(--fg3)" }}> · {coverage.couvertes}/{coverage.demanded}</span>
      </span>
    </div>
  );
}

function PairHeader({
  label,
  n,
  color,
  children,
}: {
  label: string;
  n: number;
  color: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <div
        style={{
          fontFamily: "var(--sans-body)",
          fontSize: 13,
          color: "var(--fg1)",
          fontWeight: 600,
          borderBottom: "2px solid " + color,
          paddingBottom: 8,
          marginBottom: 4,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
        }}
      >
        <span style={{ color, textTransform: "uppercase", letterSpacing: "0.08em" }}>{label}</span>
        <span className="mono tabular" style={{ color: "var(--fg3)", fontSize: 11.5 }}>
          {formatFR(n)} compétences manquantes
        </span>
      </div>
      {children}
    </div>
  );
}

function Recommendation({
  n,
  color,
  title,
  metric,
  desc,
}: {
  n: string;
  color: string;
  title: string;
  metric: string;
  desc: string;
}) {
  return (
    <div
      className="card"
      style={{
        padding: "18px 20px",
        borderLeft: `3px solid ${color}`,
      }}
    >
      <div
        className="mono"
        style={{
          fontSize: 11,
          color,
          fontWeight: 700,
          letterSpacing: "0.1em",
          marginBottom: 8,
        }}
      >
        Reco {n}
      </div>
      <div
        style={{
          fontFamily: "var(--serif-display)",
          fontSize: 17,
          fontWeight: 600,
          color: "var(--fg1)",
          lineHeight: 1.25,
          margin: "0 0 8px 0",
        }}
      >
        {title}
      </div>
      <div
        className="mono tabular"
        style={{
          fontSize: 13,
          color,
          fontWeight: 700,
          marginBottom: 10,
        }}
      >
        {metric}
      </div>
      <p style={{ fontSize: 12.5, color: "var(--fg2)", lineHeight: 1.55, margin: 0 }}>{desc}</p>
    </div>
  );
}
