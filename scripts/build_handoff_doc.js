/**
 * Génère docs/handoff/SKILLNAV_Guide_Modelisation_Structure_Mining.docx
 *
 * Version concise : 4 sections + une page de garde sobre, sans signature
 * ni mention de soutenance. Formulations à la troisième personne, sans « tu ».
 *
 * Exécution : node scripts/build_handoff_doc.js
 */

const fs = require("fs");
const path = require("path");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  AlignmentType,
  LevelFormat,
  HeadingLevel,
  BorderStyle,
  WidthType,
  ShadingType,
  PageBreak,
  TabStopType,
  TabStopPosition,
  Header,
  Footer,
  PageNumber,
} = require("docx");

// ---------------------------------------------------------------------------
// Mise en page A4
// ---------------------------------------------------------------------------
const A4_WIDTH = 11906;
const A4_HEIGHT = 16838;
const MARGIN = 1440;
const CONTENT_WIDTH = A4_WIDTH - MARGIN * 2;

const COULEUR_TITRE = "1565C0";
const COULEUR_NEUTRE = "424242";
const COULEUR_ACCENT = "EF6C00";
const COULEUR_BORDURE = "BDBDBD";
const COULEUR_FOND_ENTETE = "E3F2FD";

const OUT_DIR = path.resolve(__dirname, "..", "docs", "handoff");
const OUT_FILE = path.join(OUT_DIR, "SKILLNAV_Guide_Modelisation_Structure_Mining.docx");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const border = (color = COULEUR_BORDURE, size = 4) => ({
  style: BorderStyle.SINGLE,
  size,
  color,
});
const cellBorders = { top: border(), bottom: border(), left: border(), right: border() };

function p(texte, options = {}) {
  return new Paragraph({
    spacing: { after: 120, line: 320 },
    alignment: options.alignment || AlignmentType.JUSTIFIED,
    children: [
      new TextRun({
        text: texte,
        size: options.size || 22,
        color: options.color || COULEUR_NEUTRE,
        bold: options.bold || false,
        italics: options.italics || false,
      }),
    ],
  });
}

function pMixte(parts, options = {}) {
  return new Paragraph({
    spacing: { after: 120, line: 320 },
    alignment: options.alignment || AlignmentType.JUSTIFIED,
    children: parts.map(
      (q) =>
        new TextRun({
          text: q.text,
          bold: q.bold || false,
          italics: q.italics || false,
          font: q.font,
          size: q.size || 22,
          color: q.color || COULEUR_NEUTRE,
        })
    ),
  });
}

function h1(texte) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 200 },
    children: [new TextRun({ text: texte, size: 32, bold: true, color: COULEUR_TITRE })],
  });
}

function h2(texte) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 300, after: 140 },
    children: [new TextRun({ text: texte, size: 26, bold: true, color: COULEUR_TITRE })],
  });
}

function bullet(texte) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: [new TextRun({ text: texte, size: 22, color: COULEUR_NEUTRE })],
  });
}

function bulletMixte(parts) {
  return new Paragraph({
    numbering: { reference: "bullets", level: 0 },
    spacing: { after: 80 },
    children: parts.map(
      (q) =>
        new TextRun({
          text: q.text,
          bold: q.bold || false,
          italics: q.italics || false,
          font: q.font,
          size: q.size || 22,
          color: q.color || COULEUR_NEUTRE,
        })
    ),
  });
}

function cellule(contenu, options = {}) {
  const width = options.width;
  const enTete = options.enTete || false;
  const enfants = Array.isArray(contenu) ? contenu : [contenu];

  const paragraphs = enfants.map((c) =>
    typeof c === "string"
      ? new Paragraph({
          spacing: { after: 40 },
          children: [
            new TextRun({
              text: c,
              size: 20,
              bold: enTete,
              color: enTete ? COULEUR_TITRE : COULEUR_NEUTRE,
            }),
          ],
        })
      : c
  );

  return new TableCell({
    borders: cellBorders,
    width: { size: width, type: WidthType.DXA },
    shading: enTete ? { fill: COULEUR_FOND_ENTETE, type: ShadingType.CLEAR } : undefined,
    margins: { top: 100, bottom: 100, left: 140, right: 140 },
    children: paragraphs,
  });
}

