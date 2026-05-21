"use client";

import { useMemo, useState } from "react";
import { Segmented } from "@/components/atoms";
import { ForceGraph, type RawNode } from "@/components/ForceGraph";
import graphData from "@/lib/graph_vis.json";

interface GraphJSON {
  nodes: RawNode[];
  links: { source: string; target: string; weight: number }[];
}

const DATA = graphData as unknown as GraphJSON;

// Stats agregees calculees a partir du JSON brut (sans supposition)
const STATS = (() => {
  const nodes = DATA.nodes;
  const families = new Set(nodes.map((n) => n.family));
  const communities = new Set(nodes.map((n) => n.community));
  const topByPagerank = [...nodes].sort((a, b) => b.pagerank - a.pagerank).slice(0, 10);

  // Pour chaque communaute : top skill + taille + 3 autres
  const byCommunity = new Map<number, RawNode[]>();
  for (const n of nodes) {
    if (!byCommunity.has(n.community)) byCommunity.set(n.community, []);
    byCommunity.get(n.community)!.push(n);
  }
  const communityStats = [...byCommunity.entries()]
    .map(([id, ns]) => {
      const sorted = [...ns].sort((a, b) => b.pagerank - a.pagerank);
      return {
        id,
        size: ns.length,
        leader: sorted[0]!,
        next: sorted.slice(1, 4),
      };
    })
    .sort((a, b) => b.size - a.size);

  return {
    nNodes: nodes.length,
    nLinks: DATA.links.length,
    nFamilies: families.size,
    nCommunities: communities.size,
    topByPagerank,
    communityStats,
    familyList: [...families].sort(),
  };
})();

// Modularite Leiden (V1 retenu, rapport §4.3) : Q = 0,2988 sur graphe complet (3 937 nœuds)
const MODULARITY_LEIDEN = 0.2988;

type ColorMode = "family" | "community";

