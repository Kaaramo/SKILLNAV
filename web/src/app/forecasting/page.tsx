"use client";

import { useMemo, useState } from "react";
import { ForecastChart } from "@/components/ForecastChart";
import forecastJson from "@/lib/forecast_top10.json";

interface SkillForecast {
  skill_name: string;
  family: string;
  best_method: "ARIMA" | "Prophet" | "LSTM";
  history: { period: string; count: number }[];
  forecast: { period: string; value: number; lower: number; upper: number }[];
  metrics: {
    arima_rmse: number;
    prophet_rmse: number;
    lstm_rmse: number;
  };
}

const DATA = forecastJson as unknown as SkillForecast[];

// Palette : une couleur unique par modele
const COLOR_ARIMA = "#2251FF";
const COLOR_PROPHET = "#7C3AED";
const COLOR_LSTM = "#0F8F65";

function colorOf(method: SkillForecast["best_method"]): string {
  if (method === "ARIMA") return COLOR_ARIMA;
  if (method === "Prophet") return COLOR_PROPHET;
  return COLOR_LSTM;
}

// Stats globales calculees a partir du JSON (sans supposition)
const STATS = (() => {
  const wins = { ARIMA: 0, Prophet: 0, LSTM: 0 };
  for (const s of DATA) wins[s.best_method]++;
  const medianRmse = (key: "arima_rmse" | "prophet_rmse" | "lstm_rmse") => {
    const vals = DATA.map((s) => s.metrics[key]).sort((a, b) => a - b);
    const n = vals.length;
    return n === 0 ? 0 : n % 2 === 0 ? (vals[n / 2 - 1]! + vals[n / 2]!) / 2 : vals[(n - 1) / 2]!;
  };
  const periods = DATA[0]?.history.map((h) => h.period) ?? [];
  const horizonPeriods = DATA[0]?.forecast.map((f) => f.period) ?? [];
  return {
    nSkills: DATA.length,
    wins,
    medianRmse: {
      arima: medianRmse("arima_rmse"),
      prophet: medianRmse("prophet_rmse"),
      lstm: medianRmse("lstm_rmse"),
    },
    nHistoryWeeks: periods.length,
    nHorizonWeeks: horizonPeriods.length,
    historyStart: periods[0] ?? "—",
    historyEnd: periods[periods.length - 1] ?? "—",
    horizonEnd: horizonPeriods[horizonPeriods.length - 1] ?? "—",
  };
})();

// Modele recommande V1.0 = celui avec le plus petit RMSE median
const RECOMMENDED: "ARIMA" | "Prophet" | "LSTM" = (() => {
  const arr: [SkillForecast["best_method"], number][] = [
    ["ARIMA", STATS.medianRmse.arima],
    ["Prophet", STATS.medianRmse.prophet],
    ["LSTM", STATS.medianRmse.lstm],
  ];
  arr.sort((a, b) => a[1] - b[1]);
  return arr[0]![0];
})();

// Mois en francais, format "5 janv. 2026" — lisible, sans confusion avec une heure
const MOIS_FR = [
  "janv.", "févr.", "mars", "avr.", "mai", "juin",
  "juil.", "août", "sept.", "oct.", "nov.", "déc.",
];

function formatPeriod(iso: string): string {
  const [y, m, d] = iso.split("-");
  const monthName = MOIS_FR[parseInt(m!, 10) - 1] ?? m;
  return `${parseInt(d!, 10)} ${monthName} ${y}`;
}

