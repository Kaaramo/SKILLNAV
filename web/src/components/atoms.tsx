"use client";

import type { CSSProperties, ReactNode } from "react";
import { FAMILIES, type FamilyKey } from "@/lib/mockData";

export function Eyebrow({ children, style }: { children: ReactNode; style?: CSSProperties }) {
  return (
    <div className="eyebrow" style={style}>
      {children}
    </div>
  );
}

export function FPill({
  fam,
  dense = false,
  outline = false,
}: {
  fam: FamilyKey;
  dense?: boolean;
  outline?: boolean;
}) {
  const F = FAMILIES[fam];
  return (
    <span
      className={`fpill ${F.cls} ${outline ? "" : "solid"}`}
      style={dense ? { height: 22, fontSize: 11, padding: "0 10px" } : undefined}
    >
      {F.lbl}
    </span>
  );
}

export interface ContextItem {
  label: string;
  value: ReactNode;
}

export function ContextStrip({ items, actions }: { items: ContextItem[]; actions?: ReactNode }) {
  return (
    <div className="context-strip">
      <div className="items">
        {items.map((it, i) => (
          <span key={i} className="item">
            <span className="label">{it.label}</span>
            <span>{it.value}</span>
          </span>
        ))}
      </div>
      {actions ? <div className="actions">{actions}</div> : null}
    </div>
  );
}

export function SectionRule({
  eyebrow,
  title,
  right,
}: {
  eyebrow?: ReactNode;
  title: ReactNode;
  right?: ReactNode;
}) {
  return (
    <div className="section-rule">
      <div>
        {eyebrow ? <Eyebrow>{eyebrow}</Eyebrow> : null}
        <h2>{title}</h2>
      </div>
      {right ? <div className="right">{right}</div> : null}
    </div>
  );
}

export function MethodFooter({ items }: { items: ReactNode[] }) {
  return (
    <div className="method-footer">
      <div className="left">
        {items.map((it, i) => (
          <span key={i}>{it}</span>
        ))}
      </div>
      <span>SKILLNAV · M242 · Sylla &amp; Konaté</span>
    </div>
  );
}

export function KPICard({
  eyebrow,
  value,
  unit,
  delta,
  deltaDir = "up",
  foot,
  size = "lg",
  accent = false,
}: {
  eyebrow: ReactNode;
  value: ReactNode;
  unit?: ReactNode;
  delta?: ReactNode;
  deltaDir?: "up" | "down";
  foot?: ReactNode;
  size?: "lg" | "md" | "sm";
  accent?: boolean;
}) {
  return (
    <div className="kpi-card">
      <Eyebrow>{eyebrow}</Eyebrow>
      <div className="kpi-row">
        <span className={`kpi-num ${size} ${accent ? "accent" : ""}`}>{value}</span>
        {unit ? <span className="kpi-unit">{unit}</span> : null}
      </div>
      <div className="kpi-foot">
        {delta != null ? <span className={`kpi-delta ${deltaDir}`}>{delta}</span> : <span />}
        {foot ? <span className="kpi-n">{foot}</span> : null}
      </div>
    </div>
  );
}

export function ScoreBar({ value, success = false }: { value: number; success?: boolean }) {
  const pct = Math.max(0, Math.min(1, value)) * 100;
  return (
    <span className={`score-bar ${success ? "success" : ""}`}>
      <span className="b">
        <i style={{ width: `${pct}%` }} />
      </span>
      <span className="v">{value.toFixed(2)}</span>
    </span>
  );
}

export interface SegOption<T extends string> {
  value: T;
  label: ReactNode;
}

export function Segmented<T extends string>({
  options,
  value,
  onChange,
}: {
  options: SegOption<T>[];
  value: T;
  onChange: (v: T) => void;
}) {
  return (
    <div className="seg">
      {options.map((o) => (
        <button
          key={o.value}
          className={value === o.value ? "active" : ""}
          onClick={() => onChange(o.value)}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

export function CheckRow({
  label,
  count,
  on,
  onToggle,
}: {
  label: ReactNode;
  count?: number | string;
  on?: boolean;
  onToggle?: () => void;
}) {
  return (
    <div className="filter-row" onClick={onToggle} style={{ cursor: onToggle ? "pointer" : undefined }}>
      <span style={{ display: "inline-flex", alignItems: "center", gap: 10 }}>
        <span className={`check ${on ? "on" : ""}`}>
          {on ? (
            <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          ) : null}
        </span>
        {label}
      </span>
      {count != null ? <span className="count">{count}</span> : null}
    </div>
  );
}

export function RangeMock({
  min = 0.7,
  max = 0.9,
  lo = 0.7,
  hi = 0.9,
}: {
  min?: number;
  max?: number;
  lo?: number;
  hi?: number;
}) {
  const left = ((lo - min) / (max - min)) * 100;
  const right = ((hi - min) / (max - min)) * 100;
  return (
    <div>
      <div className="range">
        <div className="track">
          <div className="fill" style={{ left: `${left}%`, width: `${right - left}%` }} />
          <div className="knob" style={{ left: `${left}%` }} />
          <div className="knob" style={{ left: `${right}%` }} />
        </div>
      </div>
      <div className="range-row">
        <span>{lo.toFixed(2)}</span>
        <span>{hi.toFixed(2)}</span>
      </div>
    </div>
  );
}
