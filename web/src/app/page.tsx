"use client";

import { useState } from "react";
import { KPICard, SectionRule, Segmented } from "@/components/atoms";
import { DonutChart } from "@/components/DonutChart";
import { SkillFamilyCard } from "@/components/SkillFamilyCard";
import { SlopeChart } from "@/components/SlopeChart";
import { TopSkillsBar } from "@/components/TopSkillsBar";
import { Treemap } from "@/components/Treemap";
import overview from "@/lib/dashboard_overview.json";
import gapEnsat from "@/lib/gap_analysis_ensat.json";
import topSkills from "@/lib/top_skills.json";

type Origine = "Maroc" | "International" | "Tous";

interface AiTypeSlice {
  code: string;
  label: string;
  color: string;
  count: number;
  pct: number;
}

interface OverviewDataset {
  meta: {
    n_total: number;
    n_maroc: number;
    n_international: number;
    n_companies: Record<Origine, number>;
    n_sources: Record<Origine, number>;
    n_skills_unique: Record<Origine, number>;
    n_metiers: Record<Origine, number>;
    bascule_ai_first_pct: number;
    bascule_ai_first_count: number;
    graph: {
      n_nodes: number;
      n_edges: number;
      n_communities: number;
      modularity_louvain: number;
      top_skill: {
        name: string;
        count: number;
        family: string;
        pagerank: number;
      };
    };
    periode: {
      n_mois: number;
      debut: string;
      fin: string;
      ancrage: string;
    };
    generated_at: string;
    source: string;
  };
  ai_type_distribution: Record<Origine, AiTypeSlice[]>;
  top_intitules: Record<"Maroc" | "International", { title: string; count: number }[]>;
  top_employeurs: Record<"Maroc" | "International", { company: string; count: number }[]>;
  bascule_temporelle: {
    months: string[];
    series: Record<"ai-first" | "ai-support" | "ml-first" | "non-ai" | "unknown", number[]>;
  };
}

const DATA = overview as unknown as OverviewDataset;

interface GapEnsatDataset {
  meta: {
    school: string;
    filiere_code: string;
    n_modules: number;
    volume_total_h: number;
    n_skills_taught: number;
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
}

const ENSAT = gapEnsat as unknown as GapEnsatDataset;

interface TopSkillsDataset {
  meta: { n_maroc: number; n_international: number; top_n: number; source: string };
  Maroc: { skill: string; count: number; pct: number }[];
  International: { skill: string; count: number; pct: number }[];
}

const TOP_SKILLS = topSkills as unknown as TopSkillsDataset;

const ACCENT_MA = "#2251FF";
const ACCENT_INTL = "#C77700";

function formatFR(n: number): string {
  return n.toLocaleString("fr-FR").replace(/ /g, " ");
}

function PairHeader({ left, right }: { left: { label: string; n: number }; right: { label: string; n: number } }) {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24, marginBottom: 4 }}>
      <div
        style={{
          fontFamily: "var(--sans-body)",
          fontSize: 13,
          color: "var(--fg1)",
          fontWeight: 600,
          borderBottom: "2px solid " + ACCENT_MA,
          paddingBottom: 8,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          letterSpacing: "0.02em",
        }}
      >
        <span style={{ color: ACCENT_MA, textTransform: "uppercase", letterSpacing: "0.08em" }}>
          {left.label}
        </span>
        <span className="mono tabular" style={{ color: "var(--fg3)", fontSize: 11.5 }}>
          n = {formatFR(left.n)}
        </span>
      </div>
      <div
        style={{
          fontFamily: "var(--sans-body)",
          fontSize: 13,
          color: "var(--fg1)",
          fontWeight: 600,
          borderBottom: "2px solid " + ACCENT_INTL,
          paddingBottom: 8,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          letterSpacing: "0.02em",
        }}
      >
        <span style={{ color: ACCENT_INTL, textTransform: "uppercase", letterSpacing: "0.08em" }}>
          {right.label}
        </span>
        <span className="mono tabular" style={{ color: "var(--fg3)", fontSize: 11.5 }}>
          n = {formatFR(right.n)}
        </span>
      </div>
    </div>
  );
}

type View = "marche" | "gap";

