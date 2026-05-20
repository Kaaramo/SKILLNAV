"use client";

import { Fragment } from "react";
import { FAMILIES, type FamilyKey } from "@/lib/mockData";

/* ============================================================
 *  Sparkline 80×24
 * ============================================================ */
export function Sparkline({
  data,
  w = 80,
  h = 24,
  color = "var(--hl)",
  strokeWidth = 1.5,
}: {
  data: number[];
  w?: number;
  h?: number;
  color?: string;
  strokeWidth?: number;
}) {
  const min = Math.min(...data);
  const max = Math.max(...data);
  const span = max - min || 1;
  const pad = 2;
  const dx = (w - 2 * pad) / (data.length - 1);
  const path = data
    .map((v, i) => {
      const x = pad + dx * i;
      const y = h - pad - ((v - min) / span) * (h - 2 * pad);
      return (i === 0 ? "M" : "L") + x.toFixed(1) + " " + y.toFixed(1);
    })
    .join(" ");
  return (
    <svg width={w} height={h} viewBox={`0 0 ${w} ${h}`} className="spark">
      <path
        d={path}
        stroke={color}
        strokeWidth={strokeWidth}
        fill="none"
        strokeLinejoin="round"
        strokeLinecap="round"
      />
    </svg>
  );
}

export interface LineSeries {
  data: number[];
  color?: string;
  dashedFrom?: number;
  ci?: { lo: number[]; hi: number[] } | null;
}

/* ============================================================
 *  Line chart with optional forecast (dashed) + CI band
 * ============================================================ */
export function LineChart({
  width = 320,
  height = 140,
  series,
  observed,
  total,
  showAxes = true,
  showForecastLabel = false,
}: {
  width?: number;
  height?: number;
  series: LineSeries[];
  observed?: number;
  total?: number;
  showAxes?: boolean;
  showForecastLabel?: boolean;
}) {
  const allValues: number[] = [];
  for (const s of series) {
    allValues.push(...s.data);
    if (s.ci) allValues.push(...s.ci.lo, ...s.ci.hi);
  }
  const min = Math.min(...allValues);
  const max = Math.max(...allValues);
  const span = max - min || 1;
  const padL = 28;
  const padR = 12;
  const padT = 14;
  const padB = 22;
  const innerW = width - padL - padR;
  const innerH = height - padT - padB;
  const n = total || (series[0]?.data.length ?? 0);
  const dx = innerW / Math.max(1, n - 1);

  const xPx = (i: number) => padL + dx * i;
  const yPx = (v: number) => padT + innerH - ((v - min) / span) * innerH;

  const forecastX = observed != null && observed < n ? xPx(observed - 1) : null;

  return (
    <svg
      width="100%"
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
      style={{ display: "block", maxWidth: "100%" }}
    >
      {showAxes &&
        [0.25, 0.5, 0.75].map((p) => (
          <line
            key={p}
            x1={padL}
            x2={width - padR}
            y1={padT + innerH * (1 - p)}
            y2={padT + innerH * (1 - p)}
            className="chart-grid"
          />
        ))}

      {forecastX != null && (
        <>
          <rect
            x={forecastX}
            y={padT}
            width={width - padR - forecastX}
            height={innerH}
            fill="var(--hl)"
            opacity={0.04}
          />
          <line
            x1={forecastX}
            x2={forecastX}
            y1={padT}
            y2={padT + innerH}
            stroke="var(--fg3)"
            strokeDasharray="2 3"
            strokeWidth={1}
            opacity={0.6}
          />
        </>
      )}

      {series.map((s, si) =>
        s.ci ? (
          <path
            key={`ci-${si}`}
            d={
              s.ci.hi.map((v, i) => (i === 0 ? "M" : "L") + xPx(i) + " " + yPx(v)).join(" ") +
              " " +
              s.ci.lo
                .slice()
                .reverse()
                .map((v, i) => "L" + xPx(s.ci!.lo.length - 1 - i) + " " + yPx(v))
                .join(" ") +
              " Z"
            }
            fill={s.color || "var(--hl)"}
            opacity={0.13}
          />
        ) : null,
      )}

      {series.map((s, si) => {
        const splitAt = s.dashedFrom != null ? s.dashedFrom : observed;
        if (splitAt == null || splitAt >= s.data.length) {
          const path = s.data
            .map((v, i) => (i === 0 ? "M" : "L") + xPx(i) + " " + yPx(v))
            .join(" ");
          return (
            <path
              key={si}
              d={path}
              fill="none"
              stroke={s.color || "var(--hl)"}
              strokeWidth={1.5}
              strokeLinejoin="round"
              strokeLinecap="round"
            />
          );
        }
        const solid = s.data
          .slice(0, splitAt)
          .map((v, i) => (i === 0 ? "M" : "L") + xPx(i) + " " + yPx(v))
          .join(" ");
        const dashed = s.data
          .slice(splitAt - 1)
          .map((v, i) => (i === 0 ? "M" : "L") + xPx(splitAt - 1 + i) + " " + yPx(v))
          .join(" ");
        return (
          <g key={si}>
            <path
              d={solid}
              fill="none"
              stroke={s.color || "var(--hl)"}
              strokeWidth={1.5}
              strokeLinejoin="round"
              strokeLinecap="round"
            />
            <path
              d={dashed}
              fill="none"
              stroke={s.color || "var(--hl)"}
              strokeWidth={1.5}
              strokeDasharray="4 3"
              strokeLinejoin="round"
              strokeLinecap="round"
            />
          </g>
        );
      })}

      {showForecastLabel && forecastX != null && (
        <text
          x={forecastX + 6}
          y={padT + 14}
          className="chart-axis-label"
          fontSize="9.5"
          style={{ textTransform: "uppercase", letterSpacing: "0.08em", fontWeight: 700 }}
        >
          prévision →
        </text>
      )}

      {showAxes && (
        <>
          <text x={padL - 4} y={padT + 4} textAnchor="end" className="chart-axis-label">
            {Math.round(max)}
          </text>
          <text x={padL - 4} y={padT + innerH} textAnchor="end" className="chart-axis-label">
            {Math.round(min)}
          </text>
        </>
      )}
    </svg>
  );
}

