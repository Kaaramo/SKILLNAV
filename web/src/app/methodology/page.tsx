"use client";

import { Fragment, useState, type ReactNode } from "react";

const COL_CONTENT = "#7C3AED"; // axe Content Mining (NLP)
const COL_STRUCTURE = "#2251FF"; // axe Structure Mining (graphes)
const COL_USAGE = "#0F8F65"; // axe Usage Mining (forecasting)
const COL_GOLD = "#C77700";
const COL_FG3 = "var(--fg3)";

const AXES = [
  {
    key: "content",
    color: COL_CONTENT,
    num: "1",
    title: "Content Mining",
    question: "Que dit le texte ?",
    subtitle: "Extraire le sens du texte des offres",
    desc:
      "À partir du texte brut de chaque offre d'emploi, on identifie les compétences techniques (Python, RAG, Kubernetes…), les outils, les frameworks, les entreprises. C'est l'étape qui transforme du texte en données structurées.",
    algos: ["BERT multilingue", "CamemBERT-NER", "DistilBERT-NER", "GLiNER (bonus zero-shot)"],
    href: "/ner",
    pageLabel: "NER Explorer",
  },
  {
    key: "structure",
    color: COL_STRUCTURE,
    num: "2",
    title: "Structure Mining",
    question: "Comment les compétences sont-elles connectées ?",
    subtitle: "Cartographier le réseau des compétences",
    desc:
      "Une fois les compétences extraites, on construit un graphe où deux compétences sont reliées si elles apparaissent dans la même offre. PageRank identifie les compétences centrales, Louvain regroupe en communautés cohérentes.",
    algos: ["PageRank (α=0,85)", "Louvain", "Leiden", "Label Propagation"],
    href: "/graph",
    pageLabel: "Graphe des compétences",
  },
  {
    key: "usage",
    color: COL_USAGE,
    num: "3",
    title: "Usage Mining",
    question: "Comment évoluent-elles dans le temps ?",
    subtitle: "Prédire l'évolution du marché",
    desc:
      "On agrège les offres par semaine pour les 10 compétences les plus centrales du marché IA, puis on compare 3 modèles de prévision pour anticiper les 4 semaines suivantes. Sortie : courbes avec intervalle de confiance.",
    algos: ["ARIMA (auto AIC)", "Prophet (Meta)", "LSTM (PyTorch)"],
    href: "/forecasting",
    pageLabel: "Prévisions",
  },
] as const;

const PIPELINE_STEPS = [
  { n: 1, title: "Collecte multi-sources", desc: "Crawl4AI · Playwright · Firecrawl · Apify · Wayback Machine", side: "Karamo" },
  { n: 2, title: "Ingestion + dédup", desc: "Validation Pydantic v2 → MongoDB · dédup SHA-256 (company + title + location + month)", side: "Karamo" },
  { n: 3, title: "Extraction IA structurée", desc: "Pydantic AI + Claude Sonnet 4.5 → schémas typés (skills, frameworks, modèles, entreprise…)", side: "Karamo" },
  { n: 4, title: "NER comparatif", desc: "BERT-multi · CamemBERT · DistilBERT · GLiNER → choix du meilleur sur 30 fiches gold", side: "Karamo" },
  { n: 5, title: "Graphe Skill ↔ Skill", desc: "Co-occurrences pondérées → PageRank + 3 algos de communautés → push Neo4j AuraDB", side: "Bachirou" },
  { n: 6, title: "Forecasting", desc: "Séries hebdo top 10 PageRank → ARIMA / Prophet / LSTM comparés → modèle retenu", side: "Bachirou" },
  { n: 7, title: "Pré-calcul JSON dashboard", desc: "Snapshots versionnés dans web/src/lib/*.json (overview, top_skills, gap, graph_vis, forecast_top10, ner_snapshot)", side: "Karamo" },
  { n: 8, title: "Dashboard Next.js 16", desc: "8 pages interactives · React 19 + Turbopack · composants SVG natifs + react-force-graph-2d", side: "Karamo" },
];

