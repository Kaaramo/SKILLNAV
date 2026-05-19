"use client";

export interface DonutSlice {
  label: string;
  count: number;
  color: string;
  pct: number;
}

interface Props {
  slices: DonutSlice[];
  size?: number;
  thickness?: number;
  centerTitle?: string;
  centerValue?: string;
}

export function DonutChart({
  slices,
  size = 200,
  thickness = 28,
  centerTitle,
  centerValue,
}: Props) {
  const total = slices.reduce((acc, s) => acc + s.count, 0);
  if (total === 0) {
    return (
      <div
        style={{
          fontFamily: "var(--mono)",
          fontSize: 11.5,
          color: "var(--fg3)",
          textAlign: "center",
          padding: "32px 0",
          fontStyle: "italic",
        }}
      >
        (aucune donnée)
      </div>
    );
  }

  const cx = size / 2;
  const cy = size / 2;
  const r = (size - thickness) / 2;
  const circumference = 2 * Math.PI * r;

  let cumulative = 0;
  const arcs = slices.map((s) => {
    const fraction = s.count / total;
    const dashArray = `${circumference * fraction} ${circumference}`;
    const dashOffset = -circumference * cumulative;
    cumulative += fraction;
    return { slice: s, dashArray, dashOffset };
  });

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`}>
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke="color-mix(in oklch, var(--fg3) 8%, transparent)"
          strokeWidth={thickness}
        />
        {arcs.map(({ slice, dashArray, dashOffset }) => (
          <circle
            key={slice.label}
            cx={cx}
            cy={cy}
            r={r}
            fill="none"
            stroke={slice.color}
            strokeWidth={thickness}
            strokeDasharray={dashArray}
            strokeDashoffset={dashOffset}
            transform={`rotate(-90 ${cx} ${cy})`}
            strokeLinecap="butt"
            opacity={0.9}
          />
        ))}
        {centerValue ? (
          <>
            <text
              x={cx}
              y={cy - 4}
              textAnchor="middle"
              style={{
                fontFamily: "var(--serif-display)",
                fontSize: 26,
                fontWeight: 600,
                fontVariationSettings: '"opsz" 36',
                fill: "var(--fg1)",
              }}
            >
              {centerValue}
            </text>
            {centerTitle ? (
              <text
                x={cx}
                y={cy + 18}
                textAnchor="middle"
                style={{
                  fontFamily: "var(--mono)",
                  fontSize: 10,
                  letterSpacing: "0.08em",
                  textTransform: "uppercase",
                  fill: "var(--fg3)",
                }}
              >
                {centerTitle}
              </text>
            ) : null}
          </>
        ) : null}
      </svg>

      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: 6,
          width: "100%",
          maxWidth: 280,
        }}
      >
        {slices.map((s) => (
          <div
            key={s.label}
            style={{
              display: "grid",
              gridTemplateColumns: "12px 1fr auto",
              alignItems: "center",
              gap: 10,
              fontSize: 12.5,
            }}
          >
            <span
              style={{
                width: 10,
                height: 10,
                borderRadius: 2,
                background: s.color,
              }}
            />
            <span style={{ color: "var(--fg1)" }}>{s.label}</span>
            <span
              className="mono tabular"
              style={{ fontSize: 11.5, color: "var(--fg2)" }}
            >
              {s.count.toLocaleString("fr-FR").replace(/ /g, " ")} ·{" "}
              {s.pct.toFixed(1).replace(".", ",")} %
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
