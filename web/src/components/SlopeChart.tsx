"use client";

export interface SlopeItem {
  title: string;
  count: number;
}

interface Props {
  ma: SlopeItem[];
  intl: SlopeItem[];
  accentMA: string;
  accentINTL: string;
  nMA: number;
  nINTL: number;
}

const W = 1000;
const H = 460;
const PAD_TOP = 60;
const PAD_BOT = 24;
const LEFT_X = 280;
const RIGHT_X = W - 280;

export function SlopeChart({ ma, intl, accentMA, accentINTL, nMA, nINTL }: Props) {
  const rowH = (H - PAD_TOP - PAD_BOT) / Math.max(ma.length, intl.length, 1);

  const norm = (s: string) => s.toLowerCase().trim();
  const intlByTitle = new Map(intl.map((it, i) => [norm(it.title), i]));

  const links = ma
    .map((m, i) => {
      const intlRank = intlByTitle.get(norm(m.title));
      if (intlRank === undefined) return null;
      return {
        title: m.title,
        y1: PAD_TOP + i * rowH + rowH / 2,
        y2: PAD_TOP + intlRank * rowH + rowH / 2,
      };
    })
    .filter((x): x is { title: string; y1: number; y2: number } => x !== null);

  return (
    <div className="card" style={{ padding: "22px 26px", minHeight: 520 }}>
      <svg
        viewBox={`0 0 ${W} ${H}`}
        width="100%"
        style={{ display: "block", overflow: "visible" }}
      >
        {/* Headers MAROC / INTERNATIONAL */}
        <g>
          <line
            x1={LEFT_X - 200}
            x2={LEFT_X + 12}
            y1={PAD_TOP - 22}
            y2={PAD_TOP - 22}
            stroke={accentMA}
            strokeWidth={2}
          />
          <text
            x={LEFT_X - 200}
            y={PAD_TOP - 30}
            fontSize={13}
            fontWeight={700}
            fill={accentMA}
            letterSpacing={1.3}
            fontFamily="var(--sans-body)"
          >
            MAROC
          </text>
          <text
            x={LEFT_X + 12}
            y={PAD_TOP - 30}
            textAnchor="end"
            fontSize={11}
            fill="var(--fg3)"
            fontFamily="var(--mono)"
          >
            {`n = ${nMA}`}
          </text>

          <line
            x1={RIGHT_X - 12}
            x2={RIGHT_X + 200}
            y1={PAD_TOP - 22}
            y2={PAD_TOP - 22}
            stroke={accentINTL}
            strokeWidth={2}
          />
          <text
            x={RIGHT_X - 12}
            y={PAD_TOP - 30}
            fontSize={11}
            fill="var(--fg3)"
            fontFamily="var(--mono)"
          >
            {`n = ${nINTL.toLocaleString("fr-FR").replace(/ /g, " ")}`}
          </text>
          <text
            x={RIGHT_X + 200}
            y={PAD_TOP - 30}
            textAnchor="end"
            fontSize={13}
            fontWeight={700}
            fill={accentINTL}
            letterSpacing={1.3}
            fontFamily="var(--sans-body)"
          >
            INTERNATIONAL
          </text>
        </g>

        {/* Lignes */}
        {links.map((l) => {
          const direction = l.y1 - l.y2;
          const stroke =
            direction > 4
              ? accentINTL
              : direction < -4
                ? "var(--fg3)"
                : "var(--fg3)";
          const opacity = Math.abs(direction) > 4 ? 0.55 : 0.25;
          return (
            <line
              key={l.title}
              x1={LEFT_X}
              y1={l.y1}
              x2={RIGHT_X}
              y2={l.y2}
              stroke={stroke}
              strokeWidth={1.5}
              opacity={opacity}
            />
          );
        })}

        {/* Colonne gauche MA */}
        {ma.map((m, i) => {
          const y = PAD_TOP + i * rowH + rowH / 2;
          return (
            <g key={`ma-${m.title}`}>
              <circle cx={LEFT_X} cy={y} r={5.5} fill={accentMA} />
              <text
                x={LEFT_X - 16}
                y={y - 4}
                textAnchor="end"
                fontSize={13}
                fontWeight={i < 3 ? 600 : 400}
                fill="var(--fg1)"
                fontFamily="var(--sans-body)"
              >
                {m.title}
              </text>
              <text
                x={LEFT_X - 16}
                y={y + 12}
                textAnchor="end"
                fontSize={10.5}
                fill="var(--fg3)"
                fontFamily="var(--mono)"
                letterSpacing={0.5}
              >
                {`${m.count} offres`}
              </text>
            </g>
          );
        })}

        {/* Colonne droite INTL */}
        {intl.map((it, i) => {
          const y = PAD_TOP + i * rowH + rowH / 2;
          return (
            <g key={`intl-${it.title}`}>
              <circle cx={RIGHT_X} cy={y} r={5.5} fill={accentINTL} />
              <text
                x={RIGHT_X + 16}
                y={y - 4}
                fontSize={13}
                fontWeight={i < 3 ? 600 : 400}
                fill="var(--fg1)"
                fontFamily="var(--sans-body)"
              >
                {it.title}
              </text>
              <text
                x={RIGHT_X + 16}
                y={y + 12}
                fontSize={10.5}
                fill="var(--fg3)"
                fontFamily="var(--mono)"
                letterSpacing={0.5}
              >
                {`${it.count.toLocaleString("fr-FR").replace(/ /g, " ")} offres`}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
