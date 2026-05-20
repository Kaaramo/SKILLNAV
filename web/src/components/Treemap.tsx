"use client";

export interface TreemapItem {
  name: string;
  value: number;
}

interface Rect {
  x: number;
  y: number;
  w: number;
  h: number;
  item: TreemapItem;
}

interface Props {
  items: TreemapItem[];
  accent: string;
  marketLabel: string;
  nTotal: number;
  height?: number;
}

// ────────────────────────────────────────────────────────────────────────────
// Squarified treemap (Bruls / Huijing / van Wijk 2000), version compacte.
// ────────────────────────────────────────────────────────────────────────────

function worstAspect(row: TreemapItem[], side: number, scale: number): number {
  const sum = row.reduce((a, b) => a + b.value, 0);
  const rowArea = sum * scale;
  if (rowArea === 0 || side === 0) return Infinity;
  const minV = Math.min(...row.map((i) => i.value));
  const maxV = Math.max(...row.map((i) => i.value));
  return Math.max(
    (side * side * maxV * scale) / (rowArea * rowArea),
    (rowArea * rowArea) / (side * side * minV * scale),
  );
}

function squarify(items: TreemapItem[], x: number, y: number, w: number, h: number): Rect[] {
  const sorted = [...items].filter((it) => it.value > 0).sort((a, b) => b.value - a.value);
  const totalV = sorted.reduce((a, b) => a + b.value, 0);
  if (totalV === 0) return [];
  const scale = (w * h) / totalV;

  const rects: Rect[] = [];
  let remaining = sorted;
  let curX = x;
  let curY = y;
  let curW = w;
  let curH = h;

  while (remaining.length > 0) {
    const side = Math.min(curW, curH);
    let row: TreemapItem[] = [remaining[0]!];
    let bestWorst = worstAspect(row, side, scale);
    let take = 1;

    for (let i = 1; i < remaining.length; i++) {
      const newRow = [...row, remaining[i]!];
      const newWorst = worstAspect(newRow, side, scale);
      if (newWorst > bestWorst) break;
      row = newRow;
      bestWorst = newWorst;
      take = i + 1;
    }

    const rowSum = row.reduce((a, b) => a + b.value, 0);
    const rowArea = rowSum * scale;

    if (curW >= curH) {
      const rowW = rowArea / curH;
      let yy = curY;
      for (const item of row) {
        const itemH = (item.value * scale) / rowW;
        rects.push({ x: curX, y: yy, w: rowW, h: itemH, item });
        yy += itemH;
      }
      curX += rowW;
      curW -= rowW;
    } else {
      const rowH = rowArea / curW;
      let xx = curX;
      for (const item of row) {
        const itemW = (item.value * scale) / rowH;
        rects.push({ x: xx, y: curY, w: itemW, h: rowH, item });
        xx += itemW;
      }
      curY += rowH;
      curH -= rowH;
    }

    remaining = remaining.slice(take);
  }

  return rects;
}

export function Treemap({
  items,
  accent,
  marketLabel,
  nTotal,
  height = 380,
}: Props) {
  const W = 480;
  const H = height;
  const rects = squarify(items, 0, 0, W, H);
  const maxV = rects.length > 0 ? Math.max(...rects.map((r) => r.item.value)) : 1;

  return (
    <div className="card" style={{ padding: "20px 22px 18px", minHeight: H + 80 }}>
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
          borderBottom: "2px solid " + accent,
          paddingBottom: 12,
          marginBottom: 16,
        }}
      >
        <span
          style={{
            fontFamily: "var(--sans-body)",
            fontSize: 13,
            fontWeight: 700,
            color: accent,
            textTransform: "uppercase",
            letterSpacing: "0.08em",
          }}
        >
          {marketLabel}
        </span>
        <span
          className="mono tabular"
          style={{ fontSize: 11.5, color: "var(--fg3)" }}
        >
          {`n = ${nTotal.toLocaleString("fr-FR").replace(/ /g, " ")} offres`}
        </span>
      </div>

      <svg
        viewBox={`0 0 ${W} ${H}`}
        preserveAspectRatio="none"
        width="100%"
        height={H}
        style={{ display: "block" }}
      >
        {rects.map((r) => {
          const intensity = 0.45 + 0.55 * (r.item.value / maxV);
          const fill = `color-mix(in oklch, ${accent} ${Math.round(intensity * 100)}%, white)`;
          // Fontsize qui s'adapte a la taille du rectangle (nom complet wrappe sur N lignes)
          const labelFontSize = Math.max(9, Math.min(r.w / 10, r.h / 5, 14));
          const valueFontSize = Math.max(8.5, Math.min(labelFontSize - 1.5, 12));
          const area = r.w * r.h;
          const showValue = area > 1400;

          return (
            <g key={r.item.name}>
              <rect
                x={r.x}
                y={r.y}
                width={r.w}
                height={r.h}
                fill={fill}
                stroke="var(--bg)"
                strokeWidth={2}
              >
                <title>{`${r.item.name} · ${r.item.value} offres`}</title>
              </rect>
              <foreignObject
                x={r.x}
                y={r.y}
                width={r.w}
                height={r.h}
                style={{ pointerEvents: "none" }}
              >
                <div
                  style={{
                    width: "100%",
                    height: "100%",
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                    padding: "4px 6px",
                    boxSizing: "border-box",
                    color: "white",
                    fontFamily: "var(--sans-body)",
                    textAlign: "center",
                    lineHeight: 1.15,
                    overflow: "hidden",
                    wordBreak: "break-word",
                    hyphens: "auto",
                  }}
                >
                  <span
                    style={{
                      fontSize: `${labelFontSize}px`,
                      fontWeight: 600,
                    }}
                  >
                    {r.item.name}
                  </span>
                  {showValue ? (
                    <span
                      style={{
                        fontSize: `${valueFontSize}px`,
                        fontFamily: "var(--mono)",
                        opacity: 0.9,
                        marginTop: 3,
                      }}
                    >
                      {r.item.value}
                    </span>
                  ) : null}
                </div>
              </foreignObject>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
