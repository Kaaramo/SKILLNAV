"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  BookOpen,
  Download,
  GitFork,
  LayoutDashboard,
  LineChart as LineChartIcon,
  Moon,
  Network,
  Sun,
  Target,
  type LucideIcon,
} from "lucide-react";
import type { ReactNode } from "react";
import { useTheme } from "./ThemeProvider";
import { RouteTransitionLoader } from "./RouteTransitionLoader";

interface NavItem {
  href: string;
  label: string;
  Icon: LucideIcon;
  eyebrow: string;
  title: string;
}

export const NAV_ITEMS: NavItem[] = [
  {
    href: "/",
    label: "Vue d'ensemble",
    Icon: LayoutDashboard,
    eyebrow: "",
    title: "Vue d'ensemble",
  },
  {
    href: "/skills",
    label: "Compétences",
    Icon: Network,
    eyebrow: "",
    title: "Catalogue des compétences",
  },
  {
    href: "/graph",
    label: "Graphe",
    Icon: GitFork,
    eyebrow: "Structure Mining · Louvain Q = 0,256",
    title: "Graphe des compétences",
  },
  {
    href: "/forecasting",
    label: "Prévisions",
    Icon: LineChartIcon,
    eyebrow: "Usage Mining · ARIMA RMSE 17,21",
    title: "Quel modèle prévoit le mieux ?",
  },
  {
    href: "/gap",
    label: "Gap Analysis",
    Icon: Target,
    eyebrow: "",
    title: "Gap Analysis : curricula vs marché",
  },
  {
    href: "/methodology",
    label: "Méthodologie",
    Icon: BookOpen,
    eyebrow: "3 axes · 7 sources · 4 études comparatives §N2",
    title: "Méthodologie",
  },
];

function Sidebar() {
  const pathname = usePathname();
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand">SKILLNAV</div>
      </div>
      <nav className="nav">
        {NAV_ITEMS.map((n) => {
          const isActive = pathname === n.href;
          const Icon = n.Icon;
          return (
            <Link key={n.href} href={n.href} className={isActive ? "nav-link active" : "nav-link"}>
              <Icon size={16} strokeWidth={1.5} />
              {n.label}
            </Link>
          );
        })}
      </nav>
      <div className="sidebar-tagline">
        Observatoire de compétences Data Science &amp; Intelligence Artificielle
      </div>
    </aside>
  );
}

function PageHeader() {
  const pathname = usePathname();
  const cfg = NAV_ITEMS.find((n) => n.href === pathname) ?? NAV_ITEMS[0]!;
  const { theme, toggle } = useTheme();
  const isSkills = pathname === "/skills";
  return (
    <header className="header">
      <div className="header-titles">
        {cfg.eyebrow ? <div className="page-eyebrow">{cfg.eyebrow}</div> : null}
        <div className="page-title">{cfg.title}</div>
      </div>
      {isSkills ? null : <span className="period-pill">Jan 2023 — Mai 2026</span>}
      <button className="icon-btn" onClick={toggle} aria-label="Thème">
        {theme === "dark" ? <Sun size={16} strokeWidth={1.5} /> : <Moon size={16} strokeWidth={1.5} />}
      </button>
      <button className="icon-btn" aria-label="Exporter">
        <Download size={16} strokeWidth={1.5} />
      </button>
    </header>
  );
}

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="shell">
      <Sidebar />
      <div className="main">
        <PageHeader />
        <main className="content">
          <RouteTransitionLoader>{children}</RouteTransitionLoader>
        </main>
      </div>
    </div>
  );
}