const SOURCES = [
  { name: "Rekrute", origine: "Maroc", n: 27, methode: "Crawl4AI", periode: "2023-2026" },
  { name: "LinkedIn MA", origine: "Maroc", n: 207, methode: "Apify (LinkedIn Jobs Scraper)", periode: "2023-2026" },
  { name: "Indeed MA", origine: "Maroc", n: 67, methode: "Crawl4AI + Wayback", periode: "2023-2026" },
  { name: "Glassdoor MA", origine: "Maroc", n: 72, methode: "Firecrawl (JS rendering)", periode: "2023-2026" },
  { name: "Anapec", origine: "Maroc", n: 2, methode: "Crawl4AI", periode: "2023-2026" },
  { name: "Pages-carrières MA", origine: "Maroc", n: 6, methode: "Playwright manuel", periode: "2023-2026" },
  { name: "intl-ai-corpus", origine: "International", n: 3087, methode: "builtin.com via Firecrawl", periode: "Q1 2026" },
];

const ETUDES = [
  { ref: "01", titre: "NER multilingue", algos: "BERT-multi · CamemBERT · DistilBERT", metric: "F1 = 0,463", winner: "DistilBERT-NER", color: COL_CONTENT, href: "/ner" },
  { ref: "02", titre: "Communautés du graphe", algos: "Louvain · Leiden · Label Propagation", metric: "Q = 0,295", winner: "Louvain", color: COL_STRUCTURE, href: "/graph" },
  { ref: "03", titre: "Forecasting séries temporelles", algos: "ARIMA · Prophet · LSTM", metric: "RMSE médian 17,21", winner: "ARIMA", color: COL_USAGE, href: "/forecasting" },
  { ref: "04", titre: "Détection compétences émergentes", algos: "Heuristique · XGBoost · KMeans temporel", metric: "à venir", winner: "—", color: COL_GOLD, href: null },
];

const LIMITES = [
  { titre: "Volume marché marocain", desc: "381 offres MA collectées sur 41 mois — corpus solide mais petit en absolu. Les conclusions MA s'appuient sur un échantillon non-exhaustif." },
  { titre: "Profondeur internationale", desc: "Le corpus INTL (3 086 offres) couvre principalement Q1 2026 (builtin.com). Pas d'historique 2023-2025 INTL pour comparer pre/post-ChatGPT côté INTL." },
  { titre: "Biais linguistique", desc: "50 % FR (côté MA) + 50 % EN (côté INTL). Les modèles NER varient en performance selon la langue (cf. paradoxe DistilBERT > CamemBERT)." },
  { titre: "Biais plateforme", desc: "LinkedIn MA surreprésenté (207/381 offres MA). Tend à favoriser les profils ESN (Capgemini, ALTEN). Plateformes locales (Anapec) sous-couvertes." },
  { titre: "Biais sectoriel", desc: "Le scope ciblé (Data Science + IA) exclut les profils Dev classiques. Les chiffres ne sont pas généralisables au marché tech global marocain." },
  { titre: "Canonicalisation imparfaite INTL", desc: "Le corpus INTL n'a pas le même niveau de canonicalisation que MA. Variants (`.NET`, `.NET Core`, `.Net`) comptés séparément, gonflant artificiellement le vocabulaire INTL." },
];

const RGPD_POINTS = [
  { titre: "User-Agent identifié", desc: "SkillnavBot/1.0 (Academic; ENSA-Tetouan) — identification transparente sur chaque requête." },
  { titre: "Crawl-delay respecté", desc: "5 secondes minimum entre 2 requêtes vers une même source. Respect strict des robots.txt." },
  { titre: "Aucune donnée candidate", desc: "Pas de nom, email, téléphone, photo, profil LinkedIn personnel. Seules les entités morales (employeurs) et les descriptions publiques d'offres sont collectées." },
  { titre: "Dédup par hash SHA-256", desc: "Identifiants techniques basés sur (company + title + location + month) — pas de PII candidat dans les clés." },
  { titre: "Conformité robots.txt", desc: "Sources documentées dans sources/registry.yaml. Pré-vol de chaque source avant scraping pour vérifier l'autorisation." },
  { titre: "DPIA disponible", desc: "Analyse d'impact à la protection des données dans docs/RGPD_DPIA.md — couverture des risques + mesures de minimisation." },
];