function tab(enTetes, lignes, largeurs) {
  return new Table({
    width: { size: CONTENT_WIDTH, type: WidthType.DXA },
    columnWidths: largeurs,
    rows: [
      new TableRow({
        tableHeader: true,
        children: enTetes.map((t, i) => cellule(t, { width: largeurs[i], enTete: true })),
      }),
      ...lignes.map(
        (l) => new TableRow({ children: l.map((c, i) => cellule(c, { width: largeurs[i] })) })
      ),
    ],
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// ---------------------------------------------------------------------------
// Contenu
// ---------------------------------------------------------------------------
const contenu = [];

// --- Page de garde sobre (sans signature ni date de soutenance) ---
contenu.push(
  new Paragraph({
    spacing: { before: 3600, after: 400 },
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({ text: "SKILLNAV", size: 64, bold: true, color: COULEUR_TITRE }),
    ],
  })
);

contenu.push(
  new Paragraph({
    spacing: { after: 1400 },
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: "Observatoire des compétences IA et Data Science",
        size: 24,
        italics: true,
        color: COULEUR_NEUTRE,
      }),
    ],
  })
);

contenu.push(
  new Paragraph({
    spacing: { after: 200 },
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: "Guide de modélisation",
        size: 44,
        bold: true,
        color: COULEUR_NEUTRE,
      }),
    ],
  })
);

contenu.push(
  new Paragraph({
    spacing: { after: 1600 },
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: "Volet Structure Mining",
        size: 28,
        color: COULEUR_ACCENT,
      }),
    ],
  })
);

contenu.push(
  new Paragraph({
    spacing: { after: 120 },
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: "Module M242 — Analyse de Web",
        size: 22,
        color: COULEUR_NEUTRE,
      }),
    ],
  })
);

contenu.push(
  new Paragraph({
    spacing: { after: 120 },
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: "École Nationale des Sciences Appliquées de Tétouan",
        size: 22,
        color: COULEUR_NEUTRE,
      }),
    ],
  })
);

contenu.push(
  new Paragraph({
    spacing: { after: 120 },
    alignment: AlignmentType.CENTER,
    children: [
      new TextRun({
        text: "Encadrement : Pr. Imad Sassi",
        size: 22,
        color: COULEUR_NEUTRE,
      }),
    ],
  })
);

contenu.push(pageBreak());

// --- Section 1 : Ce que « modélisation » veut dire dans M242 ---
contenu.push(h1("1. Ce que « modélisation » veut dire dans M242"));

contenu.push(
  p(
    "On pourrait croire que « modélisation » signifie ML supervisé (régression, classification). Ce n'est pas le cas dans le contexte du sujet imposé. M242 attend trois choses, alignées sur les trois axes Web Mining."
  )
);

contenu.push(
  tab(
    ["Axe Web Mining", "Type de modélisation attendu", "Responsable"],
    [
      [
        "Content Mining",
        "NER comparatif (BERT multilingue, CamemBERT, DistilBERT) pour l'extraction des compétences à partir du texte brut",
        "Karamo Sylla",
      ],
      [
        "Structure Mining",
        "Modélisation en graphe (nœuds Job / Skill / Company + arêtes), puis algorithmes de communautés (Louvain, Leiden, Label Propagation, PageRank)",
        "Bachirou Konaté",
      ],
      [
        "Usage Mining",
        "Forecasting temporel (ARIMA, Prophet, LSTM) sur les compétences émergentes",
        "Bachirou Konaté",
      ],
    ],
    [2200, 5026, 1800]
  )
);