/* ============================================================
 *  Scatter — Score × Volume
 * ============================================================ */
export interface ScatterPt {
  x: number;
  y: number;
  fam: FamilyKey;
  size: number;
  hi: boolean;
}

export function ScatterPlot({
  width = 520,
  height = 360,
  points,
}: {
  width?: number;
  height?: number;
  points: ScatterPt[];
}) {
  const padL = 40;
  const padR = 16;
  const padT = 28;
  const padB = 32;
  const innerW = width - padL - padR;
  const innerH = height - padT - padB;
  return (
    <svg
      width="100%"
      height={height}
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="none"
      style={{ display: "block", maxWidth: "100%" }}
    >
      {[0, 0.25, 0.5, 0.75, 1].map((p) => (
        <g key={p}>
          <line
            x1={padL}
            x2={width - padR}
            y1={padT + innerH * (1 - p)}
            y2={padT + innerH * (1 - p)}
            className="chart-grid"
          />
          <text
            x={padL - 6}
            y={padT + innerH * (1 - p) + 3}
            textAnchor="end"
            className="chart-axis-label"
          >
            {p === 0 ? "0.30" : (0.3 + p * 0.7).toFixed(2)}
          </text>
        </g>
      ))}
      <line
        x1={padL}
        x2={width - padR}
        y1={padT + innerH * (1 - (0.7 - 0.3) / 0.7)}
        y2={padT + innerH * (1 - (0.7 - 0.3) / 0.7)}
        stroke="var(--hl)"
        strokeWidth={1}
        strokeDasharray="2 4"
        opacity={0.5}
      />
      <line
        x1={padL}
        x2={width - padR}
        y1={padT + innerH * (1 - (0.85 - 0.3) / 0.7)}
        y2={padT + innerH * (1 - (0.85 - 0.3) / 0.7)}
        stroke="var(--hl)"
        strokeWidth={1}
        strokeDasharray="2 4"
        opacity={0.5}
      />
      <text x={padL} y={height - 8} className="chart-axis-label">
        0
      </text>
      <text x={width - padR} y={height - 8} textAnchor="end" className="chart-axis-label">
        3 240
      </text>
      {points.map((p, i) => {
        const F = FAMILIES[p.fam];
        return (
          <circle
            key={i}
            cx={padL + p.x * innerW}
            cy={padT + innerH * (1 - p.y)}
            r={p.size}
            fill={p.hi ? F.color : "transparent"}
            stroke={F.color}
            strokeWidth={1.5}
            opacity={p.hi ? 0.85 : 0.6}
          />
        );
      })}
    </svg>
  );
}