export default function OverviewPage() {
  const meta = DATA.meta;
  const [view, setView] = useState<View>("marche");

  return (
    <>
      {/* KPI strip — 4 cards */}
      <div className="kpi-grid">
        <KPICard
          eyebrow="Offres collectées au Maroc"
          value={formatFR(meta.n_maroc)}
          size="md"
          foot={
            <span>
              {meta.n_sources.Maroc} sources · {formatFR(meta.n_companies.Maroc)} entreprises
            </span>
          }
        />
        <KPICard
          eyebrow="Offres collectées à l'international"
          value={formatFR(meta.n_international)}
          size="md"
          foot={
            <span>
              {formatFR(meta.n_companies.International)} entreprises ·{" "}
              {meta.n_metiers.International} métiers représentés
            </span>
          }
        />
        <KPICard
          eyebrow="Métiers dominants"
          value={
            <span
              style={{
                display: "inline-flex",
                flexDirection: "column",
                gap: 6,
                lineHeight: 1.1,
              }}
            >
              <span style={{ display: "inline-flex", alignItems: "baseline", gap: 10 }}>
                <span
                  style={{
                    fontSize: 11,
                    color: "var(--fg2)",
                    textTransform: "uppercase",
                    letterSpacing: "0.08em",
                    fontFamily: "var(--sans-body)",
                    fontWeight: 500,
                  }}
                >
                  Maroc
                </span>
                <span style={{ color: ACCENT_MA, fontWeight: 600 }}>
                  {DATA.top_intitules.Maroc[0]?.title ?? "—"}
                </span>
              </span>
              <span style={{ display: "inline-flex", alignItems: "baseline", gap: 10 }}>
                <span
                  style={{
                    fontSize: 11,
                    color: "var(--fg2)",
                    textTransform: "uppercase",
                    letterSpacing: "0.08em",
                    fontFamily: "var(--sans-body)",
                    fontWeight: 500,
                  }}
                >
                  International
                </span>
                <span style={{ color: ACCENT_INTL, fontWeight: 600 }}>
                  {DATA.top_intitules.International[0]?.title ?? "—"}
                </span>
              </span>
            </span>
          }
          size="md"
        />
        <KPICard
          eyebrow="Entreprises analysées"
          value={formatFR(meta.n_companies.Tous)}
          size="md"
          foot={
            <span>
              {formatFR(meta.n_companies.Maroc)} Maroc + {formatFR(meta.n_companies.International)} INTERNATIONAL
            </span>
          }
        />
      </div>

      {/* Toggle vue marché ↔ vue gap ENSAT */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          margin: "32px 0 12px",
        }}
      >
        <Segmented<View>
          options={[
            { value: "marche", label: "Vue marché" },
            { value: "gap", label: "Gap ENSA Tétouan" },
          ]}
          value={view}
          onChange={setView}
        />
      </div>

      {view === "marche" ? (
        <>
      {/* Section — Top 20 compétences MA vs INTL (figures F.11 + F.14) */}
      <section className="section">
        <SectionRule
          title="Top 20 compétences les plus demandées"
        />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <TopSkillsBar
            items={TOP_SKILLS.Maroc}
            accent={ACCENT_MA}
            nTotal={TOP_SKILLS.meta.n_maroc}
            marketLabel="Maroc"
          />
          <TopSkillsBar
            items={TOP_SKILLS.International}
            accent={ACCENT_INTL}
            nTotal={TOP_SKILLS.meta.n_international}
            marketLabel="International"
          />
        </div>
      </section>

      {/* Section A — Donuts AI-type */}
      <section className="section">
        <SectionRule
          title="Distribution des types de poste"
        />
        <PairHeader
          left={{ label: "Maroc", n: meta.n_maroc }}
          right={{ label: "International", n: meta.n_international }}
        />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <div className="card" style={{ padding: 24 }}>
            <DonutChart
              slices={DATA.ai_type_distribution.Maroc}
              centerTitle="dominant"
              centerValue={
                DATA.ai_type_distribution.Maroc[0]
                  ? DATA.ai_type_distribution.Maroc[0].label
                  : "—"
              }
            />
          </div>
          <div className="card" style={{ padding: 24 }}>
            <DonutChart
              slices={DATA.ai_type_distribution.International}
              centerTitle="dominant"
              centerValue={
                DATA.ai_type_distribution.International[0]
                  ? DATA.ai_type_distribution.International[0].label
                  : "—"
              }
            />
          </div>
        </div>
      </section>

      {/* Section B — Top intitulés de poste (slope chart MA ↔ INTL) */}
      <section className="section">
        <SectionRule
          title="Top intitulés de poste · l'inversion Maroc ↔ International"
        />
        <SlopeChart
          ma={DATA.top_intitules.Maroc}
          intl={DATA.top_intitules.International}
          accentMA={ACCENT_MA}
          accentINTL={ACCENT_INTL}
          nMA={meta.n_maroc}
          nINTL={meta.n_international}
        />
      </section>

      {/* Section C — Top entreprises qui recrutent (treemap pair) */}
      <section className="section">
        <SectionRule
          title="Top entreprises qui recrutent"
        />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <Treemap
            items={DATA.top_employeurs.Maroc.map((t) => ({ name: t.company, value: t.count }))}
            accent={ACCENT_MA}
            marketLabel="Maroc"
            nTotal={meta.n_maroc}
            height={380}
          />
          <Treemap
            items={DATA.top_employeurs.International.map((t) => ({ name: t.company, value: t.count }))}
            accent={ACCENT_INTL}
            marketLabel="International"
            nTotal={meta.n_international}
            height={380}
          />
        </div>
      </section>

        </>
      ) : (
      /* Section E — Gap analysis marché vs formation ENSAT */
      <section className="section">
        <SectionRule
          title="Recouvrement marché ↔ formation ENSA Tétouan"
          right={`${ENSAT.meta.filiere_code} · ${ENSAT.meta.n_modules} modules · ${formatFR(ENSAT.meta.volume_total_h)} h`}
        />

        {/* Mini KPIs couverture */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 24,
            marginBottom: 24,
          }}
        >
          <div
            className="card"
            style={{
              padding: "18px 22px",
              borderTop: "3px solid " + ACCENT_MA,
            }}
          >
            <div
              style={{
                fontFamily: "var(--mono)",
                fontSize: 11,
                color: ACCENT_MA,
                textTransform: "uppercase",
                letterSpacing: "0.08em",
                marginBottom: 6,
              }}
            >
              Couverture Maroc
            </div>
            <div
              style={{
                fontSize: 14,
                color: "var(--fg2)",
                marginTop: 4,
                fontFamily: "var(--sans-body)",
                lineHeight: 1.5,
              }}
            >
              <span style={{ color: "var(--fg1)", fontWeight: 600, fontSize: 22 }}>
                {ENSAT.couverture.Maroc.n_couvertes} / {ENSAT.couverture.Maroc.n_demanded}
              </span>{" "}
              <span style={{ fontSize: 13, color: "var(--fg2)" }}>compétences enseignées</span>
              {" · "}
              <span
                className="mono tabular"
                style={{
                  color: ACCENT_MA,
                  fontWeight: 700,
                  fontSize: 18,
                }}
              >
                {ENSAT.couverture.Maroc.pct_skills.toFixed(1).replace(".", ",")} %
              </span>
            </div>
          </div>
          <div
            className="card"
            style={{
              padding: "18px 22px",
              borderTop: "3px solid " + ACCENT_INTL,
            }}
          >
            <div
              style={{
                fontFamily: "var(--mono)",
                fontSize: 11,
                color: ACCENT_INTL,
                textTransform: "uppercase",
                letterSpacing: "0.08em",
                marginBottom: 6,
              }}
            >
              Couverture International
            </div>
            <div
              style={{
                fontSize: 14,
                color: "var(--fg2)",
                marginTop: 4,
                fontFamily: "var(--sans-body)",
                lineHeight: 1.5,
              }}
            >
              <span style={{ color: "var(--fg1)", fontWeight: 600, fontSize: 22 }}>
                {formatFR(ENSAT.couverture.International.n_couvertes)} /{" "}
                {formatFR(ENSAT.couverture.International.n_demanded)}
              </span>{" "}
              <span style={{ fontSize: 13, color: "var(--fg2)" }}>compétences enseignées</span>
              {" · "}
              <span
                className="mono tabular"
                style={{
                  color: ACCENT_INTL,
                  fontWeight: 700,
                  fontSize: 18,
                }}
              >
                {ENSAT.couverture.International.pct_skills.toFixed(1).replace(".", ",")} %
              </span>
            </div>
          </div>
        </div>

        {/* Pair Top gaps MA / INTL */}
        <PairHeader
          left={{ label: "Maroc · top gaps", n: ENSAT.couverture.Maroc.n_demanded - ENSAT.couverture.Maroc.n_couvertes }}
          right={{ label: "International · top gaps", n: ENSAT.couverture.International.n_demanded - ENSAT.couverture.International.n_couvertes }}
        />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 24 }}>
          <SkillFamilyCard
            familleLabel="Compétences demandées non enseignées"
            items={ENSAT.top_gaps.Maroc.slice(0, 10).map((g) => ({
              skill: g.skill,
              count: g.demand_count,
            }))}
            accent={ACCENT_MA}
          />
          <SkillFamilyCard
            familleLabel="Compétences demandées non enseignées"
            items={ENSAT.top_gaps.International.slice(0, 10).map((g) => ({
              skill: g.skill,
              count: g.demand_count,
            }))}
            accent={ACCENT_INTL}
          />
        </div>

      </section>
      )}
    </>
  );
}