contenu.push(
  pMixte([
    {
      text: "S'y ajoute la modélisation NoSQL polyglotte du PRD §7 : MongoDB (source of truth) + Neo4j (graphe) + Elasticsearch (recherche). Il s'agit de modélisation de schéma, et non de machine learning. Cette partie reste pilotée par Karamo Sylla.",
    },
  ])
);

contenu.push(
  pMixte([
    { text: "Conclusion : ", bold: true },
    {
      text: "la part de Bachirou Konaté couvre désormais deux axes. D'une part la construction du graphe Skill ↔ Job dans Neo4j puis l'exécution comparative de quatre algorithmes de communautés (§N2.2 du PRD). D'autre part le forecasting temporel des compétences émergentes (§N2.3 du PRD) via ARIMA, Prophet et LSTM. Ces deux volets constituent l'essentiel du Sprint 2 et du Sprint 3.",
    },
  ])
);

// --- Section 2 : Qui fait quoi ---
contenu.push(h1("2. Qui fait quoi (RACI, focus modélisation)"));

contenu.push(
  tab(
    ["Tâche de modélisation", "Karamo Sylla", "Bachirou Konaté"],
    [
      ["Schémas Pydantic (skillnav/schemas/)", "A R", "C"],
      ["Insertion MongoDB Atlas", "A R", "I"],
      ["Construction du graphe Neo4j", "C", "A R"],
      ["Algorithmes de communautés (Louvain, Leiden, ...)", "I", "A R"],
      ["Tableau comparatif §N2.2", "I", "A R"],
      ["NER comparatif (§N2.1)", "A R", "C"],
      ["Forecasting Usage Mining (§N2.3)", "I", "A R"],
      ["Indexation Elasticsearch", "A R", "I"],
    ],
    [5026, 2000, 2000]
  )
);

contenu.push(
  p(
    "La responsabilité immédiate côté Karamo Sylla consiste à préparer le terrain afin que Bachirou Konaté puisse attaquer le volet Structure Mining sans friction."
  )
);

// --- Section 3 : Format de données ---
contenu.push(h1("3. Format de données : pourquoi le faire évoluer"));

contenu.push(
  p(
    "Le format YAML actuel reste parfait pour l'EDA — c'est-à-dire lisible humainement, ce qui a guidé les deux notebooks existants. Deux limites apparaissent toutefois pour la modélisation."
  )
);

contenu.push(
  tab(
    ["Limite", "Conséquence"],
    [
      [
        "3 467 fichiers à parser à chaque chargement",
        "Lent, en particulier dès qu'une itération fréquente est nécessaire (cas typique du graphe)",
      ],
      [
        "Pas directement consommable par Neo4j, MongoDB ou Elasticsearch",
        "Risque de mobiliser deux jours d'écriture de parseur du côté Structure Mining",
      ],
    ],
    [4500, 4526]
  )
);

contenu.push(h2("3.1 Approche retenue"));

contenu.push(
  p(
    "Le format YAML d'origine est conservé en tant que source brute. Trois formats dérivés viennent s'ajouter, chacun optimisé pour son usage."
  )
);

contenu.push(
  tab(
    ["Fichier dérivé", "Format", "Usage", "Consommateur"],
    [
      [
        "data/jobs.jsonl",
        "JSON Lines (un job par ligne)",
        "Source unifiée importable d'un seul mongoimport",
        "MongoDB + dashboard backend",
      ],
      [
        "data/graph_nodes.csv",
        "CSV (id, type, label, attributs)",
        "Nœuds Neo4j (Job, Skill, Company)",
        "Bachirou Konaté via Neo4j LOAD CSV",
      ],
      [
        "data/graph_edges.csv",
        "CSV (source_id, target_id, type, weight)",
        "Arêtes Neo4j (REQUIRES, POSTED_BY)",
        "Bachirou Konaté via Neo4j LOAD CSV",
      ],
    ],
    [2200, 2400, 2426, 2000]
  )
);

contenu.push(h2("3.2 Justification du choix de format par cible"));

