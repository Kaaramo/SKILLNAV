"use client";

import { useMemo, useState } from "react";

export interface HistoryPoint {
  period: string; // YYYY-MM-DD
  count: number;
}

export interface ForecastPoint {
  period: string;
  value: number;
  lower: number;
  upper: number;
}

interface Props {
  history: HistoryPoint[];
  forecast: ForecastPoint[];
  /** Couleur de la trajectoire forecast (bleu / violet / vert selon best_method) */
  forecastColor: string;
  /** Label du modele utilise pour le forecast ("ARIMA" / "Prophet" / "LSTM") */
  modelLabel: string;
  /** Nom de la skill (affiche dans le tooltip) */
  skillName: string;
  height?: number;
}

const W = 900;
const PAD_L = 56;
const PAD_R = 24;
const PAD_T = 30;
const PAD_B = 48;

const COLOR_HIST = "var(--fg2)";
const COLOR_AXIS = "color-mix(in oklch, var(--fg3) 30%, transparent)";
const COLOR_GRID = "color-mix(in oklch, var(--fg3) 12%, transparent)";

// Mois abreges en francais — pas de confusion avec une heure
const MOIS_FR_SHORT = [
  "jan", "fév", "mar", "avr", "mai", "juin",
  "juil", "août", "sep", "oct", "nov", "déc",
];

function formatDate(iso: string): string {
  const [, m, d] = iso.split("-");
  const mi = parseInt(m!, 10) - 1;
  return `${parseInt(d!, 10)} ${MOIS_FR_SHORT[mi] ?? m}`;
}