const GLOSSARY: { term: string; def: string }[] = [
  { term: "NER", def: "Named Entity Recognition · Reconnaissance d'entités nommées. Tâche NLP qui consiste à repérer dans un texte les mots qui désignent un nom propre (entreprise), un concept technique (Python), un lieu, etc." },
  { term: "F1 score", def: "Moyenne harmonique de la précision et du rappel. Va de 0 à 1. Plus c'est élevé, mieux le modèle équilibre les deux. Le PRD demande F1 ≥ 0,15." },
  { term: "Précision", def: "Sur toutes les entités prédites par le modèle, quelle proportion est correcte ?" },
  { term: "Rappel", def: "Sur toutes les entités à trouver (gold), quelle proportion le modèle a-t-il effectivement détectée ?" },
  { term: "PageRank", def: "Algorithme de Larry Page (Google) qui mesure l'importance d'un nœud dans un graphe selon le nombre + l'importance de ses voisins. Adapté ici aux compétences." },
  { term: "Modularité Q", def: "Mesure (Newman) de qualité d'un partitionnement d'un graphe en communautés. Va de -0,5 à 1. Plus c'est haut, mieux les groupes sont distincts." },
  { term: "Louvain", def: "Algorithme glouton qui optimise la modularité Q pour découvrir des communautés dans un graphe. Méthode de référence en analyse de réseaux." },
  { term: "ARIMA", def: "AutoRegressive Integrated Moving Average. Modèle statistique classique de prévision sur séries temporelles. Combine valeurs passées + erreurs passées + différences." },
  { term: "Prophet", def: "Modèle de Meta (Facebook) qui décompose une série en tendance + saisonnalité + effets ponctuels. Particulièrement adapté aux séries business." },
  { term: "LSTM", def: "Long Short-Term Memory. Réseau de neurones récurrent capable de mémoriser des patterns longue durée. Ici utilisé via neuralforecast / PyTorch." },
  { term: "RMSE", def: "Root Mean Squared Error. Écart quadratique moyen entre prédiction et réalité. Plus c'est bas, plus le modèle est précis." },
  { term: "IC 95 %", def: "Intervalle de confiance à 95 %. Plage dans laquelle la vraie valeur tombe 95 fois sur 100 si on répète l'expérience. Zone colorée semi-transparente sur les graphes /forecasting." },
  { term: "Pydantic v2", def: "Bibliothèque Python de validation de données par types. Sert de source de vérité unique pour tous les schémas du projet (jobs, NER, graphe, séries)." },
  { term: "Wayback Machine", def: "Archive.org. Snapshots datés du web depuis 1996. Source critique pour récupérer les offres expirées (LinkedIn ne les conserve pas)." },
  { term: "RGPD", def: "Règlement Général sur la Protection des Données (UE 2016/679). Cadre légal qui régit la collecte et le traitement de données personnelles." },
];