contenu.push(
  bullet(
    "Neo4j dispose d'une commande native LOAD CSV qui crée des arêtes en bulk, ce qui constitue le pattern standard pour bootstrapper un graphe à partir d'un dump."
  )
);
contenu.push(
  bullet(
    "JSON Lines est le format privilégié de MongoDB et d'Elasticsearch pour l'import bulk."
  )
);
contenu.push(
  bullet(
    "Le YAML d'origine reste la source brute, utile à la lecture humaine, à l'audit qualité et au retour aux annonces originales."
  )
);

// --- Section 4 : Plan d'action ---
contenu.push(h1("4. Plan d'action en trois phases"));

contenu.push(h2("Phase A : préparation (Karamo Sylla, environ trois heures)"));
contenu.push(p("Trois artefacts à produire avant le démarrage du Sprint 2."));

contenu.push(
  tab(
    ["Artefact", "Contenu"],
    [
      [
        "scripts/build_dataset.py",
        "Lit les 3 467 YAML via skillnav_eda.charger_corpus puis écrit data/jobs.jsonl, data/graph_nodes.csv et data/graph_edges.csv",
      ],
      [
        "notebooks/02_graph_starter.ipynb",
        "Template prêt à l'emploi : import skillnav_eda, connexion Neo4j AuraDB, chargement des CSV, exemple Louvain commenté, et trois TODO pour Leiden, Label Propagation et PageRank",
      ],
      [
        "docs/MODELISATION_GUIDE.md",
        "Document de référence rappelant l'architecture (Mongo + Neo4j + ES), le schéma du graphe, la procédure de création du compte AuraDB et le tableau comparatif §N2.2 à compléter",
      ],
    ],
    [3000, 6026]
  )
);

contenu.push(h2("Phase B : exécution Structure Mining et Forecasting (Bachirou Konaté, Sprint 2 et 3)"));

contenu.push(p("Volet Structure Mining (Sprint 2, J7 à J12)."));
contenu.push(bullet("Suivre MODELISATION_GUIDE.md pas à pas."));
contenu.push(bullet("Lancer 02_graph_starter.ipynb pour peupler le graphe Neo4j."));
contenu.push(bullet("Exécuter Louvain, Leiden, Label Propagation et PageRank."));
contenu.push(
  bullet(
    "Comparer les métriques : modularité, nombre de communautés, temps d'exécution, top compétences par communauté."
  )
);
contenu.push(bullet("Compléter le tableau §N2.2 dans le rapport méthodologique L5."));
contenu.push(bullet("Exporter une visualisation du graphe (PNG ou HTML)."));

contenu.push(p("Volet Usage Mining — Forecasting (Sprint 3, J13 à J18)."));
contenu.push(bullet("Construire les séries temporelles de compétences à partir du corpus consolidé."));
contenu.push(bullet("Implémenter ARIMA, Prophet et LSTM sur un panel d'au moins dix compétences phares."));
contenu.push(bullet("Comparer les performances (MAPE, RMSE, temps d'entraînement) dans le tableau §N2.3."));
contenu.push(bullet("Rédiger la section §N2.3 du rapport L5 et exporter les courbes de prévision."));

contenu.push(h2("Phase C : travail parallèle (Karamo Sylla, Sprint 2 et 3)"));

contenu.push(bullet("NER comparatif (§N2.1) sur les descriptions de poste."));
contenu.push(bullet("Modélisation NoSQL polyglotte : MongoDB Atlas, Neo4j (mise à disposition), Elasticsearch Cloud."));
contenu.push(
  bullet(
    "Dashboard Next.js — pages /graph et /forecasting alimentées par les modèles produits par Bachirou Konaté."
  )
);

// --- Section 5 : Décisions à valider ---
// --- Section 5 : Détail du notebook starter ---
contenu.push(h1("5. Détail du notebook 02_graph_starter.ipynb"));