export function ForecastChart({
  history,
  forecast,
  forecastColor,
  modelLabel,
  skillName,
  height = 360,
}: Props) {
  const [hoverIdx, setHoverIdx] = useState<number | null>(null);

  const allPoints = useMemo(
    () => [
      ...history.map((p, i) => ({
        kind: "hist" as const,
        x: i,
        value: p.count,
        lower: null as number | null,
        upper: null as number | null,
        period: p.period,
      })),
      ...forecast.map((p, i) => ({
        kind: "fcst" as const,
        x: history.length + i,
        value: p.value,
        lower: p.lower,
        upper: p.upper,
        period: p.period,
      })),
    ],
    [history, forecast],
  );

  // Echelles
  const maxValue = useMemo(() => {
    const vals = allPoints.flatMap((p) =>
      p.upper != null ? [p.value, p.upper] : [p.value],
    );
    return Math.max(...vals, 10) * 1.1;
  }, [allPoints]);

  const totalX = allPoints.length - 1;
  const innerW = W - PAD_L - PAD_R;
  const innerH = height - PAD_T - PAD_B;
  const x = (i: number) => PAD_L + (i / totalX) * innerW;
  const y = (v: number) => PAD_T + innerH - (v / maxValue) * innerH;

  // Ligne historique (SVG path)
  const histPath = history
    .map((p, i) => `${i === 0 ? "M" : "L"} ${x(i)} ${y(p.count)}`)
    .join(" ");

  // Ligne forecast (continuee depuis le dernier point historique)
  const lastHistIdx = history.length - 1;
  const lastHistPoint = history[lastHistIdx]!;
  const fcstPath = [
    `M ${x(lastHistIdx)} ${y(lastHistPoint.count)}`,
    ...forecast.map((p, i) => `L ${x(history.length + i)} ${y(p.value)}`),
  ].join(" ");

  // Bande IC95 % : polygone refermé (upper aller, lower retour)
  const icPath =
    forecast.length === 0
      ? ""
      : [
          // upper aller, en partant du dernier point historique
          `M ${x(lastHistIdx)} ${y(lastHistPoint.count)}`,
          ...forecast.map((p, i) => `L ${x(history.length + i)} ${y(p.upper)}`),
          // lower retour
          ...forecast
            .slice()
            .reverse()
            .map((p, i) => {
              const idx = history.length + forecast.length - 1 - i;
              return `L ${x(idx)} ${y(p.lower)}`;
            }),
          `L ${x(lastHistIdx)} ${y(lastHistPoint.count)}`,
          "Z",
        ].join(" ");

  // Y ticks (5 paliers)
  const ticks = useMemo(() => {
    const step = maxValue / 4;
    return [0, 1, 2, 3, 4].map((i) => Math.round(i * step));
  }, [maxValue]);

  // X ticks (toutes les 2 semaines pour pas surcharger)
  const xTickIndices = useMemo(() => {
    const out: number[] = [];
    for (let i = 0; i < allPoints.length; i += 2) out.push(i);
    if (out[out.length - 1] !== allPoints.length - 1) out.push(allPoints.length - 1);
    return out;
  }, [allPoints.length]);

  const separatorX = x(lastHistIdx);

  const hovered = hoverIdx !== null ? allPoints[hoverIdx] : null;

  return (
    <div
      className="card"
      style={{ padding: "18px 22px 14px", overflow: "hidden" }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          marginBottom: 8,
        }}
      >
        <div
          style={{
            fontFamily: "var(--serif-display)",
            fontSize: 22,
            fontWeight: 600,
            color: "var(--fg1)",
          }}
        >
          {skillName}
        </div>
        <div
          style={{
            fontFamily: "var(--mono)",
            fontSize: 11,
            color: "var(--fg3)",
            letterSpacing: "0.06em",
          }}
        >
          modèle retenu ·{" "}
          <span style={{ color: forecastColor, fontWeight: 700 }}>{modelLabel}</span>
        </div>
      </div>

      <svg
        viewBox={`0 0 ${W} ${height}`}
        width="100%"
        height={height}
        style={{ display: "block", overflow: "visible" }}
      >
        {/* Grille horizontale */}
        {ticks.map((v) => (
          <g key={`g-${v}`}>
            <line
              x1={PAD_L}
              x2={W - PAD_R}
              y1={y(v)}
              y2={y(v)}
              stroke={COLOR_GRID}
              strokeWidth={1}
            />
            <text
              x={PAD_L - 8}
              y={y(v)}
              textAnchor="end"
              dominantBaseline="middle"
              fontSize={10.5}
              fill="var(--fg3)"
              fontFamily="var(--mono)"
            >
              {v}
            </text>
          </g>
        ))}

        {/* Axe X (labels dates) */}
        {xTickIndices.map((i) => {
          const p = allPoints[i]!;
          return (
            <text
              key={`x-${i}`}
              x={x(i)}
              y={height - PAD_B + 16}
              textAnchor="middle"
              fontSize={10}
              fill="var(--fg3)"
              fontFamily="var(--mono)"
            >
              {formatDate(p.period)}
            </text>
          );
        })}

        {/* Bande IC95 % */}
        {icPath && (
          <path
            d={icPath}
            fill={forecastColor}
            fillOpacity={0.15}
            stroke="none"
          />
        )}

        {/* Separateur vertical observé / prévu */}
        <line
          x1={separatorX}
          x2={separatorX}
          y1={PAD_T}
          y2={height - PAD_B}
          stroke={COLOR_AXIS}
          strokeWidth={1}
          strokeDasharray="3 3"
        />
        <text
          x={separatorX}
          y={PAD_T - 10}
          textAnchor="middle"
          fontSize={10}
          fill="var(--fg3)"
          fontFamily="var(--mono)"
          letterSpacing={0.5}
        >
          début prévision
        </text>

        {/* Ligne historique */}
        <path
          d={histPath}
          fill="none"
          stroke={COLOR_HIST}
          strokeWidth={2}
          strokeLinejoin="round"
          strokeLinecap="round"
        />

        {/* Ligne forecast (pointillee) */}
        <path
          d={fcstPath}
          fill="none"
          stroke={forecastColor}
          strokeWidth={2.5}
          strokeDasharray="6 4"
          strokeLinejoin="round"
          strokeLinecap="round"
        />

        {/* Points historique */}
        {history.map((p, i) => (
          <circle
            key={`h-${i}`}
            cx={x(i)}
            cy={y(p.count)}
            r={hoverIdx === i ? 5 : 3}
            fill={COLOR_HIST}
          />
        ))}

        {/* Points forecast */}
        {forecast.map((p, i) => {
          const idx = history.length + i;
          return (
            <circle
              key={`f-${i}`}
              cx={x(idx)}
              cy={y(p.value)}
              r={hoverIdx === idx ? 6 : 4}
              fill={forecastColor}
              stroke="white"
              strokeWidth={1.5}
            />
          );
        })}

        {/* Zone hover (transparente) */}
        {allPoints.map((p, i) => {
          const xCenter = x(i);
          const slotWidth = innerW / totalX;
          return (
            <rect
              key={`hv-${i}`}
              x={xCenter - slotWidth / 2}
              y={PAD_T}
              width={slotWidth}
              height={innerH}
              fill="transparent"
              onMouseEnter={() => setHoverIdx(i)}
              onMouseLeave={() => setHoverIdx(null)}
              style={{ cursor: "crosshair" }}
            />
          );
        })}

        {/* Tooltip */}
        {hovered && (
          <g style={{ pointerEvents: "none" }}>
            <line
              x1={x(hovered.x)}
              x2={x(hovered.x)}
              y1={PAD_T}
              y2={height - PAD_B}
              stroke={COLOR_AXIS}
              strokeWidth={1}
            />
            <g
              transform={`translate(${Math.min(
                x(hovered.x) + 12,
                W - 200,
              )}, ${PAD_T + 8})`}
            >
              <rect
                x={0}
                y={0}
                width={186}
                height={hovered.kind === "fcst" ? 64 : 42}
                rx={4}
                fill="var(--bg)"
                stroke="color-mix(in oklch, var(--fg3) 25%, transparent)"
              />
              <text
                x={10}
                y={16}
                fontSize={11}
                fill="var(--fg3)"
                fontFamily="var(--mono)"
              >
                {formatDate(hovered.period)}
              </text>
              <text
                x={10}
                y={32}
                fontSize={12}
                fill="var(--fg1)"
                fontWeight={600}
                fontFamily="var(--sans-body)"
              >
                {hovered.kind === "hist"
                  ? `${hovered.value} offres (observé)`
                  : `${hovered.value.toFixed(1)} offres (prévu)`}
              </text>
              {hovered.kind === "fcst" && (
                <text
                  x={10}
                  y={50}
                  fontSize={10.5}
                  fill="var(--fg2)"
                  fontFamily="var(--mono)"
                >
                  IC 95 % · [{hovered.lower!.toFixed(1)} ; {hovered.upper!.toFixed(1)}]
                </text>
              )}
            </g>
          </g>
        )}
      </svg>
    </div>
  );
}