/* ============================================================
 *  Force-directed graph mock (static)
 * ============================================================ */
export interface FgNode {
  x: number;
  y: number;
  fam: FamilyKey;
  size: number;
}
export interface FgEdge {
  s: number;
  t: number;
  w: number;
}

export function ForceGraphMock({
  nodes,
  edges,
  width = 800,
  height = 600,
}: {
  nodes: FgNode[];
  edges: FgEdge[];
  width?: number;
  height?: number;
}) {
  return (
    <svg
      width="100%"
      height="100%"
      viewBox={`0 0 ${width} ${height}`}
      preserveAspectRatio="xMidYMid meet"
      style={{ display: "block" }}
    >
      <g>
        {edges.map((e, i) => {
          const a = nodes[e.s]!;
          const b = nodes[e.t]!;
          return (
            <line
              key={i}
              x1={a.x}
              y1={a.y}
              x2={b.x}
              y2={b.y}
              stroke="var(--fg3)"
              strokeWidth={Math.max(0.4, e.w * 1.2)}
              opacity={0.25}
            />
          );
        })}
      </g>
      <g>
        {nodes.map((n, i) => {
          const F = FAMILIES[n.fam];
          return (
            <g key={i}>
              <circle
                cx={n.x}
                cy={n.y}
                r={n.size}
                fill={F.color}
                fillOpacity={0.18}
                stroke={F.color}
                strokeWidth={1.5}
              />
            </g>
          );
        })}
      </g>
      <g>
        <circle
          cx={400}
          cy={300}
          r={16}
          fill={FAMILIES["deep-learning"].color}
          fillOpacity={0.35}
          stroke={FAMILIES["deep-learning"].color}
          strokeWidth={2}
        />
        <text
          x={400}
          y={278}
          textAnchor="middle"
          fontFamily="JetBrains Mono, monospace"
          fontSize="11"
          fill="var(--fg1)"
        >
          LLM Engineering
        </text>
      </g>
    </svg>
  );
}

/* ============================================================
 *  Diverging bars — Maroc vs International
 * ============================================================ */
export interface DivergingRowLike {
  fam: string;
  lbl: string;
  ma: number;
  in_: number;
}

export function DivergingBars({ rows, max = 30 }: { rows: DivergingRowLike[]; max?: number }) {
  return (
    <div>
      <div
        className="dbar-row"
        style={{
          borderBottom: "1px dashed var(--line-dashed)",
          paddingBottom: 8,
          marginBottom: 4,
        }}
      >
        <span />
        <span className="mono muted" style={{ fontSize: 11, textAlign: "right" }}>
          ← Maroc (%)
        </span>
        <span className="mono muted" style={{ fontSize: 11 }}>
          International (%) →
        </span>
        <span className="mono muted" style={{ fontSize: 11, textAlign: "right" }}>
          Δ (pts)
        </span>
      </div>
      <div className="dbars">
        {rows.map((r) => {
          const lw = (r.ma / max) * 100;
          const rw = (r.in_ / max) * 100;
          const delta = r.in_ - r.ma;
          return (
            <div key={r.fam} className="dbar-row">
              <span className="lbl">{r.lbl}</span>
              <span className="l-side">
                <span
                  className="bar"
                  style={{
                    width: `${lw}%`,
                    justifyContent: "flex-end",
                    paddingRight: 8,
                    paddingLeft: 0,
                  }}
                >
                  <span className="v">{r.ma.toFixed(1)} %</span>
                </span>
              </span>
              <span className="r-side">
                <span
                  className="bar"
                  style={{ width: `${rw}%`, justifyContent: "flex-start", paddingLeft: 8 }}
                >
                  <span className="v">{r.in_.toFixed(1)} %</span>
                </span>
              </span>
              <span className={`delta ${delta > 0 ? "pos" : delta < 0 ? "neg" : ""}`}>
                {delta > 0 ? "+" : ""}
                {delta.toFixed(1)}
              </span>
            </div>
          );
        })}
      </div>
      <div className="dbar-legend">
        <span className="swatch ma">Maroc</span>
        <span className="swatch in">International</span>
      </div>
    </div>
  );
}

