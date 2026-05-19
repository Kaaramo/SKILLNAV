"use client";

import type { CSSProperties } from "react";

export interface TopSkillItem {
  skill: string;
  count: number;
  pct: number;
}

interface Props {
  items: TopSkillItem[];
  accent: string;
  /** n total du corpus (affiché dans le footer de la carte) */
  nTotal: number;
  /** Libelle du marche affiche en haut */
  marketLabel: string;
}

export function TopSkillsBar({ items, accent, nTotal, marketLabel }: Props) {
  if (items.length === 0) {
    return (
      <div className="card" style={{ padding: 24, textAlign: "center" }}>
        <span style={{ color: "var(--fg3)", fontFamily: "var(--mono)", fontSize: 12 }}>
          (aucune compétence)
        </span>
      </div>
    );
  }

  const maxCount = items[0]!.count;

  const headerStyle: CSSProperties = {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "baseline",
    borderBottom: "2px solid " + accent,
    paddingBottom: 12,
    marginBottom: 18,
  };
  const labelStyle: CSSProperties = {
    fontFamily: "var(--sans-body)",
    fontSize: 13,
    fontWeight: 700,
    color: accent,
    textTransform: "uppercase",
    letterSpacing: "0.08em",
  };
  const ntotalStyle: CSSProperties = {
    fontFamily: "var(--mono)",
    fontSize: 11.5,
    color: "var(--fg3)",
    fontWeight: 400,
  };

  return (
    <div className="card" style={{ padding: "20px 22px 18px", minHeight: 520 }}>
      <div style={headerStyle}>
        <span style={labelStyle}>{marketLabel}</span>
        <span className="mono tabular" style={ntotalStyle}>
          n = {nTotal.toLocaleString("fr-FR").replace(/ /g, " ")} offres
        </span>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
        {items.map((it, idx) => {
          const width = (it.count / maxCount) * 100;
          const rank = idx + 1;
          return (
            <div
              key={it.skill}
              style={{
                display: "grid",
                gridTemplateColumns: "26px 1fr",
                alignItems: "center",
                gap: 12,
                padding: "5px 0",
                borderBottom: idx < items.length - 1
                  ? "1px solid color-mix(in oklch, var(--fg3) 6%, transparent)"
                  : "none",
              }}
            >
              {/* Rank */}
              <span
                className="mono tabular"
                style={{
                  fontSize: 10.5,
                  color: "var(--fg3)",
                  textAlign: "right",
                  fontVariantNumeric: "tabular-nums",
                }}
              >
                #{rank}
              </span>

              {/* Skill row : nom + barre + count */}
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "minmax(120px, 1fr) 2fr auto",
                  alignItems: "center",
                  gap: 12,
                }}
              >
                <span
                  title={it.skill}
                  style={{
                    fontFamily: "var(--sans-body)",
                    fontSize: 12.5,
                    color: "var(--fg1)",
                    fontWeight: rank <= 3 ? 600 : 400,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {it.skill}
                </span>

                {/* Barre */}
                <span
                  style={{
                    height: 10,
                    background: "color-mix(in oklch, var(--fg3) 7%, transparent)",
                    borderRadius: 3,
                    position: "relative",
                    overflow: "hidden",
                  }}
                >
                  <span
                    style={{
                      position: "absolute",
                      left: 0,
                      top: 0,
                      bottom: 0,
                      width: `${width}%`,
                      background:
                        `linear-gradient(90deg, ${accent} 0%, color-mix(in oklch, ${accent} 78%, transparent) 100%)`,
                      borderRadius: 3,
                      transition: "width 380ms cubic-bezier(0.22, 1, 0.36, 1)",
                    }}
                  />
                </span>

                {/* Count + pct */}
                <span
                  className="mono tabular"
                  style={{
                    fontSize: 11.5,
                    color: "var(--fg2)",
                    fontVariantNumeric: "tabular-nums",
                    whiteSpace: "nowrap",
                    textAlign: "right",
                    minWidth: 92,
                  }}
                >
                  <span style={{ color: "var(--fg1)", fontWeight: 600 }}>
                    {it.count.toLocaleString("fr-FR").replace(/ /g, " ")}
                  </span>
                  <span style={{ color: "var(--fg3)" }}>
                    {"  · "}
                    {it.pct.toFixed(0)} %
                  </span>
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
