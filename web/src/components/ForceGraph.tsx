"use client";

import dynamic from "next/dynamic";
import { useEffect, useMemo, useRef, useState } from "react";

// react-force-graph-2d est canvas pur → client only, dynamic import sans SSR.
const ForceGraph2D = dynamic(() => import("react-force-graph-2d"), { ssr: false });

export interface RawNode {
  id: string;
  pagerank: number;
  community: number;
  family: string;
  count: number;
}

export interface RawLink {
  source: string;
  target: string;
  weight: number;
}

export interface ForceGraphData {
  nodes: RawNode[];
  links: RawLink[];
}

interface Props {
  data: ForceGraphData;
  /** Filtre famille (label exact ex "GenAI") ; null = toutes */
  familyFilter: string | null;
  /** Filtre community id ; null = toutes */
  communityFilter: number | null;
  /** Seuil minimal de weight pour afficher une arete (filtre densite) */
  weightThreshold: number;
  /** Couleur a appliquer selon `mode` : 'family' ou 'community' */
  colorMode: "family" | "community";
  /** Callback quand un noeud est cliqué */
  onSelectNode?: (node: RawNode | null) => void;
  /** Hauteur du canvas */
  height?: number;
}

// Palette familles (10 couleurs distinctes)
const FAMILY_COLORS: Record<string, string> = {
  GenAI: "#7C3AED",
  ML: "#2251FF",
  "Data Engineering": "#0F8F65",
  Cloud: "#C77700",
  Databases: "#0891B2",
  "Web & APIs": "#E11D48",
  "DevOps / MLOps": "#A16207",
  Languages: "#6D28D9",
  Domains: "#BE185D",
  Other: "#6B7280",
};

// Palette communautés (11 teintes douces)
const COMMUNITY_COLORS = [
  "#2251FF", "#C77700", "#0F8F65", "#7C3AED", "#E11D48",
  "#0891B2", "#A16207", "#6D28D9", "#15803D", "#BE185D",
  "#475569",
];

function colorForNode(node: RawNode, mode: "family" | "community"): string {
  if (mode === "family") {
    return FAMILY_COLORS[node.family] ?? FAMILY_COLORS.Other!;
  }
  return COMMUNITY_COLORS[node.community % COMMUNITY_COLORS.length]!;
}

export function ForceGraph({
  data,
  familyFilter,
  communityFilter,
  weightThreshold,
  colorMode,
  onSelectNode,
  height = 540,
}: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const fgRef = useRef<{ zoomToFit?: (ms?: number, padding?: number) => void } | null>(null);
  const [width, setWidth] = useState(800);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  // Resize observer pour responsive
  useEffect(() => {
    if (!containerRef.current) return;
    const ro = new ResizeObserver((entries) => {
      for (const e of entries) {
        setWidth(Math.max(200, Math.floor(e.contentRect.width)));
      }
    });
    ro.observe(containerRef.current);
    return () => ro.disconnect();
  }, []);

  // Filtrage nodes + links
  const filteredData = useMemo(() => {
    const passNode = (n: RawNode) => {
      if (familyFilter && n.family !== familyFilter) return false;
      if (communityFilter !== null && n.community !== communityFilter) return false;
      return true;
    };
    const nodesKept = data.nodes.filter(passNode);
    const idSet = new Set(nodesKept.map((n) => n.id));
    const linksKept = data.links.filter(
      (l) => l.weight >= weightThreshold && idSet.has(l.source) && idSet.has(l.target),
    );
    return { nodes: nodesKept, links: linksKept };
  }, [data, familyFilter, communityFilter, weightThreshold]);

  // Set des voisins du noeud sélectionné (highlight)
  const neighborIds = useMemo(() => {
    if (!selectedId) return new Set<string>();
    const s = new Set<string>([selectedId]);
    for (const l of filteredData.links) {
      if (l.source === selectedId) s.add(l.target);
      if (l.target === selectedId) s.add(l.source);
    }
    return s;
  }, [selectedId, filteredData.links]);

  // Mise à l'échelle PageRank → rayon
  const maxPagerank = useMemo(
    () => Math.max(...filteredData.nodes.map((n) => n.pagerank), 0.0001),
    [filteredData.nodes],
  );

  return (
    <div
      ref={containerRef}
      style={{
        width: "100%",
        height,
        borderRadius: 8,
        overflow: "hidden",
        background: "color-mix(in oklch, var(--fg3) 4%, transparent)",
        position: "relative",
      }}
    >
      <ForceGraph2D
        ref={fgRef as never}
        graphData={filteredData as never}
        width={width}
        height={height}
        backgroundColor="transparent"
        cooldownTicks={120}
        nodeRelSize={5}
        nodeVal={(n: RawNode) => 0.5 + (n.pagerank / maxPagerank) * 9}
        nodeLabel={(n: RawNode) =>
          `${n.id}<br/><span style="color:#aaa">${n.family} · community ${n.community} · ${n.count} offres · PageRank ${n.pagerank.toFixed(3)}</span>`
        }
        nodeColor={(n: RawNode) => {
          const isFaded = selectedId !== null && !neighborIds.has(n.id);
          const base = colorForNode(n, colorMode);
          return isFaded ? `color-mix(in oklch, ${base} 25%, transparent)` : base;
        }}
        linkColor={(l: RawLink) => {
          if (!selectedId) {
            return "color-mix(in oklch, var(--fg3) 22%, transparent)";
          }
          const touch =
            l.source === selectedId ||
            l.target === selectedId ||
            (typeof l.source === "object" && (l.source as RawNode).id === selectedId) ||
            (typeof l.target === "object" && (l.target as RawNode).id === selectedId);
          return touch
            ? "color-mix(in oklch, var(--fg1) 55%, transparent)"
            : "color-mix(in oklch, var(--fg3) 8%, transparent)";
        }}
        linkWidth={(l: RawLink) => Math.min(3, Math.max(0.3, l.weight * 0.18))}
        onNodeClick={(n) => {
          const node = n as RawNode;
          const newId = selectedId === node.id ? null : node.id;
          setSelectedId(newId);
          onSelectNode?.(newId ? node : null);
        }}
        onBackgroundClick={() => {
          setSelectedId(null);
          onSelectNode?.(null);
        }}
        nodeCanvasObjectMode={() => "after"}
        nodeCanvasObject={(rawNode, ctx, globalScale) => {
          const n = rawNode as unknown as RawNode & { x?: number; y?: number };
          if (n.x == null || n.y == null) return;
          // Label visible pour top PageRank (10 % les plus centraux) ou si zoom suffisant
          const shouldDraw = n.pagerank >= maxPagerank * 0.35 || globalScale > 2.5;
          if (!shouldDraw) return;
          const isFaded = selectedId !== null && !neighborIds.has(n.id);
          if (isFaded) return;
          const fontSize = Math.min(13, 9 + n.pagerank / maxPagerank * 5) / globalScale;
          ctx.font = `${fontSize}px Inter, system-ui, sans-serif`;
          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          const radius = 5 * (0.5 + (n.pagerank / maxPagerank) * 9) ** 0.5;
          ctx.fillStyle = "var(--fg1, #fff)";
          ctx.fillText(n.id, n.x, n.y + radius + fontSize * 0.9);
        }}
      />
    </div>
  );
}
