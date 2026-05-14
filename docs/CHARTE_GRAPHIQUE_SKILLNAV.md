# Charte graphique.

## SKILLNAV — Skills Navigator

> Direction artistique : reproduction fidèle des codes McKinsey & Company, dark dominant. Adaptée à un observatoire académique des compétences IA & Data Science.

| | |
|---|---|
| **Projet** | SKILLNAV — Observatoire des Compétences IA & Data Science par Web Mining |
| **Cadre académique** | M242 — Analyse de Web · ENSA-Tétouan · Diplôme d'Ingénieur, filière Sciences des Données, Big Data et Intelligence Artificielle (SDBIA) |
| **Encadrement** | Prof. Imad Sassi |
| **Auteurs** | Karamo Sylla & Bachirou Konaté |
| **Direction artistique** | McKinsey & Company *(référence visuelle)* |
| **Soutenance** | 28 mai 2026 |

---

## Table des matières

| § | Section | Page |
|---|---|---|
| 01 | [Direction artistique](#01--direction-artistique) | — |
| 02 | [Palette de couleurs](#02--palette-de-couleurs) | — |
| 03 | [Typographie](#03--typographie) | — |
| 04 | [Iconographie](#04--iconographie) | — |
| 05 | [Espacements et grille](#05--espacements-et-grille) | — |
| 06 | [Composants UI](#06--composants-ui) | — |
| 06bis | [Composants visuels — Graphes Neo4j](#06bis--composants-visuels--graphes-neo4j) | — |
| 06ter | [Composants Time Series & Forecasting](#06ter--composants-time-series--forecasting) | — |
| 06quater | [Composant `<NERHighlight>`](#06quater--composant-nerhighlight) | — |
| 07 | [Variables CSS](#07--variables-css) | — |

---

## 01 — Direction artistique

> *« Cartographier les compétences IA, sans dramatiser. SKILLNAV mesure l'évolution du marché de l'expertise data avec la rigueur d'un institut de recherche et la sobriété d'une publication scientifique. »*

### Positionnement

SKILLNAV est un observatoire académique des compétences en Intelligence Artificielle et Data Science, construit dans le cadre du module M242 — Analyse de Web (ENSA-Tétouan, Diplôme d'Ingénieur, filière Sciences des Données, Big Data et Intelligence Artificielle — SDBIA). Le projet démontre une couverture rigoureuse des trois axes du Web Mining — Content, Structure, Usage — appliquée à un domaine en expansion rapide : l'expertise IA/DS sur le marché marocain et international.

L'identité visuelle reproduit fidèlement les codes de McKinsey & Company : navy profond, royal blue électrique, serif éditorial, grotesque institutionnelle, générosité des espaces blancs, zéro ornement décoratif. Cette parenté assume une ambition claire : porter l'autorité d'une publication scientifique auprès du jury, des étudiants, des chercheurs et des recruteurs IA.

### Principes directeurs

**01 — Autorité éditoriale**
Hiérarchie typographique forte, serif Display pour les titres, justification soignée. Chaque écran et chaque page imprimée doit pouvoir être lue comme une publication de référence.

**02 — Sobriété radicale**
Aucune ombre marquée, aucun gradient, aucune illustration décorative. Le contenu — chiffres, courbes, graphes, citations — porte le sens. Le design s'efface devant la donnée.

**03 — Densité assumée**
Côté dashboard analytique, la densité d'information est un parti pris : c'est un outil pour chercheur. Côté pages méthode et présentation de soutenance, le rythme s'aère pour respecter le lecteur académique.

**04 — Honnêteté méthodologique**
Disclaimers automatiques sur faibles échantillons, indication systématique de la date de dernière mise à jour, badges de confiance d'extraction visibles, intervalles de confiance affichés sur les forecasts. La transparence est un élément graphique à part entière — c'est l'exigence scientifique imposée par le sujet.

### Attributs de marque

`INSTITUTIONNEL` · `ÉDITORIAL` · `SOBRE` · `RIGOUREUX` · `SCIENTIFIQUE`

---

## 02 — Palette de couleurs

La palette SKILLNAV repose sur le couple navy + royal blue qui signe l'identité McKinsey, complétée par des neutres crème/anthracite et un set sémantique sobre. Le mode dark est dominant : il porte le dashboard analytique et la présentation de soutenance. Le mode light reste disponible pour les exports impression (rapport méthodologique).

**Répartition recommandée — 60 / 30 / 10**
60 % Navy `#051C2C` · 30 % Cream / White · 10 % Royal Blue `#2251FF` en accent strict.

### Primary — Navy McKinsey

| Token | Hex | Usage |
|---|---|---|
| Navy 1000 | `#051C2C` | Background dominant dark mode, fond rapport méthodologique, page de couverture deck |
| Navy 900 | `#0A2540` | Surface élevée mode dark — sidebar, header, panels secondaires |
| Navy 800 | `#133553` | Cards, modals, blocs de données sur fond Navy 1000 |
| Navy 700 | `#1F4868` | Bordures sur fond dark, séparateurs, hover states subtils |

### Accent — Royal Blue

| Token | Hex | Usage |
|---|---|---|
| Royal Blue | `#2251FF` | Accent principal : CTA, liens, valeurs hero KPI, focus state |
| Royal Blue 400 | `#4F73FF` | Hover button, badges actifs, highlight ligne dans tables |
| Royal Blue 700 | `#1A3FCC` | Pressed state, texte sur fond Royal Soft, charts comparatifs |
| Royal Soft | `#E5EBFF` | Backgrounds informatifs, chips, callouts méthodologiques |

### Fond et surfaces

| Token | Hex | Usage |
|---|---|---|
| White | `#FFFFFF` | Surface card mode light, fond rapports synthèse imprimés |
| Cream | `#FAF8F3` | Background light alternatif — pages méthode, rapport académique L5 |
| Bone | `#F5F1EB` | Texte sur fond Navy, fond accent papier dans deck PPTX soutenance |
| Border 100 | `#E5E7EB` | Bordures légères mode light, séparateurs cards |

### Texte et neutres

| Token | Hex | Usage |
|---|---|---|
| Ink — Anthracite | `#1A1A1A` | Texte principal mode light, titres rapports imprimés |
| Ink Soft | `#4A4A4A` | Sous-titres, paragraphes secondaires mode light |
| Muted | `#6B7280` | Légendes, captions, labels axes graphiques, footers |

### Couleurs sémantiques

| Token | Hex | Usage |
|---|---|---|
| Success | `#0F8F65` | Tendances positives, croissance compétence, score émergence confirmé |
| Warning | `#C77700` | Faible échantillon, données à confirmer, seuil émergence intermédiaire |
| Error | `#B42318` | Inadéquation grave, score émergence critique, erreurs système |
| Info | `#2251FF` | Tooltips méthodologiques, callouts, encadrés explicatifs |

### 10 familles de compétences IA / Data Science — codes couleur

Chaque famille de compétences SKILLNAV dispose d'un code couleur réservé. Ces couleurs servent dans les badges `<SkillBadge>`, les nœuds du graphe Neo4j, les segments de treemap, les barres de cartographie temporelle et les filtres. Elles sont calibrées pour rester lisibles sur Navy comme sur fond clair, sans recourir à l'arc-en-ciel.

| Famille | Hex | Exemples de compétences |
|---|---|---|
| ML Classique | `#2251FF` | Régression, classification, scikit-learn, XGBoost, feature engineering |
| Deep Learning | `#7C3AED` | PyTorch, TensorFlow, CNN, Transformers, fine-tuning, attention |
| NLP | `#0891B2` | BERT, CamemBERT, embeddings, NER, RAG, LLM, spaCy, HuggingFace |
| Computer Vision | `#C77700` | OpenCV, YOLO, segmentation, ViT, OCR, detection, image generation |
| Data Engineering | `#1F4868` | Spark, Airflow, dbt, Kafka, ETL/ELT, data pipelines, parquet |
| MLOps | `#0F8F65` | MLflow, Kubeflow, Docker, CI/CD ML, model monitoring, feature stores |
| Cloud & Big Data | `#1A3FCC` | AWS, GCP, Azure, BigQuery, Snowflake, Databricks, S3, Hadoop |
| AI Ethics & Responsible AI | `#4A1D6E` | Bias mitigation, explainability, SHAP, LIME, RGPD, AI Act, fairness |
| Statistiques & Analyse | `#5C7E2A` | Stats inférentielles, A/B testing, séries temporelles, économétrie, SQL |
| Outils & Soft skills | `#6B7280` | Python, Git, communication, vulgarisation, anglais, gestion de projet |

---

## 03 — Typographie

Le couple typographique reproduit l'autorité éditoriale McKinsey : un serif variable contemporain pour les titres et chiffres hero, une grotesque neutre pour le corps de texte, une mono pour les chiffres tabulaires et les blocs de code. Toutes les polices retenues sont open source — disponibles via Google Fonts ou GitHub — afin d'assurer une intégration zéro-friction sur web, PDF et PPTX.

### Polices retenues

| Rôle | Police | Équivalent McKinsey |
|---|---|---|
| **Display** | **Fraunces** | ≈ Bower (serif éditorial McKinsey) |
| **Body** | **Inter** | ≈ McKinsey Sans / Theinhardt |
| **Mono** | **JetBrains Mono** | Chiffres tabular figures, blocs de code |

### Hiérarchie typographique

| Niveau | Taille / poids | Police | Usage |
|---|---|---|---|
| Display | 64 / Light | Fraunces | Numéro hero d'un KPI, titre couverture rapport méthodologique |
| Heading 1 | 40 / Regular | Fraunces | Titre de section dans rapports et pages dashboard |
| Heading 2 | 28 / Regular | Fraunces | Sous-section, titre de card dashboard |
| Heading 3 | 20 / Semibold | Inter | Titre de bloc, label de groupe de filtres |
| Body | 14 / Regular · line 1.6 | Inter | Paragraphe, description tooltip, contenu de table |
| Body Small | 12 / Regular · line 1.5 | Inter | Captions, légendes, footers, disclaimers méthodologiques |
| Eyebrow | 11 / Bold · UPPER | Inter | Étiquette de section, kicker de card, label de chart |
| Mono | 13 / Regular · TF | JetBrains Mono | Chiffres tabular figures, codes hex, identifiants de modèles HF |

### Règles typographiques

- Tabular figures **ON par défaut** sur tous les chiffres affichant des séries — alignement vertical impeccable.
- Aucun titre tout-capitales hors eyebrows — les capitales sont réservées aux labels de moins de 30 caractères.
- Italique réservé aux citations méthodologiques et aux noms d'institutions étrangères ; jamais pour l'emphase.
- Veuves et orphelins évitées dans les rapports PDF — utiliser `keep-with-next` pour les titres et `keep-together` pour les tableaux.
- Hauteur de ligne : **1.6 sur le body** ; **1.2 sur les chiffres hero** pour densifier l'impact visuel.

---

## 04 — Iconographie

SKILLNAV utilise **Lucide Icons** comme bibliothèque exclusive : trait fin (1.5 px), grille 24 px, esthétique éditoriale parfaitement compatible avec la sobriété McKinsey. Pas de glyphes pleins, pas d'icônes colorées, pas d'emoji dans l'interface.

### Bibliothèque

| Paramètre | Valeur | Usage |
|---|---|---|
| Bibliothèque | `lucide-react` | Web (Next.js 15) — composants `<SkillBadge>`, `<KPICard>`, `<FiltersBar>` |
| Style | Outline | Aucune icône solid — cohérence avec le minimalisme éditorial |
| Stroke width | `1.5` | Largeur de trait fixe sur toute l'interface, jamais 2 ni 1 |
| Color tokens | `currentColor` | Héritage de la couleur du parent — cycle Navy / Royal selon le contexte |
| Format export | SVG inline | Pour rapport méthodologique généré via WeasyPrint et PPTX via python-pptx |

### Tailles standards

| Taille | Valeur | Usage |
|---|---|---|
| XS | 14 px | Inline avec body small — captions, labels de chart |
| S | 16 px | Inline avec body — boutons compacts, items de menu |
| M | 20 px | Boutons principaux, headers de card, action bar |
| L | 24 px | Sidebar, navigation principale, pages de détail |
| XL | 32 px | Empty states, illustrations éditoriales, KPI hero |

### Icônes clés SKILLNAV

| Concept | Icône Lucide | Contexte d'usage |
|---|---|---|
| Famille de compétences IA | `Cpu` / `Brain` | Filtres, badge `SkillBadge`, segmentation treemap |
| Compétence émergente | `Sparkles` | Header de page `/skills`, badge `EmergingScore`, alertes |
| Graphe de compétences (Neo4j) | `Network` / `GitGraph` | Header page `/graph`, légendes communautés Louvain |
| Communauté détectée (Louvain) | `Users` | Légende couleur halo, panneau filtres communauté |
| Nœud central (PageRank) | `Award` / `Crown` | Badge top 5 nœuds, mise en avant compétence-pivot |
| Forecasting / time series | `LineChart` | Header page `/forecasting`, KPIs de tendance |
| Entité NER détectée | `Highlighter` / `Tag` | Composant `<NERHighlight>`, page `/ner-explorer` |
| Source de données | `Database` | `<SourceStatus>`, page `/quality`, indicateur last refresh |
| Score de confiance | `ShieldCheck` | `<ConfidenceBadge>`, validation extraction Pydantic AI |
| Tendance positive | `TrendingUp` | `KPICard`, charts comparatifs annuels |
| Tendance négative | `TrendingDown` | `KPICard` pour inadéquation, alertes |
| Étude comparative | `GitCompare` | Page `/comparative-study`, comparaison 3 algorithmes |
| Rapport / livrable | `FileText` | Page `/methodology`, `ReportCard`, export rapport L5 |
| Export dataset | `Download` | Page `/datasets`, boutons d'export JSON/CSV/Parquet |
| Méthodologie | `BookOpen` | Page `/methodology` publique, tooltips méthodologiques |
| Filtre | `SlidersHorizontal` | `<FiltersBar>` dashboard et pages d'exploration |
| Recherche | `Search` | Champ de recherche global (Elasticsearch), exploration insights |

---

## 05 — Espacements et grille

SKILLNAV utilise un système d'espacement **base 4 px** — chaque token est un multiple de 4. Cette règle s'applique aussi bien au padding interne des composants qu'aux gouttières de la grille. Elle garantit un rythme vertical cohérent entre dashboard Next.js, rapport méthodologique PDF généré via WeasyPrint et deck de soutenance PPTX.

### Tokens de spacing

| Token | Valeur | Usage |
|---|---|---|
| `space-1` | 4 px | Espace inline minimal — entre icône et label, gap dans badge |
| `space-2` | 8 px | Padding interne badge, gap entre boutons d'un même groupe |
| `space-3` | 12 px | Padding ligne de table, gap dans liste de filtres |
| `space-4` | 16 px | Padding standard input et button, marge entre paragraphes |
| `space-5` | 24 px | Padding interne card, gap entre cards d'une même rangée |
| `space-6` | 32 px | Marge entre sections d'une page, padding panneau latéral |
| `space-7` | 48 px | Espace au-dessus d'un titre H2, gap entre rangées de cards |
| `space-8` | 64 px | Marge entre blocs majeurs d'une page, header de section |
| `space-9` | 96 px | Espace au-dessus d'un titre H1 dans rapports, séparation chapitres |
| `space-10` | 128 px | Réserves éditoriales — page de couverture, transitions de chapitre |

### Layout principal — Dashboard Next.js 15

| Élément | Valeur | Note |
|---|---|---|
| Sidebar width | 264 px | Navigation fixe — collapsable à 72 px sur tablet |
| Header height | 64 px | `FiltersBar` globale, breadcrumbs, sélecteur de période |
| Content max-width | 1440 px | Centré dans le viewport — gouttières latérales auto |
| Gutters interne | 32 px | Entre les colonnes du content area |
| Card padding | 24 px | Padding interne card standard |
| Card border-radius | 6 px | Éditorial — pas de cards trop arrondies |
| Modal max-width | 720 px | Modals de configuration, formulaires QC |

### Breakpoints

| Nom | Valeur | Usage cible |
|---|---|---|
| `sm` | 640 px | Mobile — consultation rapide page méthodologie |
| `md` | 768 px | Tablet — sidebar collapsable, cards en colonne |
| `lg` | 1024 px | Laptop — dashboard analyste, sidebar fixe |
| `xl` | 1280 px | Desktop standard — layout 12 colonnes, charts complets |
| `2xl` | 1536 px | Large desktop — exploration graphe Neo4j, treemap pleine largeur |

---

## 06 — Composants UI

Les composants SKILLNAV sont construits sur **Shadcn UI** customisé avec les tokens de la charte. Cette section documente les variantes principales — boutons, cards, inputs, badges — et détaille les composants SKILLNAV-spécifiques cités dans le PRD : `KPICard`, `SkillBadge`, `EmergingScore`, `ConfidenceBadge`, `SourceStatus`.

### Boutons

| Variante | Tokens | Usage |
|---|---|---|
| Primary | `bg #2251FF` / `text #FFFFFF` / radius 6 / h 40 | Action principale — Générer rapport, Exporter dataset |
| Secondary | `bg transparent` / border Navy 700 / text Navy | Actions secondaires — Annuler, Filtrer |
| Ghost | `bg transparent` / text Navy / hover bg Royal Soft | Boutons tertiaires, items de menu |
| Destructive | `bg #B42318` / `text #FFFFFF` | Suppression d'une source, reset taxonomy |
| CTA dark | `bg #FFFFFF` / `text #051C2C` / radius 6 | Sur fond Navy — bouton hero page méthodologie |

### Cards

| Propriété | Valeur | Note |
|---|---|---|
| Background light | `#FFFFFF` | Mode light dashboard |
| Background dark | `#0A2540` (Navy 900) | Mode dark dashboard — surface élevée |
| Border | 1 px `#E5E7EB` / Navy 700 | Sans ombre — cohérent avec sobriété éditoriale |
| Border radius | 6 px | Éditorial — éviter les cards trop arrondies |
| Padding | 24 px (`space-5`) | Padding interne standard |
| Hover state | border Royal Blue | Pas d'élévation — juste accentuation de la bordure |

### Inputs et formulaires

| Propriété | Valeur | Note |
|---|---|---|
| Height | 40 px | Aligné sur boutons primary |
| Background | `#FFFFFF` / Navy 900 | Light / dark mode |
| Border | 1 px Border 100 | Repos |
| Border focus | 2 px Royal Blue + ring | État focus accessibilité — outline visible |
| Border radius | 6 px | Cohérent avec cards et boutons |
| Placeholder | Muted `#6B7280` | Italique non — cohérent avec body text |

### Composants SKILLNAV spécifiques

| Composant | Variantes / Tokens | Rôle |
|---|---|---|
| `<KPICard>` | Display 64 / Royal Blue / icône TrendingUp 32 | KPI hero d'une page — chiffre + delta + sparkline |
| `<SkillBadge>` | h 24 / radius pill / couleur famille compétences | Badge skill avec couleur de famille IA/DS (10 variantes) |
| `<EmergingScore>` | Bar visuelle 100 % / seuils 0.7 et 0.85 | Score émergence avec barre — vert / ambre / rouge |
| `<ConfidenceBadge>` | Score 0-1 / Royal Soft, Warning, Error | Confiance d'extraction Pydantic AI ou Transformers NER |
| `<SourceStatus>` | Dot 8 px / Success / Warning / Error | Statut source — last scraped, count, ok/erreur |
| `<FiltersBar>` | Header 64 / Navy 900 / icônes Lucide M | Barre globale de filtres — géographie, période, famille IA |
| `<DataTable>` | TanStack Table / tabular figures / mono hex | Tables QC, taxonomy review, export datasets |
| `<PlotlyChart>` | Wrapper / palette familles IA + Royal Blue accent | Bar, treemap, heatmap — visualisations principales |
| `<ReportCard>` | Card / preview thumbnail / Download icon | Card de rapport généré — preview + bouton télécharger |
| `<ComparativeTable>` | TanStack / 3 colonnes algos / cellules métriques mono | Tableau étude comparative — protocole, métriques chiffrées, choix |

### Exemple — Card compétence IA (mode dark)

```
┌──────────────────────────────────────────────────────────────────┐
│ DEEP LEARNING  ·  MAROC  ·  MAI 2026                             │
│                                                                  │
│ Transformers (BERT, GPT, LLaMA)                                  │
│ 187 offres analysées sur la période                              │
│                                                                  │
│ Score émergence — fine-tuning LLM                   0.87         │
│ Croissance demande sur 3 mois                       +24 %        │
│ Couverture cursus ingénieur IA Maroc                2 / 15       │
└──────────────────────────────────────────────────────────────────┘
   bg #051C2C  ·  text #F5F1EB  ·  accent #4F73FF
```

---

## 06bis — Composants visuels — Graphes Neo4j

L'axe **Web Structure Mining** est porté visuellement par la page `/graph` du dashboard. Cette section fixe les conventions pour rendre le graphe de compétences (nœuds = compétences, arêtes = co-occurrences dans les offres) lisible, navigable et conforme à la sobriété éditoriale McKinsey.

### Librairie de rendu

| Option | Cas d'usage | Verdict |
|---|---|---|
| `react-force-graph-2d` | Rendu Canvas, performant ≥ 1 000 nœuds, layout force-directed natif | **Recommandé** — démo soutenance fluide |
| `cytoscape.js` | Algorithmes avancés (Cose-Bilkent, Klay), interactions riches | Alternative si layouts hiérarchiques requis |
| `vis-network` | Simple, large communauté | Évité — esthétique non alignée |
| `d3-force` natif | Maximum de contrôle | Surcoût de dev hors deadline 18 jours |

### Conventions visuelles

| Élément | Token / paramètre | Note |
|---|---|---|
| **Nœud Skill** | Cercle plein, couleur famille IA, diamètre `4 + 12 × PageRank_normalisé` (px) | Taille porte l'importance, couleur porte la famille |
| **Label de nœud** | Inter 12 / Bone sur Navy / max 14 caractères, ellipsis ensuite | Visible uniquement zoom ≥ 1.2 ou top-20 PageRank |
| **Arête co-occurrence** | Trait Navy 700 (mode dark) / Border 100 (mode light), épaisseur `0.5 + 2 × poids_normalisé` (px) | Opacité 0.4–0.8 selon poids |
| **Communauté Louvain** | Halo coloré semi-transparent autour des nœuds — couleur tirée d'une palette dérivée des familles IA + variantes neutres | Maximum 8 communautés colorées simultanément, le reste en gris Muted |
| **Badge PageRank top 5** | Icône `Award` Royal Blue + score affiché en Mono 11 sous le label | Mise en avant immédiate des compétences-pivot |
| **Tooltip hover** | Card Navy 800, padding 12, infos : nom compétence, famille, degré, PageRank, communauté, top 3 co-occurrences | Apparition 200 ms |
| **Légende latérale** | Panel droit 240 px, liste des communautés détectées + couleur + nombre de nœuds | Cliquable pour filtrer |
| **Zoom & pan** | Contrôle scroll/pinch, minimap bas-droite 160 × 100 px | Reset button Lucide `LocateFixed` |
| **Mode dark / light** | Toggle global ; en light → arêtes Border 100, halos opacité 0.15, labels Ink | Dark conservé par défaut pour soutenance |

### Cas d'usage à illustrer dans le PRD §6 et la soutenance

- Densité du graphe complet (vue d'ensemble, sans labels — démontre l'échelle)
- Vue filtrée famille « NLP » uniquement (~ 30–60 nœuds, labels visibles)
- Communautés Louvain colorées avec légende — démontre l'axe Structure Mining
- Top 10 PageRank en table latérale + nœuds correspondants surlignés

---

## 06ter — Composants Time Series & Forecasting

L'axe **Web Usage Mining** est porté visuellement par la page `/forecasting`. Cette section fixe les conventions pour les graphiques de séries temporelles et les prédictions d'évolution des compétences IA.

### `<TimeSeriesChart>`

| Élément | Token / paramètre |
|---|---|
| **Ligne historique** | Royal Blue `#2251FF`, épaisseur 2 px, solide |
| **Ligne forecast** | Royal Blue 700 `#1A3FCC`, épaisseur 2 px, **dashed** (`8 4`) |
| **Bande confiance 95 %** | Royal Soft `#E5EBFF` alpha 0.25, sans bordure |
| **Axes** | Tick Inter 11 Muted, format Mono pour les valeurs, format `MMM YYYY` pour le temps |
| **Grille** | Border 100 (light) / Navy 700 (dark), 1 px, opacité 0.4, lignes horizontales uniquement |
| **Marker pivot** | Vertical dashed Muted au point `now()` — séparation historique / forecast |
| **Annotations** | Pin Lucide `MapPin` Royal Blue sur événements marquants (ex. sortie modèle, conférence) |

### `<ForecastComparisonChart>`

Présente côte à côte les 3 algorithmes comparés (ARIMA / Prophet / LSTM) sur une même série temporelle réelle.

| Élément | Token / paramètre |
|---|---|
| **Ligne réalité** | Navy `#051C2C` (light : Ink), solide, 2 px |
| **Ligne ARIMA** | Royal Blue `#2251FF`, dashed `8 4`, 1.5 px |
| **Ligne Prophet** | Royal Blue 400 `#4F73FF`, dashed `4 4`, 1.5 px |
| **Ligne LSTM** | Royal Blue 700 `#1A3FCC`, dotted, 1.5 px |
| **Légende** | Inline bottom-right : nom algo + MAPE en Mono 12 (ex. `LSTM · MAPE 11.8 %`) |
| **Encadré métriques** | Card latérale, table 3 lignes × MAPE / RMSE / MAE / runtime |

### `<TreemapEmerging>`

Treemap des compétences émergentes — taille = score émergence, couleur = famille IA.

| Élément | Token / paramètre |
|---|---|
| **Pavé** | Border 1 px Navy 700, padding interne 8, label Inter 12 |
| **Label** | Affichage : nom compétence (Inter 12 Bone) + score (Mono 11) ; ellipsis si pavé < 80 px |
| **Hover** | Bordure Royal Blue 2 px, tooltip avec famille, score, croissance |
| **Couleur fond** | Token `--skn-fam-*` correspondant à la famille |

### `<KPIDelta>`

Petite card de KPI pour pages d'overview.

| Élément | Token / paramètre |
|---|---|
| **Valeur principale** | Fraunces Display 40, Bone (dark) / Ink (light) |
| **Delta %** | Mono 14, couleur sémantique (Success / Warning / Error) avec flèche `TrendingUp` ou `TrendingDown` |
| **Sparkline** | Royal Blue, h 32 px, sans axes, 12 derniers mois |
| **Label** | Eyebrow 11 Bold UPPER Muted |

---

## 06quater — Composant `<NERHighlight>`

L'axe **Web Content Mining** est porté visuellement par la page `/ner-explorer`. Le composant `<NERHighlight>` affiche un texte d'offre d'emploi avec les entités annotées par les modèles NER (BERT, CamemBERT, DistilBERT) — c'est la démonstration visuelle clé du Content Mining.

### Mise en page

| Élément | Token / paramètre |
|---|---|
| **Conteneur** | Card Navy 800 (dark) / White (light), padding 24, border 1 px Navy 700 / Border 100, radius 6 |
| **Texte de base** | Inter 14 / line-height 1.7, Bone (dark) / Ink (light) |
| **Largeur** | Max-width 720 px — confort de lecture maximal |
| **Mode** | Toggle dark / light en haut-droit |

### Spans annotés

Chaque entité détectée est wrapée dans un span stylé :

| Token | Valeur |
|---|---|
| `background` | Couleur de l'entité × alpha **0.2** |
| `border` | 1 px solid couleur de l'entité × alpha **0.4** |
| `border-radius` | 4 px (pill — `9999px` si une seule ligne) |
| `padding` | 2 px 6 px |
| `margin` | 0 1 px (évite collage entre tokens annotés) |
| **Label type entité** | Mono 10 Bold UPPER, en superscript à droite du span (`SKILL`, `TOOL`, etc.), opacité 0.7 |

### Couleurs par type d'entité

| Type entité | Couleur | Justification |
|---|---|---|
| `SKILL` | Royal Blue `#2251FF` | Entité principale du projet — accent dominant |
| `TOOL` | Royal Blue 400 `#4F73FF` | Variante de skill — distinct mais cousin |
| `FRAMEWORK` | Violet `#7C3AED` | PyTorch, TensorFlow, etc. — cohérent avec famille Deep Learning |
| `MODEL` | Cyan `#0891B2` | BERT, GPT, etc. — cohérent avec famille NLP |
| `LANGUAGE` | Success `#0F8F65` | Python, R, SQL — stabilité, fondations |
| `ROLE` | Navy 800 `#133553` | Titre de poste — contextuel, pas l'objet du focus |
| `ORGANIZATION` | Muted `#6B7280` | Entreprise mentionnée — secondaire |

### Interactions

| Action | Résultat |
|---|---|
| Hover span | Tooltip Card : type entité, confidence Pydantic AI (Mono 12), texte normalisé, famille assignée |
| Click span | Drawer latéral droit avec : occurrences dans la base, famille SKILLNAV, top 5 co-occurrences (graphe local) |
| Toggle légende | Affiche / masque la barre de légende inline (8 chips compétences avec couleurs) |
| Comparaison 3 modèles | Mode side-by-side : 3 colonnes (BERT / CamemBERT / DistilBERT) — mêmes textes annotés différemment — visualisation directe du delta |

### Exemple — Snippet annoté (mode dark)

```
Nous recherchons un Data Scientist [ROLE] confirmé maîtrisant
Python [LANGUAGE] et PyTorch [FRAMEWORK]. Vous travaillerez sur des
modèles BERT [MODEL] fine-tunés pour la classification de texte
[SKILL] et la détection d'entités nommées [SKILL] sur des données
multilingues.
```

---

## 07 — Variables CSS

Bloc `:root` prêt à copier-coller dans un projet **Next.js 15 avec Tailwind v4**. Les tokens couvrent palette, typographie, spacing, layout et basculent automatiquement entre mode dark (par défaut) et mode light via l'attribut `data-theme`.

```css
/* ============================================ */
/* SKILLNAV Design Tokens — McKinsey-inspired   */
/* Mode dark dominant. Compatible Tailwind v4.  */
/* ============================================ */

:root {
  /* Primary — Navy McKinsey */
  --skn-navy:        #051C2C;
  --skn-navy-900:    #0A2540;
  --skn-navy-800:    #133553;
  --skn-navy-700:    #1F4868;

  /* Accent — Royal Blue */
  --skn-royal:       #2251FF;
  --skn-royal-light: #4F73FF;
  --skn-royal-dark:  #1A3FCC;
  --skn-royal-soft:  #E5EBFF;

  /* Surfaces light */
  --skn-white:       #FFFFFF;
  --skn-cream:       #FAF8F3;
  --skn-bone:        #F5F1EB;
  --skn-border:      #E5E7EB;

  /* Text */
  --skn-ink:         #1A1A1A;
  --skn-ink-soft:    #4A4A4A;
  --skn-muted:       #6B7280;

  /* Semantic */
  --skn-success:     #0F8F65;
  --skn-warning:     #C77700;
  --skn-error:       #B42318;
  --skn-info:        #2251FF;

  /* Familles compétences IA / DS — SKILLNAV */
  --skn-fam-ml-classique:   #2251FF;
  --skn-fam-deep-learning:  #7C3AED;
  --skn-fam-nlp:            #0891B2;
  --skn-fam-cv:             #C77700;
  --skn-fam-data-eng:       #1F4868;
  --skn-fam-mlops:          #0F8F65;
  --skn-fam-cloud-bigdata:  #1A3FCC;
  --skn-fam-ai-ethics:      #4A1D6E;
  --skn-fam-stats:          #5C7E2A;
  --skn-fam-tools:          #6B7280;

  /* NER entity colors */
  --skn-ner-skill:        #2251FF;
  --skn-ner-tool:         #4F73FF;
  --skn-ner-framework:    #7C3AED;
  --skn-ner-model:        #0891B2;
  --skn-ner-language:     #0F8F65;
  --skn-ner-role:         #133553;
  --skn-ner-organization: #6B7280;

  /* Typographie */
  --font-display: "Fraunces", "Times New Roman", serif;
  --font-body:    "Inter", -apple-system, "Segoe UI", sans-serif;
  --font-mono:    "JetBrains Mono", "Consolas", monospace;

  /* Spacing — base 4 px */
  --space-1:  0.25rem;  /* 4 px  */
  --space-2:  0.5rem;   /* 8 px  */
  --space-3:  0.75rem;  /* 12 px */
  --space-4:  1rem;     /* 16 px */
  --space-5:  1.5rem;   /* 24 px */
  --space-6:  2rem;     /* 32 px */
  --space-7:  3rem;     /* 48 px */
  --space-8:  4rem;     /* 64 px */
  --space-9:  6rem;     /* 96 px */
  --space-10: 8rem;     /* 128 px */

  /* Radius */
  --radius-sm:   4px;
  --radius:      6px;
  --radius-pill: 9999px;

  /* Layout */
  --sidebar-width:    264px;
  --header-height:    64px;
  --content-max:      1440px;

  /* Graph (Neo4j) */
  --graph-node-min:   4px;
  --graph-node-max:   16px;
  --graph-edge-min:   0.5px;
  --graph-edge-max:   2.5px;
  --graph-halo-alpha: 0.18;

  /* Forecast */
  --forecast-ci-alpha: 0.25;
  --forecast-dash:     8 4;

  /* Mode dark — defaults */
  --bg:              var(--skn-navy);
  --surface:         var(--skn-navy-900);
  --surface-2:       var(--skn-navy-800);
  --text:            var(--skn-bone);
  --text-muted:      #8FA3B8;
  --border-color:    var(--skn-navy-700);
  --accent:          var(--skn-royal);
}

[data-theme="light"] {
  --bg:              var(--skn-white);
  --surface:         var(--skn-cream);
  --surface-2:       var(--skn-white);
  --text:            var(--skn-ink);
  --text-muted:      var(--skn-muted);
  --border-color:    var(--skn-border);
  --accent:          var(--skn-royal);
}
```

---

**Référence design officielle — SKILLNAV**
Projet académique M242 — ENSA-Tétouan · Karamo Sylla & Bachirou Konaté · Mai 2026
