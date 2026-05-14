# Charte graphique.

## Observatoire des Compétences et Métiers d'Afrique de l'Ouest

> Direction artistique : reproduction fidèle des codes McKinsey & Company, dark dominant.

| | |
|---|---|
| **Produit** | SYLI Technology |
| **Client** | MESRS — République de Guinée |
| **Auteur** | Karamo Sylla |
| **Direction artistique** | McKinsey & Company *(référence visuelle)* |

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
| 07 | [Variables CSS](#07--variables-css) | — |

---

## 01 — Direction artistique

> *« Cartographier, sans dramatiser. OCTAO mesure la vérité du marché du travail ouest-africain avec la rigueur d'un institut de statistique et la sobriété d'une publication de cabinet de conseil. »*

### Positionnement

OCTAO est le premier produit B2G de SYLI Technology. Il s'adresse en V1 à la Ministre de l'Enseignement Supérieur et de la Recherche Scientifique de la République de Guinée, pour piloter les mégaprojets MPS-30 et MPS-32 du Programme Simandou 2040.

L'identité visuelle reproduit fidèlement les codes de McKinsey & Company : navy profond, royal blue électrique, serif éditorial, grotesque institutionnelle, générosité des espaces blancs, zéro ornement décoratif. Cette parenté assume une ambition claire : porter une autorité immédiate auprès des décideurs politiques et académiques.

### Principes directeurs

**01 — Autorité éditoriale**
Hiérarchie typographique forte, serif Display pour les titres, justification soignée. Chaque écran et chaque page imprimée doit pouvoir être lue comme une publication de référence.

**02 — Sobriété radicale**
Aucune ombre marquée, aucun gradient, aucune illustration décorative. Le contenu — chiffres, courbes, citations — porte le sens. Le design s'efface devant la donnée.

**03 — Densité assumée**
Côté dashboard interne, la densité d'information est un parti pris : c'est un outil pour analyste. Côté livrables et portail universités, le rythme s'aère pour respecter le lecteur institutionnel.

**04 — Honnêteté méthodologique**
Disclaimers automatiques sur faibles échantillons, indication systématique de la date de dernière mise à jour, badges de confiance d'extraction visibles. La transparence est un élément graphique à part entière.

### Attributs de marque

`INSTITUTIONNEL` · `ÉDITORIAL` · `SOBRE` · `RIGOUREUX` · `SOUVERAIN`

---

## 02 — Palette de couleurs

La palette OCTAO repose sur le couple navy + royal blue qui signe l'identité McKinsey, complétée par des neutres crème/anthracite et un set sémantique sobre. Le mode dark est dominant : il porte le dashboard interne et les livrables institutionnels. Le mode light reste disponible pour les exports impression.

**Répartition recommandée — 60 / 30 / 10**
60 % Navy `#051C2C` · 30 % Cream / White · 10 % Royal Blue `#2251FF` en accent strict.

### Primary — Navy McKinsey

| Token | Hex | Usage |
|---|---|---|
| Navy 1000 | `#051C2C` | Background dominant dark mode, fond livrables, page de couverture deck |
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
| Cream | `#FAF8F3` | Background light alternatif — pages méthode publiques portail universités |
| Bone | `#F5F1EB` | Texte sur fond Navy, fond accent papier dans deck PPTX |
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
| Success | `#0F8F65` | Tendances positives, croissance métier, score ghost confirmé |
| Warning | `#C77700` | Faible échantillon, données à confirmer, seuil ghost intermédiaire |
| Error | `#B42318` | Inadéquation grave, score ghost critique, erreurs système |
| Info | `#2251FF` | Tooltips méthodologiques, callouts, encadrés explicatifs |

### 13 familles de métiers — codes couleur

Chaque famille métier OCTAO dispose d'un code couleur réservé. Ces couleurs servent dans les badges `<SkillBadge>`, les segments de treemap, les barres de cartographie et les filtres. Elles sont calibrées pour rester lisibles sur Navy comme sur fond clair, sans recourir à l'arc-en-ciel.

| Famille | Hex | Exemples de métiers |
|---|---|---|
| Santé | `#B42318` | Médecin, infirmier, pharmacien, sage-femme, biologiste |
| Droit & Conformité | `#4A1D6E` | Juriste, avocat, conseiller juridique, compliance officer |
| Gestion & Management | `#2251FF` | Chef de projet, manager, DAF, directeur opérationnel |
| Finance & Comptabilité | `#0F8F65` | Comptable, contrôleur, auditeur, analyste financier |
| Marketing & Commerce | `#C77700` | Commercial, marketeur, business developer, account manager |
| Ingénierie & Technique | `#1F4868` | Ingénieur civil, électrique, mécanique, BTP, mines |
| IT & Numérique | `#7C3AED` | Développeur, data analyst, devops, sysadmin, IA |
| RH & Formation | `#0891B2` | RRH, recruteur, formateur, gestionnaire de paie |
| Agriculture & Agroalimentaire | `#5C7E2A` | Agronome, technicien agricole, ingénieur agro |
| Éducation & Recherche | `#1A3FCC` | Enseignant, chercheur, formateur, ingénieur pédagogique |
| Social & Humanitaire | `#BE185D` | Travailleur social, coordinateur projet ONG |
| Logistique & Supply Chain | `#78716C` | Logisticien, supply chain manager, acheteur |
| Support & Service | `#525252` | Assistant, secrétaire, customer service |

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
| Display | 64 / Light | Fraunces | Numéro hero d'un KPI, titre couverture livrable |
| Heading 1 | 40 / Regular | Fraunces | Titre de section dans rapports et pages portail |
| Heading 2 | 28 / Regular | Fraunces | Sous-section, titre de card dashboard |
| Heading 3 | 20 / Semibold | Inter | Titre de bloc, label de groupe de filtres |
| Body | 14 / Regular · line 1.6 | Inter | Paragraphe, description tooltip, contenu de table |
| Body Small | 12 / Regular · line 1.5 | Inter | Captions, légendes, footers, disclaimers méthodologiques |
| Eyebrow | 11 / Bold · UPPER | Inter | Étiquette de section, kicker de card, label de chart |
| Mono | 13 / Regular · TF | JetBrains Mono | Chiffres tabular figures, codes pays, hex de couleurs |

### Règles typographiques

- Tabular figures **ON par défaut** sur tous les chiffres affichant des séries — alignement vertical impeccable.
- Aucun titre tout-capitales hors eyebrows — les capitales sont réservées aux labels de moins de 30 caractères.
- Italique réservé aux citations méthodologiques et aux noms d'institutions étrangères ; jamais pour l'emphase.
- Veuves et orphelins évitées dans les rapports PDF — utiliser `keep-with-next` pour les titres et `keep-together` pour les tableaux.
- Hauteur de ligne : **1.6 sur le body** ; **1.2 sur les chiffres hero** pour densifier l'impact visuel.

---

## 04 — Iconographie

OCTAO utilise **Lucide Icons** comme bibliothèque exclusive : trait fin (1.5 px), grille 24 px, esthétique éditoriale parfaitement compatible avec la sobriété McKinsey. Pas de glyphes pleins, pas d'icônes colorées, pas d'emoji dans l'interface.

### Bibliothèque

| Paramètre | Valeur | Usage |
|---|---|---|
| Bibliothèque | `lucide-react` | Web (Next.js V2+) — composants `<SkillBadge>`, `<KPICard>`, `<FiltersBar>` |
| Style | Outline | Aucune icône solid — cohérence avec le minimalisme éditorial |
| Stroke width | `1.5` | Largeur de trait fixe sur toute l'interface, jamais 2 ni 1 |
| Color tokens | `currentColor` | Héritage de la couleur du parent — cycle Navy / Royal selon le contexte |
| Format export | SVG inline | Pour livrables PDF générés via WeasyPrint et PPTX via python-pptx |

### Tailles standards

| Taille | Valeur | Usage |
|---|---|---|
| XS | 14 px | Inline avec body small — captions, labels de chart |
| S | 16 px | Inline avec body — boutons compacts, items de menu |
| M | 20 px | Boutons principaux, headers de card, action bar |
| L | 24 px | Sidebar, navigation principale, pages de détail |
| XL | 32 px | Empty states, illustrations éditoriales, KPI hero |

### Icônes clés OCTAO

| Concept | Icône Lucide | Contexte d'usage |
|---|---|---|
| Compétence ghost | `Ghost` | Header de page `/ghost-skills`, badge `GhostScore`, alertes |
| Famille métier | `Briefcase` | Filtres, badge `SkillBadge`, segmentation treemap |
| Source de données | `Database` | `<SourceStatus>`, page `/quality`, indicateur last refresh |
| Score de confiance | `ShieldCheck` | `<ConfidenceBadge>`, validation extraction Pydantic AI |
| Tendance positive | `TrendingUp` | `KPICard`, charts comparatifs annuels |
| Tendance négative | `TrendingDown` | `KPICard` pour inadéquation, alertes |
| Université / institution | `GraduationCap` | Portail universités, page institution, taxonomy review |
| Rapport / livrable | `FileText` | Page `/reports`, `ReportCard`, exports |
| Export dataset | `Download` | Page `/datasets`, boutons d'export JSON/CSV |
| Méthodologie | `BookOpen` | Page `/methode` publique, tooltips méthodologiques |
| Filtre | `SlidersHorizontal` | `<FiltersBar>` dashboard et portail |
| Recherche | `Search` | Champ de recherche global, exploration insights |

---

## 05 — Espacements et grille

OCTAO utilise un système d'espacement **base 4 px** — chaque token est un multiple de 4. Cette règle s'applique aussi bien au padding interne des composants qu'aux gouttières de la grille. Elle garantit un rythme vertical cohérent entre dashboard Next.js, livrables PDF générés via WeasyPrint et templates PPTX.

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

### Layout principal — Dashboard Next.js V2+

| Élément | Valeur | Note |
|---|---|---|
| Sidebar width | 264 px | Navigation fixe — collapsable à 72 px sur tablet |
| Header height | 64 px | `FiltersBar` globale, breadcrumbs, profil utilisateur |
| Content max-width | 1440 px | Centré dans le viewport — gouttières latérales auto |
| Gutters interne | 32 px | Entre les colonnes du content area |
| Card padding | 24 px | Padding interne card standard |
| Card border-radius | 6 px | Éditorial — pas de cards trop arrondies |
| Modal max-width | 720 px | Modals de configuration, formulaires QC |

### Breakpoints

| Nom | Valeur | Usage cible |
|---|---|---|
| `sm` | 640 px | Mobile — portail universités en lecture seule |
| `md` | 768 px | Tablet — sidebar collapsable, cards en colonne |
| `lg` | 1024 px | Laptop — dashboard analyste, sidebar fixe |
| `xl` | 1280 px | Desktop standard — layout 12 colonnes, charts complets |
| `2xl` | 1536 px | Large desktop — exploration insights, treemap pleine largeur |

---

## 06 — Composants UI

Les composants OCTAO sont construits sur **Shadcn UI** customisé avec les tokens de la charte. Cette section documente les variantes principales — boutons, cards, inputs, badges — et détaille les composants OCTAO-spécifiques cités dans le PRD : `KPICard`, `SkillBadge`, `GhostScore`, `ConfidenceBadge`, `SourceStatus`.

### Boutons

| Variante | Tokens | Usage |
|---|---|---|
| Primary | `bg #2251FF` / `text #FFFFFF` / radius 6 / h 40 | Action principale — Générer rapport, Exporter dataset |
| Secondary | `bg transparent` / border Navy 700 / text Navy | Actions secondaires — Annuler, Filtrer |
| Ghost | `bg transparent` / text Navy / hover bg Royal Soft | Boutons tertiaires, items de menu |
| Destructive | `bg #B42318` / `text #FFFFFF` | Suppression d'une source, reset taxonomy |
| CTA dark | `bg #FFFFFF` / `text #051C2C` / radius 6 | Sur fond Navy — bouton hero page méthode |

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

### Composants OCTAO spécifiques

| Composant | Variantes / Tokens | Rôle |
|---|---|---|
| `<KPICard>` | Display 64 / Royal Blue / icône TrendingUp 32 | KPI hero d'une page — chiffre + delta + sparkline |
| `<SkillBadge>` | h 24 / radius pill / couleur famille métier | Badge skill avec couleur de famille (13 variantes) |
| `<GhostScore>` | Bar visuelle 100 % / seuils 0.7 et 0.85 | Score ghost avec barre — vert / ambre / rouge |
| `<ConfidenceBadge>` | Score 0-1 / Royal Soft, Warning, Error | Confiance d'extraction Pydantic AI |
| `<SourceStatus>` | Dot 8 px / Success / Warning / Error | Statut source — last scraped, count, ok/erreur |
| `<FiltersBar>` | Header 64 / Navy 900 / icônes Lucide M | Barre globale de filtres — pays, période, famille |
| `<DataTable>` | TanStack Table / tabular figures / mono hex | Tables QC, taxonomy review, export datasets |
| `<PlotlyChart>` | Wrapper / palette familles + Royal Blue accent | Bar, treemap, heatmap — visualisations principales |
| `<ReportCard>` | Card / preview thumbnail / Download icon | Card de rapport généré — preview + bouton télécharger |

### Exemple — Card métier (mode dark)

```
┌──────────────────────────────────────────────────────────────────┐
│ IT & NUMÉRIQUE  ·  GUINÉE  ·  T1 2026                            │
│                                                                  │
│ Développeur Full-Stack                                           │
│ 247 offres analysées sur la période                              │
│                                                                  │
│ Score ghost — gestion de projet Agile               0.85         │
│ Croissance demande sur 3 mois                       +18 %        │
│ Présence dans les cursus de référence               0 / 10       │
└──────────────────────────────────────────────────────────────────┘
   bg #051C2C  ·  text #F5F1EB  ·  accent #4F73FF
```

---

## 07 — Variables CSS

Bloc `:root` prêt à copier-coller dans un projet **Next.js 15 avec Tailwind v4**. Les tokens couvrent palette, typographie, spacing, layout et basculent automatiquement entre mode dark (par défaut) et mode light via l'attribut `data-theme`.

```css
/* ============================================ */
/* OCTAO Design Tokens — McKinsey-inspired      */
/* Mode dark dominant. Compatible Tailwind v4.  */
/* ============================================ */

:root {
  /* Primary — Navy McKinsey */
  --octao-navy:        #051C2C;
  --octao-navy-900:    #0A2540;
  --octao-navy-800:    #133553;
  --octao-navy-700:    #1F4868;

  /* Accent — Royal Blue */
  --octao-royal:       #2251FF;
  --octao-royal-light: #4F73FF;
  --octao-royal-dark:  #1A3FCC;
  --octao-royal-soft:  #E5EBFF;

  /* Surfaces light */
  --octao-white:       #FFFFFF;
  --octao-cream:       #FAF8F3;
  --octao-bone:        #F5F1EB;
  --octao-border:      #E5E7EB;

  /* Text */
  --octao-ink:         #1A1A1A;
  --octao-ink-soft:    #4A4A4A;
  --octao-muted:       #6B7280;

  /* Semantic */
  --octao-success:     #0F8F65;
  --octao-warning:     #C77700;
  --octao-error:       #B42318;
  --octao-info:        #2251FF;

  /* Familles métiers OCTAO */
  --fam-sante:         #B42318;
  --fam-droit:         #4A1D6E;
  --fam-gestion:       #2251FF;
  --fam-finance:       #0F8F65;
  --fam-marketing:     #C77700;
  --fam-ingenierie:    #1F4868;
  --fam-it:            #7C3AED;
  --fam-rh:            #0891B2;
  --fam-agri:          #5C7E2A;
  --fam-education:     #1A3FCC;
  --fam-social:        #BE185D;
  --fam-logistique:    #78716C;
  --fam-support:       #525252;

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

  /* Mode dark — defaults */
  --bg:              var(--octao-navy);
  --surface:         var(--octao-navy-900);
  --surface-2:       var(--octao-navy-800);
  --text:            var(--octao-bone);
  --text-muted:      #8FA3B8;
  --border-color:    var(--octao-navy-700);
  --accent:          var(--octao-royal);
}

[data-theme="light"] {
  --bg:              var(--octao-white);
  --surface:         var(--octao-cream);
  --surface-2:       var(--octao-white);
  --text:            var(--octao-ink);
  --text-muted:      var(--octao-muted);
  --border-color:    var(--octao-border);
  --accent:          var(--octao-royal);
}
```

---

**Référence design officielle — OCTAO**
SYLI Technology · MESRS République de Guinée · Mai 2026
