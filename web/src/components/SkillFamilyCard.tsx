"use client";

import type { CSSProperties } from "react";

export interface SkillRow {
  skill: string;
  count: number;
}

interface Props {
  familleLabel: string;
  items: SkillRow[];
  accent: string;
}

export function SkillFamilyCard({ familleLabel, items, accent }: Props) {
  const maxCount = items.length > 0 ? items[0]!.count : 1;
  const titleStyle: CSSProperties = {
    fontFamily: "var(--sans-body)",
    fontSize: 13,
    fontWeight: 700,
    color: accent,
    letterSpacing: "0.01em",
    margin: 0,
    marginBottom: 12,
  };
  return (
    <div className="card" style={{ padding: "16px 18px", minHeight: 240 }}>
      <h3 style={titleStyle}>{familleLabel}</h3>
      {items.length === 0 ? (
        <div
          style={{
            fontFamily: "var(--mono)",
            fontSize: 11.5,
            color: "var(--fg3)",
            padding: "32px 0",
            textAlign: "center",
            fontStyle: "italic",
          }}
        >
          (aucune compétence référencée)
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 5 }}>
          {items.map((it) => {
            const pct = Math.round((it.count / maxCount) * 100);
            return (
              <div
                key={it.skill}
                style={{
                  display: "grid",
                  gridTemplateColumns: "120px 1fr 38px",
                  alignItems: "center",
                  gap: 8,
                  fontSize: 12.5,
                }}
              >
                <span
                  title={it.skill}
                  style={{
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                    color: "var(--fg1)",
                  }}
                >
                  {it.skill}
                </span>
                <span
                  style={{
                    height: 10,
                    background: "color-mix(in oklch, var(--fg3) 8%, transparent)",
                    borderRadius: 2,
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
                      width: `${pct}%`,
                      background: accent,
                      opacity: 0.88,
                      borderRadius: 2,
                    }}
                  />
                </span>
                <span
                  className="mono tabular"
                  style={{ fontSize: 11.5, color: "var(--fg2)", textAlign: "right" }}
                >
                  {it.count.toLocaleString("fr-FR").replace(/ /g, " ")}
                </span>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