contenu.push(
  p(
    "Le notebook livré en Phase A est un starter kit dont le rôle est de préparer l'environnement Neo4j et de servir de patron pour le travail algorithmique. Sa structure est volontairement dichotomique : la moitié technique (connexion, chargement bulk, exemple Louvain commenté) est livrée prête à l'emploi ; l'autre moitié (trois algorithmes restants, interprétation, synthèse §N2.2) constitue le périmètre d'évaluation du volet Structure Mining."
  )
);

contenu.push(h2("5.1 Cellules livrées clés en main (Phase A)"));

contenu.push(
  tab(
    ["§", "Section du notebook", "État"],
    [
      ["0", "Setup : connexion Neo4j AuraDB via .env", "Prête à exécuter"],
      ["1", "Vérification des artefacts CSV générés par build_dataset.py", "Prête à exécuter"],
      ["2", "Contraintes d'unicité et index Cypher", "Prête à exécuter"],
      ["3", "Chargement bulk des 13 071 nœuds (UNWIND par batches de 500)", "Prête à exécuter"],
      ["4", "Chargement bulk des 62 341 arêtes (REQUIRES et POSTED_BY)", "Prête à exécuter"],
      ["5", "Validation par comptages côté Neo4j", "Prête à exécuter"],
      ["6", "Exemple complet : algorithme Louvain (commenté)", "Prête à exécuter, sert de patron"],
      ["9", "Fermeture propre du driver Neo4j", "Prête à exécuter"],
    ],
    [600, 6000, 2426]
  )
);

contenu.push(h2("5.2 Cellules à compléter en Phase B"));

contenu.push(
  tab(
    ["§", "Section du notebook", "Action attendue"],
    [
      ["7", "Leiden", "Adapter la requête Cypher (gds.leiden.stream) sur le patron Louvain, mesurer durée et nombre de communautés"],
      ["7", "Label Propagation", "Adapter (gds.labelPropagation.stream), même méthode"],
      ["7", "PageRank", "Calculer les centralités, extraire le top 20 compétences"],
      ["8", "Tableau comparatif §N2.2", "Reporter les métriques des quatre algorithmes (communautés, modularité, temps, notes)"],
    ],
    [600, 2800, 5626]
  )
);

contenu.push(h2("5.3 Logique du découpage"));

contenu.push(
  p(
    "Le travail livré clés en main couvre la plomberie technique : driver Neo4j, gestion des batches, optimisation des transactions, contraintes d'unicité. Cette partie est universelle et ne contribue pas à l'évaluation académique du volet."
  )
);

contenu.push(
  p(
    "Le travail à compléter couvre en revanche le contenu scientifique : choix des paramètres, exécution comparative des trois algorithmes restants, interprétation des résultats et rédaction de la synthèse. C'est ce périmètre qui porte la note §N2.2 du PRD et qui nourrit la section correspondante du rapport méthodologique L5."
  )
);

contenu.push(h1("6. Décisions à valider avant Phase A"));

contenu.push(h2("Choix 1 — Profondeur du graphe"));

contenu.push(
  tab(
    ["Approche", "Nœuds", "Arêtes", "Justification"],
    [
      ["Minimal", "Job + Skill", "REQUIRES", "Démarrage rapide, suffit pour Louvain de base"],
      [
        "Standard (recommandé)",
        "Job + Skill + Company",
        "REQUIRES, POSTED_BY",
        "Permet de répondre à la question « quelle entreprise recrute quelle famille »",
      ],
      [
        "Riche",
        "Job + Skill + Company + Source + Mois",
        "REQUIRES, POSTED_BY, FROM_SOURCE, POSTED_AT",
        "Coût en complexité élevé, pertinent seulement pour un graphe temporel",
      ],
    ],
    [2200, 2200, 2200, 2426]
  )
);

contenu.push(
  pMixte([
    { text: "Recommandation : ", bold: true },
    {
      text: "approche Standard. Elle couvre les besoins des quatre algorithmes et laisse une marge pour des analyses bonus.",
    },
  ])
);

contenu.push(h2("Choix 2 — Neo4j local ou Neo4j AuraDB"));