export default function ForecastingPage() {
  const [selectedIdx, setSelectedIdx] = useState<number>(0);
  const selected = DATA[selectedIdx]!;

  const accent = colorOf(selected.best_method);

  // Skill stats triees par best_method pour le tableau global
  const sortedAll = useMemo(() => DATA, []);

  return (
    <>
      {/* Acte 1 — KPI strip */}
      <div
        className="kpi-grid"
        style={{ gridTemplateColumns: "repeat(5, minmax(0, 1fr))" }}
      >
        <KPI
          label="Compétences prévues"
          value={STATS.nSkills.toString()}
          sub="les 10 compétences les plus centrales du marché IA"
        />
        <KPI
          label="Données observées"
          value={`${STATS.nHistoryWeeks} semaines`}
          sub={`du ${formatPeriod(STATS.historyStart)} au ${formatPeriod(STATS.historyEnd)}`}
        />
        <KPI
          label="Prédiction"
          value={`${STATS.nHorizonWeeks} semaines`}
          sub={`jusqu'au ${formatPeriod(STATS.horizonEnd)}`}
        />
        <KPI
          label="Modèles comparés"
          value="3"
          sub="ARIMA · Prophet · LSTM"
        />
        <KPI
          label="Modèle retenu"
          value={RECOMMENDED}
          sub={`erreur médiane ${STATS.medianRmse[RECOMMENDED.toLowerCase() as "arima"].toFixed(2).replace(".", ",")} — la plus basse des 3 modèles`}
          accent
        />
      </div>

      {/* Acte 2 — Sélecteur skill + Graphe */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "240px minmax(0, 1fr)",
          gap: 22,
          marginTop: 28,
          marginBottom: 22,
        }}
      >
        {/* Sélecteur de skill */}
        <div className="card" style={{ padding: "16px 14px" }}>
          <div
            style={{
              fontFamily: "var(--mono)",
              fontSize: 11,
              color: "var(--fg3)",
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              marginBottom: 10,
              paddingLeft: 4,
            }}
          >
            10 compétences
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
            {DATA.map((s, i) => {
              const isActive = i === selectedIdx;
              const color = colorOf(s.best_method);
              return (
                <button
                  key={s.skill_name}
                  onClick={() => setSelectedIdx(i)}
                  style={{
                    textAlign: "left",
                    padding: "8px 10px",
                    borderRadius: 4,
                    border: "none",
                    background: isActive
                      ? "color-mix(in oklch, " + color + " 12%, transparent)"
                      : "transparent",
                    borderLeft: isActive
                      ? `3px solid ${color}`
                      : "3px solid transparent",
                    cursor: "pointer",
                    fontFamily: "var(--sans-body)",
                    color: "var(--fg1)",
                    fontSize: 13,
                  }}
                >
                  <div
                    style={{
                      fontWeight: isActive ? 600 : 400,
                      lineHeight: 1.2,
                    }}
                  >
                    {s.skill_name}
                  </div>
                  <div
                    style={{
                      fontSize: 10.5,
                      color: "var(--fg3)",
                      fontFamily: "var(--mono)",
                      marginTop: 2,
                      display: "flex",
                      justifyContent: "space-between",
                    }}
                  >
                    <span>{s.family}</span>
                    <span style={{ color }}>{s.best_method}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Graphe principal */}
        <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
          <ForecastChart
            history={selected.history}
            forecast={selected.forecast}
            forecastColor={accent}
            modelLabel={selected.best_method}
            skillName={selected.skill_name}
            height={360}
          />

          {/* Acte 3 — Tableau metriques skill courante */}
          <div className="card" style={{ padding: "16px 18px" }}>
            <div
              style={{
                fontFamily: "var(--mono)",
                fontSize: 11,
                color: "var(--fg3)",
                textTransform: "uppercase",
                letterSpacing: "0.08em",
                marginBottom: 10,
              }}
            >
              Comparaison des 3 modèles · {selected.skill_name}
            </div>
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(3, minmax(0, 1fr))",
                gap: 12,
              }}
            >
              {(
                [
                  ["ARIMA", selected.metrics.arima_rmse, COLOR_ARIMA],
                  ["Prophet", selected.metrics.prophet_rmse, COLOR_PROPHET],
                  ["LSTM", selected.metrics.lstm_rmse, COLOR_LSTM],
                ] as const
              ).map(([name, rmse, color]) => {
                const isBest = name === selected.best_method;
                return (
                  <div
                    key={name}
                    style={{
                      padding: "10px 12px",
                      borderRadius: 6,
                      border: isBest
                        ? `2px solid ${color}`
                        : "1px solid color-mix(in oklch, var(--fg3) 14%, transparent)",
                      background: isBest
                        ? `color-mix(in oklch, ${color} 8%, transparent)`
                        : "transparent",
                    }}
                  >
                    <div
                      style={{
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "baseline",
                      }}
                    >
                      <span
                        style={{
                          fontFamily: "var(--sans-body)",
                          fontSize: 13,
                          fontWeight: 600,
                          color: isBest ? color : "var(--fg1)",
                        }}
                      >
                        {name}
                      </span>
                      {isBest && (
                        <span
                          className="mono"
                          style={{
                            fontSize: 10,
                            color,
                            textTransform: "uppercase",
                            letterSpacing: "0.08em",
                          }}
                        >
                          retenu
                        </span>
                      )}
                    </div>
                    <div
                      style={{
                        fontFamily: "var(--mono)",
                        fontSize: 18,
                        fontWeight: 700,
                        color: "var(--fg1)",
                        marginTop: 4,
                      }}
                    >
                      RMSE {rmse.toFixed(2).replace(".", ",")}
                    </div>
                  </div>
                );
              })}
            </div>
            <div
              style={{
                fontSize: 11.5,
                color: "var(--fg3)",
                marginTop: 10,
                fontStyle: "italic",
                lineHeight: 1.5,
              }}
            >
              RMSE = Root Mean Squared Error sur la dernière fenêtre test (4 semaines).
              Plus c&apos;est bas, mieux c&apos;est. Le modèle retenu pour la prévision
              affichée est celui avec le plus petit RMSE sur cette skill.
            </div>
          </div>
        </div>
      </div>

      {/* Acte 4 — Synthèse globale 10 skills */}
      <section className="section">
        <div className="card" style={{ padding: "18px 22px" }}>
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "baseline",
              marginBottom: 14,
              flexWrap: "wrap",
              gap: 12,
            }}
          >
            <div>
              <div
                style={{
                  fontFamily: "var(--mono)",
                  fontSize: 11,
                  color: "var(--fg3)",
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                }}
              >
                Synthèse §N2.3
              </div>
              <div
                style={{
                  fontFamily: "var(--serif-display)",
                  fontSize: 19,
                  fontWeight: 600,
                  color: "var(--fg1)",
                  marginTop: 4,
                }}
              >
                Comparaison ARIMA · Prophet · LSTM sur les 10 compétences
              </div>
            </div>
            <div style={{ display: "flex", gap: 18 }}>
              <Pill label="ARIMA" wins={STATS.wins.ARIMA} color={COLOR_ARIMA} />
              <Pill label="Prophet" wins={STATS.wins.Prophet} color={COLOR_PROPHET} />
              <Pill label="LSTM" wins={STATS.wins.LSTM} color={COLOR_LSTM} />
            </div>
          </div>

          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
              fontFamily: "var(--sans-body)",
              fontSize: 12.5,
            }}
          >
            <thead>
              <tr
                style={{
                  textAlign: "left",
                  borderBottom:
                    "1px solid color-mix(in oklch, var(--fg3) 18%, transparent)",
                  color: "var(--fg3)",
                  fontSize: 11,
                  textTransform: "uppercase",
                  letterSpacing: "0.06em",
                }}
              >
                <th style={{ padding: "8px 10px 8px 0" }}>Skill</th>
                <th style={{ padding: "8px 10px" }}>Famille</th>
                <th style={{ padding: "8px 10px", textAlign: "right" }}>RMSE ARIMA</th>
                <th style={{ padding: "8px 10px", textAlign: "right" }}>RMSE Prophet</th>
                <th style={{ padding: "8px 10px", textAlign: "right" }}>RMSE LSTM</th>
                <th style={{ padding: "8px 10px" }}>Retenu</th>
              </tr>
            </thead>
            <tbody>
              {sortedAll.map((s, i) => {
                const c = colorOf(s.best_method);
                const isActive = i === selectedIdx;
                return (
                  <tr
                    key={s.skill_name}
                    onClick={() => setSelectedIdx(i)}
                    style={{
                      cursor: "pointer",
                      background: isActive
                        ? "color-mix(in oklch, var(--fg3) 6%, transparent)"
                        : "transparent",
                      borderBottom:
                        "1px solid color-mix(in oklch, var(--fg3) 8%, transparent)",
                    }}
                  >
                    <td
                      style={{
                        padding: "10px 10px 10px 0",
                        fontWeight: isActive ? 600 : 400,
                        color: "var(--fg1)",
                      }}
                    >
                      {s.skill_name}
                    </td>
                    <td
                      style={{ padding: "10px 10px", color: "var(--fg2)", fontSize: 11.5 }}
                    >
                      {s.family}
                    </td>
                    <td
                      className="mono tabular"
                      style={{
                        padding: "10px 10px",
                        textAlign: "right",
                        color:
                          s.best_method === "ARIMA"
                            ? COLOR_ARIMA
                            : "var(--fg2)",
                        fontWeight: s.best_method === "ARIMA" ? 600 : 400,
                      }}
                    >
                      {s.metrics.arima_rmse.toFixed(2).replace(".", ",")}
                    </td>
                    <td
                      className="mono tabular"
                      style={{
                        padding: "10px 10px",
                        textAlign: "right",
                        color:
                          s.best_method === "Prophet"
                            ? COLOR_PROPHET
                            : "var(--fg2)",
                        fontWeight: s.best_method === "Prophet" ? 600 : 400,
                      }}
                    >
                      {s.metrics.prophet_rmse.toFixed(2).replace(".", ",")}
                    </td>
                    <td
                      className="mono tabular"
                      style={{
                        padding: "10px 10px",
                        textAlign: "right",
                        color:
                          s.best_method === "LSTM" ? COLOR_LSTM : "var(--fg2)",
                        fontWeight: s.best_method === "LSTM" ? 600 : 400,
                      }}
                    >
                      {s.metrics.lstm_rmse.toFixed(2).replace(".", ",")}
                    </td>
                    <td
                      style={{
                        padding: "10px 10px",
                        color: c,
                        fontWeight: 600,
                        fontSize: 12,
                      }}
                    >
                      {s.best_method}
                    </td>
                  </tr>
                );
              })}
              <tr
                style={{
                  background: "color-mix(in oklch, var(--fg3) 5%, transparent)",
                  fontFamily: "var(--mono)",
                  fontSize: 11.5,
                  color: "var(--fg2)",
                }}
              >
                <td style={{ padding: "10px 10px 10px 0", fontWeight: 600 }}>
                  RMSE médian
                </td>
                <td />
                <td
                  className="mono tabular"
                  style={{ padding: "10px 10px", textAlign: "right", fontWeight: 700 }}
                >
                  {STATS.medianRmse.arima.toFixed(2).replace(".", ",")}
                </td>
                <td
                  className="mono tabular"
                  style={{ padding: "10px 10px", textAlign: "right", fontWeight: 700 }}
                >
                  {STATS.medianRmse.prophet.toFixed(2).replace(".", ",")}
                </td>
                <td
                  className="mono tabular"
                  style={{ padding: "10px 10px", textAlign: "right", fontWeight: 700 }}
                >
                  {STATS.medianRmse.lstm.toFixed(2).replace(".", ",")}
                </td>
                <td />
              </tr>
            </tbody>
          </table>

          <div
            style={{
              fontSize: 12,
              color: "var(--fg3)",
              marginTop: 12,
              fontStyle: "italic",
              lineHeight: 1.55,
            }}
          >
            Lecture : <strong style={{ color: "var(--fg2)" }}>LSTM</strong> gagne sur{" "}
            {STATS.wins.LSTM}/10 skills (skill par skill) mais{" "}
            <strong style={{ color: "var(--fg2)" }}>{RECOMMENDED}</strong> a le plus
            petit RMSE médian global ({STATS.medianRmse[RECOMMENDED.toLowerCase() as "arima"].toFixed(2).replace(".", ",")}) → retenu V1.0 SKILLNAV pour robustesse moyenne.
          </div>
        </div>
      </section>
    </>
  );
}

// ─── helpers locaux ───

function KPI({
  label,
  value,
  sub,
  accent = false,
}: {
  label: string;
  value: string;
  sub: string;
  accent?: boolean;
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
          fontSize: 26,
          fontWeight: 600,
          color: accent ? "var(--skn-royal, #2251FF)" : "var(--fg1)",
          lineHeight: 1.1,
        }}
      >
        {value}
      </div>
      <div style={{ fontSize: 11.5, color: "var(--fg2)", marginTop: 6 }}>{sub}</div>
    </div>
  );
}

function Pill({ label, wins, color }: { label: string; wins: number; color: string }) {
  return (
    <div
      style={{
        display: "inline-flex",
        alignItems: "baseline",
        gap: 6,
        padding: "4px 10px",
        borderRadius: 14,
        border: `1px solid ${color}`,
        background: `color-mix(in oklch, ${color} 8%, transparent)`,
      }}
    >
      <span
        style={{
          fontFamily: "var(--sans-body)",
          fontSize: 12,
          fontWeight: 600,
          color,
        }}
      >
        {label}
      </span>
      <span
        className="mono tabular"
        style={{ fontSize: 11, color: "var(--fg2)" }}
      >
        {wins}/10
      </span>
    </div>
  );
}