/* ============================================================
 *  Confusion matrix
 * ============================================================ */
export function ConfusionMatrix({
  matrix,
  classes,
}: {
  matrix: number[][];
  classes: readonly string[];
}) {
  const flatMax = Math.max(...matrix.flat());
  return (
    <div className="confmat">
      <div className="h" />
      {classes.map((c) => (
        <div key={c} className="h">
          {c}
        </div>
      ))}
      {matrix.map((row, ri) => (
        <Fragment key={ri}>
          <div className="h row">{classes[ri]}</div>
          {row.map((v, ci) => {
            const diag = ri === ci;
            const intensity = v / flatMax;
            const style = diag
              ? {
                  background: `color-mix(in oklch, var(--hl) ${20 + intensity * 70}%, transparent)`,
                }
              : v > 5
                ? {
                    background: `color-mix(in oklch, var(--skn-error) ${5 + intensity * 12}%, transparent)`,
                    color: "var(--fg2)",
                  }
                : { background: "transparent", color: "var(--fg3)" };
            return (
              <div key={ci} className={`cell ${diag ? "diag" : ""}`} style={style}>
                {v}
              </div>
            );
          })}
        </Fragment>
      ))}
    </div>
  );
}

/* ============================================================
 *  Gap analysis — dual-bar coverage
 * ============================================================ */
export interface GapRow {
  fam: string;
  lbl: string;
  marche: number;
  ensa: number;
  delta: number;
}

export function GapBars({ rows }: { rows: GapRow[] }) {
  return (
    <div>
      {rows.map((r) => (
        <div key={r.fam} className="gapbar-row">
          <span className="lbl">{r.lbl}</span>
          <span className="gapbar">
            <span className="marche" style={{ width: `${r.marche}%` }} />
            <span
              className="marche-lbl"
              style={{ left: `${r.marche}%`, paddingLeft: 6, color: "var(--hl)" }}
            >
              {r.marche} %
            </span>
            <span className="ensa" style={{ width: `${r.ensa}%` }} />
            <span className="ensa-lbl" style={{ left: `${r.ensa}%`, paddingLeft: 6 }}>
              {r.ensa} %
            </span>
          </span>
          <span className={`gap-delta ${r.delta > 0 ? "pos" : "neg"}`}>
            {r.delta > 0 ? "+" : ""}
            {r.delta}
          </span>
        </div>
      ))}
      <div
        style={{
          display: "flex",
          gap: 16,
          marginTop: 14,
          fontFamily: "var(--mono)",
          fontSize: 11.5,
          color: "var(--fg3)",
        }}
      >
        <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
          <span style={{ width: 18, height: 8, background: "var(--hl)", borderRadius: 2 }} />
          marché · demandé
        </span>
        <span style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
          <span
            style={{
              width: 18,
              height: 8,
              border: "1.5px dashed var(--fg2)",
              borderRadius: 2,
              background: "color-mix(in oklch, var(--fg2) 14%, transparent)",
            }}
          />
          ENSA · enseigné
        </span>
      </div>
    </div>
  );
}