export default function GraphPage() {
  const [familyFilter, setFamilyFilter] = useState<string | null>(null);
  const [communityFilter, setCommunityFilter] = useState<number | null>(null);
  const [weightThreshold, setWeightThreshold] = useState<number>(3);
  const [colorMode, setColorMode] = useState<ColorMode>("family");
  const [selected, setSelected] = useState<RawNode | null>(null);

  // Neighbors du noeud sélectionné triés par poids decroissant
  const neighbors = useMemo(() => {
    if (!selected) return [];
    const out: { id: string; weight: number; node: RawNode | undefined }[] = [];
    for (const l of DATA.links) {
      let other: string | null = null;
      if (l.source === selected.id) other = l.target;
      else if (l.target === selected.id) other = l.source;
      if (other) {
        out.push({
          id: other,
          weight: l.weight,
          node: DATA.nodes.find((n) => n.id === other),
        });
      }
    }
    return out.sort((a, b) => b.weight - a.weight).slice(0, 8);
  }, [selected]);

  return (
    <>
      {/* KPI strip — carte d'identité du graphe */}
      <div
        className="kpi-grid"
        style={{ gridTemplateColumns: "repeat(5, minmax(0, 1fr))" }}
      >
        <KPI label="Nœuds" value={STATS.nNodes.toString()} sub="compétences cartographiées" />
        <KPI label="Arêtes" value={STATS.nLinks.toLocaleString("fr-FR")} sub="co-occurrences pondérées" />
        <KPI label="Communautés" value={STATS.nCommunities.toString()} sub="détectées par Leiden" />
        <KPI label="Modularité Q" value={MODULARITY_LEIDEN.toFixed(3).replace(".", ",")} sub="qualité du partitionnement" />
        <KPI
          label="Skill #1"
          value={STATS.topByPagerank[0]?.id ?? "—"}
          sub={`PageRank ${STATS.topByPagerank[0]?.pagerank.toFixed(3).replace(".", ",")} · ${STATS.topByPagerank[0]?.count ?? 0} mentions`}
          accent
        />
      </div>

      {/* Toolbar */}
      <div
        style={{
          display: "flex",
          gap: 18,
          flexWrap: "wrap",
          alignItems: "center",
          marginTop: 26,
          marginBottom: 18,
          padding: "12px 14px",
          background: "color-mix(in oklch, var(--fg3) 5%, transparent)",
          borderRadius: 8,
        }}
      >
        <span style={toolLabelStyle}>Coloration</span>
        <Segmented<ColorMode>
          options={[
            { value: "family", label: "Famille" },
            { value: "community", label: "Communauté" },
          ]}
          value={colorMode}
          onChange={setColorMode}
        />
        <span style={{ ...toolLabelStyle, marginLeft: 20 }}>
          Seuil cooccurrence ≥{" "}
          <span className="mono tabular" style={{ color: "var(--fg1)" }}>
            {weightThreshold}
          </span>
        </span>
        <input
          type="range"
          min={1}
          max={20}
          step={1}
          value={weightThreshold}
          onChange={(e) => setWeightThreshold(Number(e.target.value))}
          style={{ width: 180 }}
        />
        <span style={{ ...toolLabelStyle, marginLeft: 20 }}>Famille</span>
        <select
          value={familyFilter ?? ""}
          onChange={(e) => setFamilyFilter(e.target.value || null)}
          style={selectStyle}
        >
          <option value="">Toutes ({STATS.nFamilies})</option>
          {STATS.familyList.map((f) => (
            <option key={f} value={f}>
              {f}
            </option>
          ))}
        </select>
        <span style={{ ...toolLabelStyle, marginLeft: 8 }}>Communauté</span>
        <select
          value={communityFilter === null ? "" : String(communityFilter)}
          onChange={(e) =>
            setCommunityFilter(e.target.value === "" ? null : Number(e.target.value))
          }
          style={selectStyle}
        >
          <option value="">Toutes ({STATS.nCommunities})</option>
          {STATS.communityStats.map((c) => (
            <option key={c.id} value={c.id}>
              {`#${c.id} · ${c.leader.id} · ${c.size} skills`}
            </option>
          ))}
        </select>
        {(familyFilter || communityFilter !== null) && (
          <button
            onClick={() => {
              setFamilyFilter(null);
              setCommunityFilter(null);
            }}
            style={{
              marginLeft: "auto",
              fontFamily: "var(--mono)",
              fontSize: 11,
              padding: "6px 10px",
              borderRadius: 4,
              border: "1px solid var(--fg3)",
              background: "transparent",
              color: "var(--fg2)",
              cursor: "pointer",
            }}
          >
            Réinitialiser filtres
          </button>
        )}
      </div>

      {/* Graphe interactif + panneau Sélection */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(0, 1fr) 280px",
          gap: 20,
          marginBottom: 28,
        }}
      >
        <ForceGraph
          data={DATA}
          familyFilter={familyFilter}
          communityFilter={communityFilter}
          weightThreshold={weightThreshold}
          colorMode={colorMode}
          onSelectNode={setSelected}
          height={540}
        />

        <div
          className="card"
          style={{ padding: "18px 20px", display: "flex", flexDirection: "column", gap: 10 }}
        >
          {selected ? (
            <>
              <div
                style={{
                  fontFamily: "var(--mono)",
                  fontSize: 11,
                  color: "var(--fg3)",
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                }}
              >
                Sélection
              </div>
              <div
                style={{
                  fontFamily: "var(--serif-display)",
                  fontSize: 24,
                  fontWeight: 600,
                  color: "var(--fg1)",
                  lineHeight: 1.15,
                }}
              >
                {selected.id}
              </div>
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: 6,
                  fontSize: 12,
                  color: "var(--fg2)",
                  marginTop: 2,
                }}
              >
                <KV label="Famille" value={selected.family} />
                <KV label="Communauté" value={`#${selected.community}`} />
                <KV label="Mentions" value={selected.count.toString()} />
                <KV label="PageRank" value={selected.pagerank.toFixed(4).replace(".", ",")} />
              </div>
              <div
                style={{
                  marginTop: 14,
                  paddingTop: 12,
                  borderTop: "1px solid color-mix(in oklch, var(--fg3) 12%, transparent)",
                }}
              >
                <div
                  style={{
                    fontFamily: "var(--mono)",
                    fontSize: 11,
                    color: "var(--fg3)",
                    textTransform: "uppercase",
                    letterSpacing: "0.08em",
                    marginBottom: 8,
                  }}
                >
                  Top 8 voisins
                </div>
                {neighbors.length === 0 ? (
                  <div style={{ fontSize: 11.5, color: "var(--fg3)", fontStyle: "italic" }}>
                    Aucun voisin sous le seuil actuel
                  </div>
                ) : (
                  <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                    {neighbors.map((nb) => (
                      <div
                        key={nb.id}
                        style={{
                          display: "flex",
                          justifyContent: "space-between",
                          fontSize: 12.5,
                        }}
                      >
                        <span style={{ color: "var(--fg1)" }}>{nb.id}</span>
                        <span className="mono tabular" style={{ color: "var(--fg3)" }}>
                          {nb.weight}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </>
          ) : (
            <>
              <div
                style={{
                  fontFamily: "var(--mono)",
                  fontSize: 11,
                  color: "var(--fg3)",
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                }}
              >
                Légende
              </div>
              <div style={{ fontSize: 12.5, color: "var(--fg2)", lineHeight: 1.6 }}>
                <strong style={{ color: "var(--fg1)" }}>● Taille</strong> ∝ PageRank
                <br />
                <strong style={{ color: "var(--fg1)" }}>● Couleur</strong> ={" "}
                {colorMode === "family" ? "famille de compétences" : "communauté Louvain"}
                <br />
                <strong style={{ color: "var(--fg1)" }}>— Épaisseur</strong> ∝ co-occurrence
              </div>
              <div
                style={{
                  fontSize: 11,
                  color: "var(--fg3)",
                  marginTop: 10,
                  fontStyle: "italic",
                  lineHeight: 1.5,
                }}
              >
                Cliquez sur un nœud pour voir ses voisins. Cliquez sur le fond pour désélectionner.
              </div>
            </>
          )}
        </div>
      </div>

      {/* Top 10 PageRank + Communautés en grille */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(0, 1fr) minmax(0, 1.4fr)",
          gap: 20,
          marginBottom: 28,
        }}
      >
        {/* Top 10 PageRank */}
        <div className="card" style={{ padding: "18px 20px" }}>
          <div
            style={{
              fontFamily: "var(--mono)",
              fontSize: 11,
              color: "var(--fg3)",
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              marginBottom: 12,
            }}
          >
            Top 10 PageRank
          </div>
          <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
            {STATS.topByPagerank.map((n, i) => (
              <div
                key={n.id}
                style={{
                  display: "grid",
                  gridTemplateColumns: "22px 1fr auto",
                  alignItems: "center",
                  gap: 10,
                  fontSize: 12.5,
                  padding: "3px 0",
                  borderBottom:
                    i < 9
                      ? "1px solid color-mix(in oklch, var(--fg3) 6%, transparent)"
                      : "none",
                }}
              >
                <span
                  className="mono tabular"
                  style={{ fontSize: 10.5, color: "var(--fg3)", textAlign: "right" }}
                >
                  #{i + 1}
                </span>
                <span style={{ color: "var(--fg1)", fontWeight: i < 3 ? 600 : 400 }}>
                  {n.id}
                </span>
                <span
                  className="mono tabular"
                  style={{ fontSize: 11.5, color: "var(--fg2)", whiteSpace: "nowrap" }}
                >
                  {n.pagerank.toFixed(3).replace(".", ",")}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Communautés Louvain */}
        <div className="card" style={{ padding: "18px 20px" }}>
          <div
            style={{
              fontFamily: "var(--mono)",
              fontSize: 11,
              color: "var(--fg3)",
              textTransform: "uppercase",
              letterSpacing: "0.08em",
              marginBottom: 12,
            }}
          >
            {STATS.nCommunities} communautés Leiden
          </div>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
              gap: 10,
            }}
          >
            {STATS.communityStats.map((c) => {
              const isActive = communityFilter === c.id;
              return (
                <button
                  key={c.id}
                  onClick={() =>
                    setCommunityFilter(communityFilter === c.id ? null : c.id)
                  }
                  style={{
                    textAlign: "left",
                    padding: "10px 12px",
                    borderRadius: 6,
                    border: isActive
                      ? "2px solid var(--skn-royal, #2251FF)"
                      : "1px solid color-mix(in oklch, var(--fg3) 14%, transparent)",
                    background: isActive
                      ? "color-mix(in oklch, var(--skn-royal, #2251FF) 9%, transparent)"
                      : "transparent",
                    cursor: "pointer",
                    fontFamily: "var(--sans-body)",
                    color: "var(--fg1)",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      alignItems: "baseline",
                      marginBottom: 4,
                    }}
                  >
                    <span
                      className="mono"
                      style={{ fontSize: 10.5, color: "var(--fg3)" }}
                    >
                      #{c.id}
                    </span>
                    <span
                      className="mono tabular"
                      style={{ fontSize: 10.5, color: "var(--fg3)" }}
                    >
                      {c.size} skills
                    </span>
                  </div>
                  <div style={{ fontSize: 13, fontWeight: 600, marginBottom: 4 }}>
                    {c.leader.id}
                  </div>
                  <div style={{ fontSize: 11, color: "var(--fg3)", lineHeight: 1.35 }}>
                    {c.next.map((n) => n.id).join(" · ")}
                  </div>
                </button>
              );
            })}
          </div>
        </div>
      </div>

    </>
  );
}

// ───────── helpers locaux ─────────

const toolLabelStyle = {
  fontFamily: "var(--mono)",
  fontSize: 11,
  color: "var(--fg3)",
  textTransform: "uppercase" as const,
  letterSpacing: "0.08em",
};

const selectStyle = {
  fontFamily: "var(--sans-body)",
  fontSize: 12.5,
  padding: "6px 8px",
  borderRadius: 4,
  border: "1px solid color-mix(in oklch, var(--fg3) 22%, transparent)",
  background: "var(--bg, transparent)",
  color: "var(--fg1)",
  cursor: "pointer",
  maxWidth: 260,
};

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
          wordBreak: "break-word",
        }}
      >
        {value}
      </div>
      <div
        style={{
          fontSize: 11.5,
          color: "var(--fg2)",
          marginTop: 6,
        }}
      >
        {sub}
      </div>
    </div>
  );
}

function KV({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between" }}>
      <span style={{ color: "var(--fg3)" }}>{label}</span>
      <span style={{ color: "var(--fg1)", fontWeight: 500 }}>{value}</span>
    </div>
  );
}