contenu.push(
  tab(
    ["Option", "Pour", "Contre"],
    [
      ["Neo4j Desktop local", "Pas de quota, pas d'authentification distante", "Nécessite une installation locale"],
      [
        "AuraDB Free Tier (recommandé)",
        "Aucune installation, accessible partout, démonstration plus professionnelle en soutenance",
        "Limité à 50 000 nœuds (la volumétrie cible est d'environ 5 000)",
      ],
    ],
    [2800, 3200, 3026]
  )
);

contenu.push(
  pMixte([
    { text: "Recommandation : ", bold: true },
    { text: "AuraDB Free Tier. Aligné avec le PRD §7 et avec la démonstration de soutenance." },
  ])
);

contenu.push(
  p(
    "Une validation du couple « Standard + AuraDB » autorise le lancement immédiat de la Phase A : script de consolidation, notebook template et guide markdown."
  )
);

// ---------------------------------------------------------------------------
// Document
// ---------------------------------------------------------------------------
const doc = new Document({
  creator: "SKILLNAV",
  title: "SKILLNAV — Guide de modélisation : volet Structure Mining",
  description: "Document de passation pour le volet Structure Mining (M242 ENSA-Tétouan).",
  styles: {
    default: { document: { run: { font: "Calibri", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1",
        name: "Heading 1",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 32, bold: true, font: "Calibri", color: COULEUR_TITRE },
        paragraph: { spacing: { before: 400, after: 200 }, outlineLevel: 0 },
      },
      {
        id: "Heading2",
        name: "Heading 2",
        basedOn: "Normal",
        next: "Normal",
        quickFormat: true,
        run: { size: 26, bold: true, font: "Calibri", color: COULEUR_TITRE },
        paragraph: { spacing: { before: 300, after: 140 }, outlineLevel: 1 },
      },
    ],
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          {
            level: 0,
            format: LevelFormat.BULLET,
            text: "•",
            alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 720, hanging: 360 } } },
          },
        ],
      },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: A4_WIDTH, height: A4_HEIGHT },
          margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN },
        },
      },
      headers: {
        default: new Header({
          children: [
            new Paragraph({
              alignment: AlignmentType.LEFT,
              children: [
                new TextRun({
                  text: "SKILLNAV — Guide de modélisation Structure Mining",
                  size: 18,
                  color: COULEUR_NEUTRE,
                  italics: true,
                }),
                new TextRun({ text: "\t" }),
                new TextRun({
                  text: "ENSA-Tétouan — M242",
                  size: 18,
                  color: COULEUR_NEUTRE,
                  italics: true,
                }),
              ],
              tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
              border: {
                bottom: { style: BorderStyle.SINGLE, size: 6, color: COULEUR_TITRE, space: 4 },
              },
            }),
          ],
        }),
      },
      footers: {
        default: new Footer({
          children: [
            new Paragraph({
              alignment: AlignmentType.CENTER,
              children: [
                new TextRun({ text: "Page ", size: 18, color: COULEUR_NEUTRE }),
                new TextRun({
                  children: [PageNumber.CURRENT],
                  size: 18,
                  color: COULEUR_NEUTRE,
                }),
                new TextRun({ text: " / ", size: 18, color: COULEUR_NEUTRE }),
                new TextRun({
                  children: [PageNumber.TOTAL_PAGES],
                  size: 18,
                  color: COULEUR_NEUTRE,
                }),
              ],
            }),
          ],
        }),
      },
      children: contenu,
    },
  ],
});

// ---------------------------------------------------------------------------
// Sérialisation
// ---------------------------------------------------------------------------
fs.mkdirSync(OUT_DIR, { recursive: true });

Packer.toBuffer(doc).then((buffer) => {
  fs.writeFileSync(OUT_FILE, buffer);
  const stats = fs.statSync(OUT_FILE);
  console.log("DOCX écrit :", OUT_FILE);
  console.log("Taille :", Math.round(stats.size / 1024), "Ko");
  console.log("Paragraphes :", contenu.length);
});