export default function MethodologyPage() {
  const [openGloss, setOpenGloss] = useState<Set<number>>(new Set());

  const toggleGloss = (i: number) => {
    setOpenGloss((prev) => {
      const next = new Set(prev);
      if (next.has(i)) next.delete(i);
      else next.add(i);
      return next;
    });
  };

  return (
    <>
      {/* Hero */}
      <section style={{ marginBottom: 32 }}>
        <div
          style={{
            fontFamily: "var(--mono)",
            fontSize: 11,
            color: COL_FG3,
            textTransform: "uppercase",
            letterSpacing: "0.1em",
            marginBottom: 8,
          }}
        >
          Méthodologie
        </div>
        <h1
          style={{
            fontFamily: "var(--serif-display)",
            fontSize: 34,
            fontWeight: 600,
            color: "var(--fg1)",
            lineHeight: 1.2,
            margin: "0 0 12px 0",
          }}
        >
          Comment l&apos;observatoire fonctionne — sans boîte noire
        </h1>
        <p
          style={{
            fontFamily: "var(--sans-body)",
            fontSize: 15.5,
            color: "var(--fg2)",
            lineHeight: 1.7,
            maxWidth: 880,
            margin: 0,
          }}
        >
          Trois axes. Huit étapes. Sept sources. Quatre études comparatives chiffrées. Aucune
          valeur affichée dans le dashboard n&apos;est inventée — chacune est traçable jusqu&apos;à sa source.
        </p>
      </section>

      {/* Section 1 — Les 3 axes Web Mining */}
      <Section eyebrow="Cadre théorique" title="Les 3 axes du Web Mining">
        {/* Bandeau introductif : les 3 questions phares */}
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr auto 1fr auto 1fr",
            alignItems: "center",
            gap: 14,
            marginBottom: 22,
            padding: "16px 18px",
            borderRadius: 8,
            background: "color-mix(in oklch, var(--fg3) 5%, transparent)",
            border: "1px solid color-mix(in oklch, var(--fg3) 10%, transparent)",
          }}
        >
          {AXES.map((a, i) => (
            <Fragment key={a.key}>
              <div style={{ textAlign: "center" }}>
                <div
                  className="mono"
                  style={{
                    fontSize: 10.5,
                    color: a.color,
                    fontWeight: 700,
                    letterSpacing: "0.1em",
                    textTransform: "uppercase",
                    marginBottom: 4,
                  }}
                >
                  Axe {a.num}
                </div>
                <div
                  style={{
                    fontFamily: "var(--serif-display)",
                    fontSize: 16,
                    fontWeight: 600,
                    color: "var(--fg1)",
                    fontStyle: "italic",
                    lineHeight: 1.3,
                  }}
                >
                  « {a.question} »
                </div>
              </div>
              {i < AXES.length - 1 && (
                <div
                  style={{
                    fontSize: 22,
                    color: COL_FG3,
                    fontWeight: 300,
                    userSelect: "none",
                  }}
                >
                  →
                </div>
              )}
            </Fragment>
          ))}
        </div>

        {/* Les 3 cartes détaillées */}
        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, minmax(0, 1fr))", gap: 18 }}>
          {AXES.map((a) => (
            <a
              key={a.key}
              href={a.href}
              style={{
                textDecoration: "none",
                display: "block",
                padding: "20px 22px",
                borderRadius: 8,
                background: "color-mix(in oklch, var(--fg3) 4%, transparent)",
                border: `1px solid color-mix(in oklch, ${a.color} 30%, transparent)`,
                borderTop: `4px solid ${a.color}`,
                color: "inherit",
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 10 }}>
                <span
                  className="mono"
                  style={{ fontSize: 11, color: a.color, letterSpacing: "0.08em", textTransform: "uppercase" }}
                >
                  Axe {a.num}
                </span>
                <span className="mono" style={{ fontSize: 10.5, color: COL_FG3 }}>
                  → {a.pageLabel}
                </span>
              </div>
              <h3
                style={{
                  fontFamily: "var(--serif-display)",
                  fontSize: 22,
                  fontWeight: 600,
                  color: "var(--fg1)",
                  margin: "0 0 4px 0",
                }}
              >
                {a.title}
              </h3>
              <div
                style={{
                  fontSize: 13,
                  color: a.color,
                  fontStyle: "italic",
                  marginBottom: 4,
                  fontWeight: 600,
                }}
              >
                « {a.question} »
              </div>
              <div style={{ fontSize: 12, color: "var(--fg2)", marginBottom: 12 }}>{a.subtitle}</div>
              <p style={{ fontSize: 12.5, color: "var(--fg2)", lineHeight: 1.6, margin: "0 0 14px 0" }}>{a.desc}</p>
              <div
                style={{
                  fontFamily: "var(--mono)",
                  fontSize: 10.5,
                  color: COL_FG3,
                  textTransform: "uppercase",
                  letterSpacing: "0.08em",
                  marginBottom: 6,
                }}
              >
                Algorithmes comparés
              </div>
              <div style={{ display: "flex", flexWrap: "wrap", gap: 4 }}>
                {a.algos.map((algo) => (
                  <span
                    key={algo}
                    style={{
                      fontSize: 11,
                      padding: "2px 8px",
                      borderRadius: 10,
                      background: `color-mix(in oklch, ${a.color} 10%, transparent)`,
                      border: `1px solid color-mix(in oklch, ${a.color} 28%, transparent)`,
                      color: "var(--fg1)",
                    }}
                  >
                    {algo}
                  </span>
                ))}
              </div>
            </a>
          ))}
        </div>

        {/* Note de bas de section : pourquoi cet ordre */}
        <div
          style={{
            marginTop: 16,
            fontSize: 12,
            color: COL_FG3,
            fontStyle: "italic",
            lineHeight: 1.6,
            textAlign: "center",
          }}
        >
          L&apos;ordre <strong style={{ color: "var(--fg2)" }}>Content → Structure → Usage</strong> n&apos;est pas
          arbitraire : on doit d&apos;abord <strong style={{ color: COL_CONTENT }}>extraire</strong> les compétences
          d&apos;un texte avant de pouvoir les <strong style={{ color: COL_STRUCTURE }}>connecter</strong> en
          graphe, puis enfin <strong style={{ color: COL_USAGE }}>prédire</strong> leur évolution dans le temps.
          C&apos;est aussi l&apos;ordre de navigation choisi pour ce dashboard.
        </div>
      </Section>

      {/* Section 2 — Pipeline en 8 étapes */}
      <Section eyebrow="Architecture" title="Le pipeline complet · 8 étapes du scraping au dashboard">
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {PIPELINE_STEPS.map((s) => {
            const sideColor = s.side === "Bachirou" ? COL_STRUCTURE : COL_USAGE;
            return (
              <div
                key={s.n}
                style={{
                  display: "grid",
                  gridTemplateColumns: "44px minmax(0, 1fr) 90px",
                  gap: 14,
                  alignItems: "center",
                  padding: "12px 16px",
                  borderRadius: 6,
                  background: "color-mix(in oklch, var(--fg3) 4%, transparent)",
                  border: "1px solid color-mix(in oklch, var(--fg3) 10%, transparent)",
                }}
              >
                <div
                  className="mono tabular"
                  style={{ fontSize: 18, color: "var(--fg1)", fontWeight: 700, textAlign: "center" }}
                >
                  {String(s.n).padStart(2, "0")}
                </div>
                <div>
                  <div style={{ fontFamily: "var(--sans-body)", fontSize: 14, fontWeight: 600, color: "var(--fg1)" }}>{s.title}</div>
                  <div style={{ fontSize: 12, color: "var(--fg2)", marginTop: 3, lineHeight: 1.5 }}>{s.desc}</div>
                </div>
                <div
                  className="mono"
                  style={{
                    fontSize: 10.5,
                    color: sideColor,
                    fontWeight: 700,
                    textAlign: "right",
                    letterSpacing: "0.04em",
                    textTransform: "uppercase",
                  }}
                >
                  {s.side}
                </div>
              </div>
            );
          })}
        </div>
      </Section>

      {/* Section 3 — Sources collectées */}
      <Section
        eyebrow="Transparence des données"
        title={`${SOURCES.length} sources collectées · ${SOURCES.reduce((a, s) => a + s.n, 0).toLocaleString("fr-FR")} offres`}
      >
        <div className="card" style={{ padding: "16px 20px" }}>
          <table style={{ width: "100%", borderCollapse: "collapse", fontFamily: "var(--sans-body)", fontSize: 12.5 }}>
            <thead>
              <tr
                style={{
                  textAlign: "left",
                  borderBottom: "1px solid color-mix(in oklch, var(--fg3) 18%, transparent)",
                  color: COL_FG3,
                  fontSize: 11,
                  textTransform: "uppercase",
                  letterSpacing: "0.06em",
                }}
              >
                <th style={{ padding: "8px 10px 8px 0" }}>Source</th>
                <th style={{ padding: "8px 10px" }}>Origine</th>
                <th style={{ padding: "8px 10px", textAlign: "right" }}>Offres collectées</th>
                <th style={{ padding: "8px 10px" }}>Méthode de scraping</th>
                <th style={{ padding: "8px 10px" }}>Période couverte</th>
              </tr>
            </thead>
            <tbody>
              {SOURCES.map((s) => (
                <tr key={s.name} style={{ borderBottom: "1px solid color-mix(in oklch, var(--fg3) 8%, transparent)" }}>
                  <td style={{ padding: "10px 10px 10px 0", fontWeight: 500, color: "var(--fg1)" }}>{s.name}</td>
                  <td style={{ padding: "10px 10px" }}>
                    <span
                      style={{
                        padding: "2px 8px",
                        borderRadius: 10,
                        fontSize: 11,
                        background:
                          s.origine === "Maroc"
                            ? "color-mix(in oklch, " + COL_STRUCTURE + " 14%, transparent)"
                            : "color-mix(in oklch, " + COL_GOLD + " 14%, transparent)",
                        color: s.origine === "Maroc" ? COL_STRUCTURE : COL_GOLD,
                        fontWeight: 600,
                      }}
                    >
                      {s.origine === "Maroc" ? "MA" : "INTL"}
                    </span>
                  </td>
                  <td className="mono tabular" style={{ padding: "10px 10px", textAlign: "right", fontWeight: 600 }}>
                    {s.n.toLocaleString("fr-FR")}
                  </td>
                  <td style={{ padding: "10px 10px", color: "var(--fg2)" }}>{s.methode}</td>
                  <td className="mono" style={{ padding: "10px 10px", color: COL_FG3, fontSize: 11.5 }}>{s.periode}</td>
                </tr>
              ))}
              <tr style={{ background: "color-mix(in oklch, var(--fg3) 5%, transparent)", fontWeight: 700 }}>
                <td style={{ padding: "10px 10px 10px 0" }}>Total</td>
                <td style={{ padding: "10px 10px", color: COL_FG3, fontSize: 11 }}>6 MA + 1 INTL</td>
                <td className="mono tabular" style={{ padding: "10px 10px", textAlign: "right" }}>
                  {SOURCES.reduce((a, s) => a + s.n, 0).toLocaleString("fr-FR")}
                </td>
                <td colSpan={2} style={{ padding: "10px 10px", color: COL_FG3, fontStyle: "italic", fontSize: 11.5 }}>
                  cf. sources/registry.yaml pour le détail compliance robots.txt
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </Section>

      {/* Section 4 — 4 études comparatives */}
      <Section eyebrow="Études comparatives" title="Quatre benchmarks chiffrés · un modèle retenu par axe">
        <div style={{ display: "grid", gridTemplateColumns: "repeat(2, minmax(0, 1fr))", gap: 16 }}>
          {ETUDES.map((e) => (
            <div
              key={e.ref}
              style={{
                padding: "18px 20px",
                borderRadius: 8,
                background: "color-mix(in oklch, var(--fg3) 4%, transparent)",
                border: `1px solid color-mix(in oklch, ${e.color} 25%, transparent)`,
                borderLeft: `4px solid ${e.color}`,
              }}
            >
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 6 }}>
                <span className="mono" style={{ fontSize: 11, color: e.color, fontWeight: 700, letterSpacing: "0.08em" }}>
                  {e.ref}
                </span>
                {e.href ? (
                  <a href={e.href} className="mono" style={{ fontSize: 10.5, color: COL_FG3, textDecoration: "none" }}>
                    → voir la page
                  </a>
                ) : (
                  <span className="mono" style={{ fontSize: 10.5, color: COL_FG3, fontStyle: "italic" }}>
                    à venir
                  </span>
                )}
              </div>
              <h3 style={{ fontFamily: "var(--serif-display)", fontSize: 18, fontWeight: 600, color: "var(--fg1)", margin: "0 0 8px 0" }}>
                {e.titre}
              </h3>
              <div style={{ fontSize: 12.5, color: "var(--fg2)", marginBottom: 10 }}>{e.algos}</div>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 12 }}>
                <div>
                  <div className="mono" style={{ fontSize: 10, color: COL_FG3, textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    Métrique principale
                  </div>
                  <div className="mono tabular" style={{ fontSize: 16, color: "var(--fg1)", fontWeight: 700, marginTop: 2 }}>
                    {e.metric}
                  </div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div className="mono" style={{ fontSize: 10, color: COL_FG3, textTransform: "uppercase", letterSpacing: "0.08em" }}>
                    Retenu V1.0
                  </div>
                  <div style={{ fontSize: 14, color: e.color, fontWeight: 700, marginTop: 2 }}>{e.winner}</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </Section>

      {/* Section 5 — Limites & RGPD */}
      <Section eyebrow="Rigueur scientifique" title="Limites assumées · RGPD · éthique">
        <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1fr) minmax(0, 1fr)", gap: 18 }}>
          <div className="card" style={{ padding: "18px 22px", borderTop: `3px solid ${COL_GOLD}` }}>
            <div
              className="mono"
              style={{
                fontSize: 11,
                color: COL_GOLD,
                textTransform: "uppercase",
                letterSpacing: "0.08em",
                marginBottom: 10,
              }}
            >
              Limites assumées
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {LIMITES.map((l) => (
                <div key={l.titre}>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "var(--fg1)", marginBottom: 3 }}>{l.titre}</div>
                  <div style={{ fontSize: 12, color: "var(--fg2)", lineHeight: 1.55 }}>{l.desc}</div>
                </div>
              ))}
            </div>
          </div>
          <div className="card" style={{ padding: "18px 22px", borderTop: `3px solid ${COL_STRUCTURE}` }}>
            <div
              className="mono"
              style={{
                fontSize: 11,
                color: COL_STRUCTURE,
                textTransform: "uppercase",
                letterSpacing: "0.08em",
                marginBottom: 10,
              }}
            >
              RGPD & éthique
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
              {RGPD_POINTS.map((p) => (
                <div key={p.titre}>
                  <div style={{ fontSize: 13, fontWeight: 600, color: "var(--fg1)", marginBottom: 3 }}>{p.titre}</div>
                  <div style={{ fontSize: 12, color: "var(--fg2)", lineHeight: 1.55 }}>{p.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </Section>

      {/* Section 6 — Glossaire */}
      <Section eyebrow="Pour aller plus loin" title="Glossaire · 15 termes techniques expliqués simplement">
        <div className="card" style={{ padding: "16px 18px" }}>
          <div style={{ display: "flex", flexDirection: "column", gap: 0 }}>
            {GLOSSARY.map((g, i) => {
              const isOpen = openGloss.has(i);
              return (
                <button
                  key={g.term}
                  onClick={() => toggleGloss(i)}
                  style={{
                    textAlign: "left",
                    padding: "10px 4px",
                    background: "transparent",
                    border: "none",
                    borderBottom:
                      i < GLOSSARY.length - 1
                        ? "1px solid color-mix(in oklch, var(--fg3) 8%, transparent)"
                        : "none",
                    cursor: "pointer",
                    color: "inherit",
                    fontFamily: "var(--sans-body)",
                  }}
                >
                  <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", gap: 12 }}>
                    <span style={{ fontWeight: 600, color: "var(--fg1)", fontSize: 14, fontFamily: "var(--mono)" }}>{g.term}</span>
                    <span style={{ fontSize: 13, color: COL_FG3 }}>{isOpen ? "−" : "+"}</span>
                  </div>
                  {isOpen && (
                    <div style={{ fontSize: 12.5, color: "var(--fg2)", lineHeight: 1.6, marginTop: 6 }}>{g.def}</div>
                  )}
                </button>
              );
            })}
          </div>
        </div>
      </Section>

    </>
  );
}

function Section({ eyebrow, title, children }: { eyebrow: string; title: string; children: ReactNode }) {
  return (
    <section style={{ marginBottom: 40 }}>
      <div style={{ marginBottom: 18 }}>
        <div
          style={{
            fontFamily: "var(--mono)",
            fontSize: 11,
            color: COL_FG3,
            textTransform: "uppercase",
            letterSpacing: "0.08em",
            marginBottom: 4,
          }}
        >
          {eyebrow}
        </div>
        <h2
          style={{
            fontFamily: "var(--serif-display)",
            fontSize: 22,
            fontWeight: 600,
            color: "var(--fg1)",
            margin: 0,
            lineHeight: 1.25,
          }}
        >
          {title}
        </h2>
      </div>
      {children}
    </section>
  );
}
