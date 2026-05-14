#!/usr/bin/env node
/**
 * SKILLNAV — Charte graphique — Generator DOCX premium
 *
 * Hybride : structure IA5D (cover full-bleed Navy, TOC, sections 01 + label,
 * palette en cards 4 colonnes) + esthétique McKinsey-Fraunces (titres serif).
 *
 * Cible : 11–13 pages premium.
 */

import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..");
const OUT_DOCX = resolve(REPO_ROOT, "docs", "CHARTE_GRAPHIQUE_SKILLNAV.docx");

const require = createRequire(import.meta.url);
const GLOBAL = "C:/Users/ksthe/AppData/Roaming/npm/node_modules";
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  Table,
  TableRow,
  TableCell,
  Header,
  Footer,
  AlignmentType,
  HeadingLevel,
  BorderStyle,
  WidthType,
  ShadingType,
  VerticalAlign,
  PageNumber,
  PageBreak,
  TabStopType,
  TabStopPosition,
  HeightRule,
  SectionType,
  TableLayoutType,
} = require(`${GLOBAL}/docx`);

// --- Tokens charte SKILLNAV ----------------------------------------------------
const C = {
  navy: "051C2C",
  navy900: "0A2540",
  navy800: "133553",
  navy700: "1F4868",
  royal: "2251FF",
  royalLight: "4F73FF",
  royalDark: "1A3FCC",
  royalSoft: "E5EBFF",
  white: "FFFFFF",
  cream: "FAF8F3",
  bone: "F5F1EB",
  border: "E5E7EB",
  ink: "1A1A1A",
  inkSoft: "4A4A4A",
  muted: "6B7280",
  success: "0F8F65",
  warning: "C77700",
  error: "B42318",
  // Familles IA
  fmlClassique: "2251FF",
  fmlDeep: "7C3AED",
  fmlNlp: "0891B2",
  fmlCv: "C77700",
  fmlDataEng: "1F4868",
  fmlMlops: "0F8F65",
  fmlCloud: "1A3FCC",
  fmlEthics: "4A1D6E",
  fmlStats: "5C7E2A",
  fmlTools: "6B7280",
};

const FONT_DISPLAY = "Georgia"; // proxy serif éditorial Fraunces (Windows-native)
const FONT_BODY = "Calibri";
const FONT_MONO = "Consolas";

// --- Helpers -------------------------------------------------------------------
const NO_BORDER_ALL = (() => {
  const none = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
  return {
    top: none, bottom: none, left: none, right: none,
    insideHorizontal: none, insideVertical: none,
  };
})();

function p(text, opts = {}) {
  const {
    font = FONT_BODY,
    size = 22,
    color = C.ink,
    bold = false,
    italics = false,
    align = AlignmentType.LEFT,
    spaceBefore = 0,
    spaceAfter = 120,
    indent,
    line = 320,
  } = opts;
  return new Paragraph({
    alignment: align,
    indent,
    spacing: { before: spaceBefore, after: spaceAfter, line, lineRule: "auto" },
    children: text === null
      ? []
      : Array.isArray(text)
        ? text
        : [new TextRun({ text, font, size, color, bold, italics })],
  });
}

function tr(text, opts = {}) {
  return new TextRun({
    text,
    font: opts.font || FONT_BODY,
    size: opts.size || 20,
    color: opts.color || C.ink,
    bold: opts.bold || false,
    italics: opts.italics || false,
  });
}

function emptyP(spaceAfter = 120) {
  return p(null, { spaceAfter });
}

// --- Section header style IA5D : "NN" + LABEL UPPER + trait Royal --------------
function sectionTitle(num, label, sublabel = null) {
  return [
    new Paragraph({
      spacing: { before: 0, after: 60, line: 240, lineRule: "auto" },
      children: [
        new TextRun({
          text: num,
          font: FONT_DISPLAY,
          size: 96, // 48pt
          color: C.royal,
          bold: false,
        }),
      ],
    }),
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 0, after: 0, line: 240, lineRule: "auto" },
      children: [
        new TextRun({
          text: label.toUpperCase(),
          font: FONT_BODY,
          size: 30, // 15pt
          color: C.navy,
          bold: true,
        }),
      ],
    }),
    sublabel
      ? p(sublabel, {
          font: FONT_DISPLAY,
          size: 32,
          color: C.navy,
          italics: true,
          spaceBefore: 240,
          spaceAfter: 120,
        })
      : null,
    // Trait Royal Blue
    new Paragraph({
      spacing: { before: 240, after: 360 },
      border: {
        bottom: {
          style: BorderStyle.SINGLE,
          size: 8,
          color: C.royal,
          space: 1,
        },
      },
      children: [],
    }),
  ].filter(Boolean);
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 360, after: 180, line: 280, lineRule: "auto" },
    children: [
      new TextRun({
        text,
        font: FONT_BODY,
        size: 26,
        color: C.navy,
        bold: true,
      }),
    ],
  });
}

function eyebrow(text, color = C.royal) {
  return p(text.toUpperCase(), {
    font: FONT_BODY,
    size: 16,
    color,
    bold: true,
    spaceAfter: 80,
  });
}

// --- Colour CARD style IA5D ---------------------------------------------------
function colorCard(hex, name, usage, opts = {}) {
  const isLight = opts.lightText !== undefined ? !opts.lightText : isLightHex(hex);
  const textColor = isLight ? C.ink : C.white;
  const cellW = opts.width || 2126;

  return new TableCell({
    width: { size: cellW, type: WidthType.DXA },
    borders: NO_BORDER_ALL,
    margins: { top: 60, bottom: 60, left: 60, right: 60 },
    verticalAlign: VerticalAlign.TOP,
    children: [
      // Bloc couleur avec hex à l'intérieur
      new Table({
        width: { size: cellW - 120, type: WidthType.DXA },
        columnWidths: [cellW - 120],
        borders: isLight
          ? {
              top: { style: BorderStyle.SINGLE, size: 4, color: C.border },
              bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
              left: { style: BorderStyle.SINGLE, size: 4, color: C.border },
              right: { style: BorderStyle.SINGLE, size: 4, color: C.border },
              insideHorizontal: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
              insideVertical: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            }
          : NO_BORDER_ALL,
        rows: [
          new TableRow({
            height: { value: 1100, rule: HeightRule.ATLEAST },
            children: [
              new TableCell({
                width: { size: cellW - 120, type: WidthType.DXA },
                borders: NO_BORDER_ALL,
                margins: { top: 200, bottom: 200, left: 220, right: 220 },
                verticalAlign: VerticalAlign.BOTTOM,
                shading: { fill: hex, type: ShadingType.CLEAR, color: "auto" },
                children: [
                  p(`#${hex}`, {
                    font: FONT_MONO,
                    size: 20,
                    color: textColor,
                    bold: true,
                    spaceAfter: 0,
                    line: 240,
                  }),
                ],
              }),
            ],
          }),
        ],
      }),
      // Sous le bloc : nom + usage
      p(name, {
        font: FONT_BODY,
        size: 20,
        color: C.navy,
        bold: true,
        spaceBefore: 120,
        spaceAfter: 40,
      }),
      p(usage, {
        font: FONT_BODY,
        size: 17,
        color: C.muted,
        spaceAfter: 0,
        line: 280,
      }),
    ],
  });
}

function isLightHex(hex) {
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  // luminance perceptuelle approximative
  return r * 0.299 + g * 0.587 + b * 0.114 > 186;
}

function colorCardRow(cards) {
  // Padding row to 4 columns with empty cells if needed
  while (cards.length < 4) {
    cards.push(
      new TableCell({
        width: { size: 2126, type: WidthType.DXA },
        borders: NO_BORDER_ALL,
        children: [emptyP(0)],
      }),
    );
  }
  return new TableRow({
    cantSplit: true,
    children: cards,
  });
}

function colorCardTable(cards) {
  return new Table({
    width: { size: 8504, type: WidthType.DXA },
    columnWidths: [2126, 2126, 2126, 2126],
    layout: TableLayoutType.FIXED,
    borders: NO_BORDER_ALL,
    rows: [colorCardRow(cards)],
  });
}

// --- Cover page (full-bleed Navy) ---------------------------------------------
function coverPage() {
  // Pour faire un full-bleed Navy en docx, on utilise une grosse table 1x1
  // avec hauteur ATLEAST (pas EXACT, sinon Word ajoute une page blanche).
  return [
    new Table({
      width: { size: 11906 - 600, type: WidthType.DXA },
      columnWidths: [11906 - 600],
      borders: NO_BORDER_ALL,
      rows: [
        new TableRow({
          // Pas de hauteur fixe : le contenu s'étire seul, le shading remplit la cellule
          cantSplit: true,
          children: [
            new TableCell({
              width: { size: 11906 - 600, type: WidthType.DXA },
              borders: NO_BORDER_ALL,
              margins: { top: 2400, bottom: 2400, left: 1100, right: 1100 },
              verticalAlign: VerticalAlign.CENTER,
              shading: { fill: C.navy, type: ShadingType.CLEAR, color: "auto" },
              children: [
                p("BRAND GUIDELINES", {
                  font: FONT_BODY,
                  size: 18,
                  color: C.royalLight,
                  bold: true,
                  spaceAfter: 180,
                }),
                // Trait Royal subtil
                new Paragraph({
                  spacing: { before: 0, after: 480 },
                  border: {
                    bottom: {
                      style: BorderStyle.SINGLE,
                      size: 4,
                      color: C.royalLight,
                      space: 1,
                    },
                  },
                  children: [],
                }),
                p("Charte", {
                  font: FONT_DISPLAY,
                  size: 56,
                  color: "C7D5E5",
                  italics: true,
                  spaceAfter: 60,
                }),
                p("Graphique", {
                  font: FONT_DISPLAY,
                  size: 144,
                  color: C.bone,
                  bold: true,
                  spaceAfter: 480,
                  line: 260,
                }),
                p("SKILLNAV", {
                  font: FONT_DISPLAY,
                  size: 88,
                  color: C.royalLight,
                  bold: true,
                  spaceAfter: 200,
                  line: 240,
                }),
                p([
                  tr("Skills Navigator —", { font: FONT_DISPLAY, size: 28, italics: true, color: "C7D5E5" }),
                  tr(" observatoire des compétences IA & Data Science.", {
                    font: FONT_BODY,
                    size: 24,
                    color: "C7D5E5",
                  }),
                ], { spaceAfter: 2400 }),
                // Footer cover
                p([
                  tr("M242 · ENSA-Tétouan", { font: FONT_BODY, size: 18, color: C.royalLight, bold: true }),
                  tr("        ", { font: FONT_BODY, size: 18, color: C.muted }),
                  tr("Karamo Sylla & Bachirou Konaté", { font: FONT_BODY, size: 18, color: "8FA3B8" }),
                  tr("        ", { font: FONT_BODY, size: 18, color: C.muted }),
                  tr("Mai 2026", { font: FONT_BODY, size: 18, color: "8FA3B8" }),
                ], { spaceAfter: 0 }),
              ],
            }),
          ],
        }),
      ],
    }),
    // Trailing paragraph minimal (Word ajoute toujours un para après une table ;
    // on le rend invisible avec font size 2 pour qu'il tienne sur la page cover)
    new Paragraph({
      spacing: { before: 0, after: 0, line: 100, lineRule: "auto" },
      children: [new TextRun({ text: "", font: FONT_BODY, size: 2 })],
    }),
  ];
}

// --- Table des matières -------------------------------------------------------
function tocPage() {
  const tocRow = (num, label) =>
    new TableRow({
      cantSplit: true,
      height: { value: 600, rule: HeightRule.ATLEAST },
      children: [
        new TableCell({
          width: { size: 1200, type: WidthType.DXA },
          borders: NO_BORDER_ALL,
          margins: { top: 100, bottom: 100, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(num, {
              font: FONT_DISPLAY,
              size: 36,
              color: C.royal,
              bold: true,
              spaceAfter: 0,
              line: 240,
            }),
          ],
        }),
        new TableCell({
          width: { size: 7304, type: WidthType.DXA },
          borders: NO_BORDER_ALL,
          margins: { top: 100, bottom: 100, left: 200, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(label, {
              font: FONT_BODY,
              size: 24,
              color: C.ink,
              spaceAfter: 0,
              line: 240,
            }),
          ],
        }),
      ],
    });

  return [
    eyebrow("Sommaire"),
    new Paragraph({
      heading: HeadingLevel.HEADING_1,
      spacing: { before: 0, after: 120, line: 280, lineRule: "auto" },
      children: [
        new TextRun({
          text: "Table des matières",
          font: FONT_DISPLAY,
          size: 64,
          color: C.navy,
          bold: true,
        }),
      ],
    }),
    new Paragraph({
      spacing: { before: 0, after: 480 },
      border: {
        bottom: { style: BorderStyle.SINGLE, size: 8, color: C.royal, space: 1 },
      },
      children: [],
    }),
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [1200, 7304],
      borders: NO_BORDER_ALL,
      rows: [
        tocRow("01", "Direction artistique"),
        tocRow("02", "Palette principale — Navy & Royal Blue"),
        tocRow("03", "Palette neutres & sémantiques"),
        tocRow("04", "Familles IA / Data Science"),
        tocRow("05", "Typographie"),
        tocRow("06", "Iconographie & espacements"),
        tocRow("07", "Composants UI"),
        tocRow("08", "Variables CSS"),
      ],
    }),
    new Paragraph({
      spacing: { before: 240, after: 0 },
      border: {
        bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border, space: 1 },
      },
      children: [],
    }),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 01 Direction artistique --------------------------------------------------
function sectionDirection() {
  const principleCell = (num, title, body) =>
    new TableCell({
      width: { size: 4252, type: WidthType.DXA },
      borders: NO_BORDER_ALL,
      margins: { top: 240, bottom: 240, left: 240, right: 240 },
      shading: { fill: C.cream, type: ShadingType.CLEAR, color: "auto" },
      verticalAlign: VerticalAlign.TOP,
      children: [
        p(num, {
          font: FONT_MONO,
          size: 16,
          color: C.royal,
          bold: true,
          spaceAfter: 60,
        }),
        p(title, {
          font: FONT_DISPLAY,
          size: 26,
          color: C.navy,
          bold: true,
          spaceAfter: 100,
          line: 280,
        }),
        p(body, {
          font: FONT_BODY,
          size: 19,
          color: C.inkSoft,
          line: 320,
          spaceAfter: 0,
        }),
      ],
    });

  return [
    ...sectionTitle("01", "Direction artistique"),
    p(
      "« Cartographier les compétences IA, sans dramatiser. SKILLNAV mesure l'évolution du marché de l'expertise data avec la rigueur d'un institut de recherche et la sobriété d'une publication scientifique. »",
      {
        font: FONT_DISPLAY,
        size: 24,
        italics: true,
        color: C.navy800,
        spaceAfter: 240,
        line: 360,
      },
    ),
    p(
      "L'identité visuelle de SKILLNAV reproduit fidèlement les codes de McKinsey & Company : navy profond, royal blue électrique, serif éditorial, grotesque institutionnelle. Aucun ornement décoratif — le contenu porte le sens.",
      { spaceAfter: 360 },
    ),
    h2("Quatre principes directeurs"),
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [4252, 4252],
      layout: TableLayoutType.FIXED,
      borders: NO_BORDER_ALL,
      rows: [
        new TableRow({
          cantSplit: true,
          children: [
            principleCell(
              "01",
              "Autorité éditoriale",
              "Hiérarchie typographique forte. Serif Display pour les titres. Chaque écran se lit comme une publication de référence.",
            ),
            principleCell(
              "02",
              "Sobriété radicale",
              "Aucune ombre, aucun gradient, aucune illustration décorative. Le design s'efface devant la donnée.",
            ),
          ],
        }),
        new TableRow({
          cantSplit: true,
          children: [
            principleCell(
              "03",
              "Densité assumée",
              "Le dashboard analytique est dense : c'est un outil pour chercheur. Les pages méthode aèrent le rythme.",
            ),
            principleCell(
              "04",
              "Honnêteté méthodologique",
              "Disclaimers automatiques, badges de confiance visibles, intervalles de confiance affichés. La transparence est un élément graphique.",
            ),
          ],
        }),
      ],
    }),
    emptyP(360),
    h2("Attributs de marque"),
    p([
      tr("INSTITUTIONNEL", { font: FONT_MONO, size: 16, color: C.royal, bold: true }),
      tr("   ·   ", { font: FONT_MONO, size: 16, color: C.border }),
      tr("ÉDITORIAL", { font: FONT_MONO, size: 16, color: C.royal, bold: true }),
      tr("   ·   ", { font: FONT_MONO, size: 16, color: C.border }),
      tr("SOBRE", { font: FONT_MONO, size: 16, color: C.royal, bold: true }),
      tr("   ·   ", { font: FONT_MONO, size: 16, color: C.border }),
      tr("RIGOUREUX", { font: FONT_MONO, size: 16, color: C.royal, bold: true }),
      tr("   ·   ", { font: FONT_MONO, size: 16, color: C.border }),
      tr("SCIENTIFIQUE", { font: FONT_MONO, size: 16, color: C.royal, bold: true }),
    ]),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 02 Palette Primary + Accent (cards 4 colonnes) ---------------------------
function sectionPaletteMain() {
  return [
    ...sectionTitle("02", "Palette principale"),
    p(
      "Le couple Navy + Royal Blue signe l'identité McKinsey. Mode dark dominant pour le dashboard analytique ; mode light pour les exports impression.",
      { spaceAfter: 240 },
    ),
    // Bloc règle 60/30/10
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [8504],
      borders: NO_BORDER_ALL,
      rows: [
        new TableRow({
          cantSplit: true,
          children: [
            new TableCell({
              width: { size: 8504, type: WidthType.DXA },
              borders: {
                top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
                bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
                right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
                left: { style: BorderStyle.SINGLE, size: 24, color: C.royal, space: 1 },
              },
              margins: { top: 200, bottom: 200, left: 280, right: 280 },
              shading: { fill: C.royalSoft, type: ShadingType.CLEAR, color: "auto" },
              children: [
                p("RÈGLE DE RÉPARTITION 60 / 30 / 10", {
                  font: FONT_BODY,
                  size: 16,
                  color: C.royal,
                  bold: true,
                  spaceAfter: 100,
                }),
                p([
                  tr("60 % Navy ", { size: 20, color: C.ink, bold: true }),
                  tr("— fonds, panels, surfaces dominantes.   ", { size: 20, color: C.inkSoft }),
                ], { spaceAfter: 40 }),
                p([
                  tr("30 % Cream / White ", { size: 20, color: C.ink, bold: true }),
                  tr("— surfaces light, rapports imprimés.   ", { size: 20, color: C.inkSoft }),
                ], { spaceAfter: 40 }),
                p([
                  tr("10 % Royal Blue ", { size: 20, color: C.ink, bold: true }),
                  tr("— CTA, accents, focus, valeurs hero.", { size: 20, color: C.inkSoft }),
                ], { spaceAfter: 0 }),
              ],
            }),
          ],
        }),
      ],
    }),
    emptyP(360),

    h2("Primary — Navy McKinsey"),
    colorCardTable([
      colorCard(C.navy, "Navy 1000", "Background dominant dark mode."),
      colorCard(C.navy900, "Navy 900", "Sidebar, header, panels secondaires."),
      colorCard(C.navy800, "Navy 800", "Cards, modals, blocs de données."),
      colorCard(C.navy700, "Navy 700", "Bordures, séparateurs, hover dark."),
    ]),
    emptyP(360),

    h2("Accent — Royal Blue"),
    colorCardTable([
      colorCard(C.royal, "Royal Blue", "CTA, liens, valeurs hero, focus."),
      colorCard(C.royalLight, "Royal Blue 400", "Hover, badges actifs, highlight."),
      colorCard(C.royalDark, "Royal Blue 700", "Pressed state, charts comparatifs."),
      colorCard(C.royalSoft, "Royal Soft", "Backgrounds informatifs, callouts."),
    ]),

    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 03 Palette neutres + sémantiques -----------------------------------------
function sectionPaletteSecondary() {
  return [
    ...sectionTitle("03", "Neutres & sémantiques"),
    p(
      "Surfaces, neutres et couleurs sémantiques pour les états de l'interface (succès, alerte, erreur, information).",
      { spaceAfter: 360 },
    ),

    h2("Surfaces et neutres"),
    colorCardTable([
      colorCard(C.white, "White", "Surface card mode light."),
      colorCard(C.cream, "Cream", "Background light alternatif."),
      colorCard(C.bone, "Bone", "Texte sur fond Navy, deck PPTX."),
      colorCard(C.border, "Border 100", "Bordures légères mode light."),
    ]),
    emptyP(240),
    colorCardTable([
      colorCard(C.ink, "Ink", "Texte principal mode light."),
      colorCard(C.inkSoft, "Ink Soft", "Sous-titres, paragraphes secondaires."),
      colorCard(C.muted, "Muted", "Légendes, captions, labels."),
      colorCard(C.navy700, "Navy 700", "Séparateurs sur fond dark."),
    ]),
    emptyP(360),

    h2("Couleurs sémantiques"),
    colorCardTable([
      colorCard(C.success, "Success", "Tendances positives, score confirmé."),
      colorCard(C.warning, "Warning", "Faible échantillon, à confirmer."),
      colorCard(C.error, "Error", "Inadéquation grave, erreur système."),
      colorCard(C.royal, "Info", "Tooltips, callouts méthodologiques."),
    ]),

    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 04 Familles IA -----------------------------------------------------------
function sectionFamilies() {
  return [
    ...sectionTitle("04", "Familles IA / Data Science"),
    p(
      "Chaque famille de compétences SKILLNAV dispose d'un code couleur réservé : badges, nœuds Neo4j, segments de treemap, filtres. Calibrées pour rester lisibles sur Navy comme sur fond clair.",
      { spaceAfter: 360 },
    ),
    colorCardTable([
      colorCard(C.fmlClassique, "ML Classique", "scikit-learn, XGBoost, régression."),
      colorCard(C.fmlDeep, "Deep Learning", "PyTorch, Transformers, fine-tuning."),
      colorCard(C.fmlNlp, "NLP", "BERT, CamemBERT, RAG, spaCy."),
      colorCard(C.fmlCv, "Computer Vision", "OpenCV, YOLO, ViT, OCR."),
    ]),
    emptyP(240),
    colorCardTable([
      colorCard(C.fmlDataEng, "Data Engineering", "Spark, Airflow, Kafka, ETL."),
      colorCard(C.fmlMlops, "MLOps", "MLflow, Docker, CI/CD ML."),
      colorCard(C.fmlCloud, "Cloud & Big Data", "AWS, GCP, BigQuery, Snowflake."),
      colorCard(C.fmlEthics, "AI Ethics", "Bias, SHAP, RGPD, AI Act."),
    ]),
    emptyP(240),
    colorCardTable([
      colorCard(C.fmlStats, "Statistiques", "A/B testing, économétrie, SQL."),
      colorCard(C.fmlTools, "Outils & Soft Skills", "Python, Git, vulgarisation."),
    ]),

    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 05 Typographie -----------------------------------------------------------
function sectionTypography() {
  const fontShowcase = (label, fontName, sample, fontFamily, sizeHP) =>
    new TableRow({
      cantSplit: true,
      height: { value: 1100, rule: HeightRule.ATLEAST },
      children: [
        new TableCell({
          width: { size: 1800, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 200, bottom: 200, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(label, {
              font: FONT_BODY,
              size: 16,
              color: C.royal,
              bold: true,
              spaceAfter: 60,
            }),
            p(fontName, {
              font: FONT_BODY,
              size: 22,
              color: C.navy,
              bold: true,
              spaceAfter: 0,
            }),
          ],
        }),
        new TableCell({
          width: { size: 6704, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 200, bottom: 200, left: 200, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            new Paragraph({
              spacing: { before: 0, after: 0, line: 280, lineRule: "auto" },
              children: [
                new TextRun({
                  text: sample,
                  font: fontFamily,
                  size: sizeHP,
                  color: C.navy,
                }),
              ],
            }),
          ],
        }),
      ],
    });

  const hierarchyRow = (role, font, sizeStr, weight, usage) =>
    new TableRow({
      cantSplit: true,
      height: { value: 480, rule: HeightRule.ATLEAST },
      children: [
        new TableCell({
          width: { size: 1700, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 120, bottom: 120, left: 0, right: 100 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(role, { font: FONT_BODY, size: 20, color: C.ink, bold: true, spaceAfter: 0 }),
          ],
        }),
        new TableCell({
          width: { size: 2200, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 120, bottom: 120, left: 0, right: 100 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(font, { font: FONT_BODY, size: 19, color: C.inkSoft, spaceAfter: 0 }),
          ],
        }),
        new TableCell({
          width: { size: 1500, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 120, bottom: 120, left: 0, right: 100 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(sizeStr, { font: FONT_MONO, size: 19, color: C.navy800, spaceAfter: 0 }),
          ],
        }),
        new TableCell({
          width: { size: 1300, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 120, bottom: 120, left: 0, right: 100 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(weight, { font: FONT_BODY, size: 19, color: C.inkSoft, spaceAfter: 0 }),
          ],
        }),
        new TableCell({
          width: { size: 1804, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 120, bottom: 120, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(usage, { font: FONT_BODY, size: 19, color: C.inkSoft, spaceAfter: 0 }),
          ],
        }),
      ],
    });

  const headerRow = (cols) =>
    new TableRow({
      cantSplit: true,
      children: cols.map((c, i) =>
        new TableCell({
          width: {
            size: [1700, 2200, 1500, 1300, 1804][i],
            type: WidthType.DXA,
          },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 8, color: C.navy },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 100, bottom: 100, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(c, { font: FONT_BODY, size: 15, color: C.muted, bold: true, spaceAfter: 0 }),
          ],
        }),
      ),
    });

  return [
    ...sectionTitle("05", "Typographie"),
    // Système typographique en callout
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [8504],
      borders: NO_BORDER_ALL,
      rows: [
        new TableRow({
          cantSplit: true,
          children: [
            new TableCell({
              width: { size: 8504, type: WidthType.DXA },
              borders: {
                top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
                bottom: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
                right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
                left: { style: BorderStyle.SINGLE, size: 24, color: C.royal, space: 1 },
              },
              margins: { top: 200, bottom: 200, left: 280, right: 280 },
              shading: { fill: C.royalSoft, type: ShadingType.CLEAR, color: "auto" },
              children: [
                p("SYSTÈME TYPOGRAPHIQUE", {
                  font: FONT_BODY,
                  size: 16,
                  color: C.royal,
                  bold: true,
                  spaceAfter: 100,
                }),
                p([
                  tr("Display ", { size: 20, color: C.ink, bold: true }),
                  tr("— Fraunces (serif éditorial). Titres et chiffres hero.", { size: 20, color: C.inkSoft }),
                ], { spaceAfter: 40 }),
                p([
                  tr("Body ", { size: 20, color: C.ink, bold: true }),
                  tr("— Inter (grotesque institutionnelle). Texte courant.", { size: 20, color: C.inkSoft }),
                ], { spaceAfter: 40 }),
                p([
                  tr("Mono ", { size: 20, color: C.ink, bold: true }),
                  tr("— JetBrains Mono. Tabular figures, hex, identifiants.", { size: 20, color: C.inkSoft }),
                ], { spaceAfter: 0 }),
              ],
            }),
          ],
        }),
      ],
    }),
    emptyP(360),

    h2("Aperçu typographique"),
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [1800, 6704],
      layout: TableLayoutType.FIXED,
      borders: NO_BORDER_ALL,
      rows: [
        fontShowcase("DISPLAY", "Fraunces", "Compétences IA — Mai 2026", FONT_DISPLAY, 56),
        fontShowcase("BODY", "Inter", "L'observatoire mesure l'évolution.", FONT_BODY, 28),
        fontShowcase("MONO", "JetBrains Mono", "F1 = 0.84   ·   MAPE 11.8 %", FONT_MONO, 24),
      ],
    }),
    emptyP(360),

    h2("Hiérarchie"),
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [1700, 2200, 1500, 1300, 1804],
      layout: TableLayoutType.FIXED,
      borders: NO_BORDER_ALL,
      rows: [
        headerRow(["STYLE", "FONT", "TAILLE", "POIDS", "USAGE"]),
        hierarchyRow("Display", "Fraunces", "64 / 1.2", "Light", "KPI hero, couverture rapport."),
        hierarchyRow("Heading 1", "Fraunces", "40 / 1.3", "Regular", "Titre de section."),
        hierarchyRow("Heading 2", "Fraunces", "28 / 1.3", "Regular", "Sous-section, card dashboard."),
        hierarchyRow("Heading 3", "Inter", "20 / 1.4", "Semibold", "Titre de bloc, label de groupe."),
        hierarchyRow("Body", "Inter", "14 / 1.6", "Regular", "Paragraphe, tooltip, table."),
        hierarchyRow("Caption", "Inter", "12 / 1.5", "Regular", "Légendes, footers, disclaimers."),
        hierarchyRow("Eyebrow", "Inter", "11 / 1.4", "Bold UPPER", "Étiquette de section."),
        hierarchyRow("Mono", "JetBrains", "13 / 1.5", "Regular", "Tabular figures, hex, ids."),
      ],
    }),

    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 06 Iconographie + Espacements --------------------------------------------
function sectionIconsSpacing() {
  const spaceRow = (token, val, usage) =>
    new TableRow({
      cantSplit: true,
      height: { value: 420, rule: HeightRule.ATLEAST },
      children: [
        new TableCell({
          width: { size: 1800, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 100, bottom: 100, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(token, { font: FONT_MONO, size: 19, color: C.royal, bold: true, spaceAfter: 0 }),
          ],
        }),
        new TableCell({
          width: { size: 1800, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 100, bottom: 100, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(val, { font: FONT_BODY, size: 19, color: C.ink, spaceAfter: 0 }),
          ],
        }),
        new TableCell({
          width: { size: 4904, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 100, bottom: 100, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(usage, { font: FONT_BODY, size: 19, color: C.inkSoft, spaceAfter: 0 }),
          ],
        }),
      ],
    });

  return [
    ...sectionTitle("06", "Iconographie & espacements"),

    h2("Iconographie"),
    p(
      "Bibliothèque exclusive : Lucide Icons. Style outline uniquement. Stroke 1.5 px. Couleur héritée du parent. Pas de glyphes pleins, pas d'icônes colorées, pas d'emoji dans l'interface.",
      { spaceAfter: 240 },
    ),
    p([
      tr("Tailles standards   ", { font: FONT_BODY, size: 16, color: C.muted, bold: true }),
      tr("XS 14   ·   S 16   ·   M 20   ·   L 24   ·   XL 32   ", { font: FONT_MONO, size: 20, color: C.navy }),
      tr("px", { font: FONT_MONO, size: 16, color: C.muted }),
    ], { spaceAfter: 280 }),

    p([
      tr("Icônes clés du projet", { font: FONT_BODY, size: 16, color: C.muted, bold: true }),
    ], { spaceAfter: 100 }),
    p([
      tr("Cpu · Brain", { font: FONT_BODY, size: 19, bold: true, color: C.navy }),
      tr("  famille IA   ", { color: C.muted, size: 19 }),
      tr("Sparkles", { font: FONT_BODY, size: 19, bold: true, color: C.navy }),
      tr("  émergence", { color: C.muted, size: 19 }),
    ], { spaceAfter: 60 }),
    p([
      tr("Network · GitGraph", { font: FONT_BODY, size: 19, bold: true, color: C.navy }),
      tr("  graphe Neo4j   ", { color: C.muted, size: 19 }),
      tr("Users", { font: FONT_BODY, size: 19, bold: true, color: C.navy }),
      tr("  communauté Louvain", { color: C.muted, size: 19 }),
    ], { spaceAfter: 60 }),
    p([
      tr("LineChart", { font: FONT_BODY, size: 19, bold: true, color: C.navy }),
      tr("  forecasting   ", { color: C.muted, size: 19 }),
      tr("Highlighter · Tag", { font: FONT_BODY, size: 19, bold: true, color: C.navy }),
      tr("  NER   ", { color: C.muted, size: 19 }),
      tr("Award · Crown", { font: FONT_BODY, size: 19, bold: true, color: C.navy }),
      tr("  PageRank", { color: C.muted, size: 19 }),
    ], { spaceAfter: 360 }),

    h2("Espacements — base 4"),
    p(
      "Chaque token est un multiple de 4 px. Cette règle garantit un rythme vertical cohérent entre dashboard, rapports PDF et templates PPTX.",
      { spaceAfter: 240 },
    ),
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [1800, 1800, 4904],
      layout: TableLayoutType.FIXED,
      borders: NO_BORDER_ALL,
      rows: [
        spaceRow("space-1", "4 px", "Espace inline minimal — icône / label."),
        spaceRow("space-2", "8 px", "Padding interne badge, gap entre boutons."),
        spaceRow("space-3", "12 px", "Padding ligne de table, gap liste filtres."),
        spaceRow("space-4", "16 px", "Padding standard input et button."),
        spaceRow("space-5", "24 px", "Padding interne card."),
        spaceRow("space-6", "32 px", "Marge entre sections d'une page."),
        spaceRow("space-7", "48 px", "Espace au-dessus d'un H2."),
        spaceRow("space-8", "64 px", "Marge entre blocs majeurs."),
      ],
    }),

    new Paragraph({ children: [new PageBreak()] }),
  ];
}

// --- 07 Composants UI ----------------------------------------------------------
function sectionComponents() {
  const compRow = (name, role) =>
    new TableRow({
      cantSplit: true,
      height: { value: 420, rule: HeightRule.ATLEAST },
      children: [
        new TableCell({
          width: { size: 2800, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 100, bottom: 100, left: 0, right: 100 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(name, { font: FONT_MONO, size: 18, color: C.royal, bold: true, spaceAfter: 0 }),
          ],
        }),
        new TableCell({
          width: { size: 5704, type: WidthType.DXA },
          borders: {
            top: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border },
            left: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
            right: { style: BorderStyle.NONE, size: 0, color: "FFFFFF" },
          },
          margins: { top: 100, bottom: 100, left: 0, right: 0 },
          verticalAlign: VerticalAlign.CENTER,
          children: [
            p(role, { font: FONT_BODY, size: 19, color: C.inkSoft, spaceAfter: 0 }),
          ],
        }),
      ],
    });

  return [
    ...sectionTitle("07", "Composants UI"),
    p(
      "Composants construits sur Shadcn UI avec les tokens SKILLNAV. Border-radius 6 px, hauteurs alignées 40 px, padding card 24 px (space-5). Aucune ombre — bordure colorée pour les hover states.",
      { spaceAfter: 360 },
    ),

    h2("Bibliothèque essentielle"),
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [2800, 5704],
      layout: TableLayoutType.FIXED,
      borders: NO_BORDER_ALL,
      rows: [
        compRow("<KPICard>", "KPI hero — chiffre Display 64, delta sémantique, sparkline 12 mois."),
        compRow("<SkillBadge>", "Badge skill — 10 variantes couleurs familles IA, pill radius."),
        compRow("<EmergingScore>", "Barre score émergence — seuils 0.7 / 0.85, sémantique vert / ambre / rouge."),
        compRow("<ConfidenceBadge>", "Score 0-1 Pydantic AI / Transformers, échelle Royal Soft → Error."),
        compRow("<NERHighlight>", "Texte annoté — spans entités colorées par type (SKILL, MODEL, FRAMEWORK…)."),
        compRow("<SkillGraph>", "Graphe force-directed Neo4j — taille = PageRank, halo = communauté."),
        compRow("<TimeSeriesChart>", "Ligne historique solide, forecast dashed, bande confiance 95 %."),
        compRow("<ForecastComparisonChart>", "ARIMA + Prophet + LSTM superposés, MAPE en légende mono."),
        compRow("<ComparativeTable>", "Tableau étude comparative — protocole, métriques chiffrées, choix."),
      ],
    }),
    emptyP(360),

    h2("Exemple — card compétence IA"),
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [8504],
      borders: NO_BORDER_ALL,
      rows: [
        new TableRow({
          cantSplit: true,
          children: [
            new TableCell({
              width: { size: 8504, type: WidthType.DXA },
              borders: NO_BORDER_ALL,
              margins: { top: 320, bottom: 320, left: 360, right: 360 },
              shading: { fill: C.navy, type: ShadingType.CLEAR, color: "auto" },
              children: [
                p("DEEP LEARNING  ·  MAROC  ·  MAI 2026", {
                  font: FONT_BODY,
                  size: 16,
                  color: C.royalLight,
                  bold: true,
                  spaceAfter: 120,
                }),
                p("Transformers (BERT, GPT, LLaMA)", {
                  font: FONT_DISPLAY,
                  size: 36,
                  color: C.bone,
                  bold: true,
                  spaceAfter: 80,
                }),
                p("187 offres analysées sur la période", {
                  font: FONT_BODY,
                  size: 20,
                  color: "8FA3B8",
                  spaceAfter: 240,
                }),
                p([
                  tr("Score émergence — fine-tuning LLM", { font: FONT_BODY, size: 18, color: "8FA3B8" }),
                  tr("\t", {}),
                  tr("0.87", { font: FONT_MONO, size: 22, color: C.royalLight, bold: true }),
                ], {
                  spaceAfter: 60,
                }),
                p([
                  tr("Croissance demande 3 mois", { font: FONT_BODY, size: 18, color: "8FA3B8" }),
                  tr("\t", {}),
                  tr("+24 %", { font: FONT_MONO, size: 22, color: C.success, bold: true }),
                ], { spaceAfter: 60 }),
                p([
                  tr("Couverture cursus ingénieur IA Maroc", { font: FONT_BODY, size: 18, color: "8FA3B8" }),
                  tr("\t", {}),
                  tr("2 / 15", { font: FONT_MONO, size: 22, color: C.warning, bold: true }),
                ], { spaceAfter: 0 }),
              ],
            }),
          ],
        }),
      ],
    }),
  ];
}

// --- 08 Variables CSS ---------------------------------------------------------
function sectionCSSTokens() {
  const cssBlock = `:root {
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

  /* Surfaces et neutres */
  --skn-white:  #FFFFFF;
  --skn-cream:  #FAF8F3;
  --skn-bone:   #F5F1EB;
  --skn-border: #E5E7EB;
  --skn-ink:    #1A1A1A;
  --skn-muted:  #6B7280;

  /* Sémantiques */
  --skn-success: #0F8F65;
  --skn-warning: #C77700;
  --skn-error:   #B42318;

  /* Familles IA / DS */
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

  /* Typographie */
  --font-display: "Fraunces", Georgia, serif;
  --font-body:    "Inter", -apple-system, "Segoe UI", sans-serif;
  --font-mono:    "JetBrains Mono", Consolas, monospace;

  /* Spacing — base 4 px */
  --space-1: 0.25rem;  --space-5: 1.5rem;
  --space-2: 0.5rem;   --space-6: 2rem;
  --space-3: 0.75rem;  --space-7: 3rem;
  --space-4: 1rem;     --space-8: 4rem;

  /* Radius & layout */
  --radius:        6px;
  --radius-pill:   9999px;
  --sidebar-width: 264px;
  --header-height: 64px;
  --content-max:   1440px;
}`;

  const lines = cssBlock.split("\n");

  return [
    ...sectionTitle("08", "Variables CSS"),
    p(
      "Bloc :root prêt à coller dans un projet Next.js 15 avec Tailwind v4. Mode dark dominant par défaut ; basculement automatique en light via attribut data-theme.",
      { spaceAfter: 360 },
    ),
    new Table({
      width: { size: 8504, type: WidthType.DXA },
      columnWidths: [8504],
      borders: NO_BORDER_ALL,
      rows: [
        new TableRow({
          cantSplit: true,
          children: [
            new TableCell({
              width: { size: 8504, type: WidthType.DXA },
              borders: NO_BORDER_ALL,
              margins: { top: 200, bottom: 200, left: 320, right: 320 },
              shading: { fill: C.navy, type: ShadingType.CLEAR, color: "auto" },
              children: lines.map((line) =>
                new Paragraph({
                  spacing: { before: 0, after: 0, line: 220, lineRule: "auto" },
                  children: [
                    new TextRun({
                      text: line || " ",
                      font: FONT_MONO,
                      size: 13,
                      color: line.trim().startsWith("/*")
                        ? "8FA3B8"
                        : C.bone,
                    }),
                  ],
                }),
              ),
            }),
          ],
        }),
      ],
    }),
    emptyP(360),
    p([
      tr("Référence design officielle  ", { font: FONT_BODY, size: 16, color: C.royal, bold: true }),
      tr("SKILLNAV · Karamo Sylla & Bachirou Konaté · Mai 2026", { font: FONT_BODY, size: 18, color: C.inkSoft }),
    ]),
  ];
}

// --- Header / Footer (à partir de la TOC) -------------------------------------
function buildHeader() {
  return new Header({
    children: [
      new Paragraph({
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        spacing: { before: 0, after: 60 },
        children: [
          new TextRun({
            text: "SKILLNAV",
            font: FONT_BODY,
            size: 16,
            color: C.royal,
            bold: true,
          }),
          new TextRun({ text: "\t" }),
          new TextRun({
            text: "Brand Guidelines",
            font: FONT_BODY,
            size: 16,
            color: C.muted,
          }),
        ],
      }),
      new Paragraph({
        spacing: { before: 0, after: 0 },
        border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: C.border, space: 1 } },
        children: [],
      }),
    ],
  });
}

function buildFooter() {
  return new Footer({
    children: [
      new Paragraph({
        tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
        children: [
          new TextRun({
            text: "skillnav · Mai 2026",
            font: FONT_BODY,
            size: 16,
            color: C.muted,
          }),
          new TextRun({ text: "\t" }),
          new TextRun({
            children: [PageNumber.CURRENT],
            font: FONT_BODY,
            size: 18,
            color: C.navy,
            bold: true,
          }),
        ],
      }),
    ],
  });
}

const EMPTY_HF = {
  headers: { default: new Header({ children: [new Paragraph("")] }) },
  footers: { default: new Footer({ children: [new Paragraph("")] }) },
};

// --- Build ---------------------------------------------------------------------
function buildDoc() {
  return new Document({
    creator: "SKILLNAV — Karamo Sylla & Bachirou Konaté",
    title: "Charte graphique SKILLNAV",
    description: "Direction artistique McKinsey-inspired",
    styles: {
      default: { document: { run: { font: FONT_BODY, size: 22 } } },
      paragraphStyles: [
        {
          id: "Heading1",
          name: "Heading 1",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: { font: FONT_BODY, size: 30, color: C.navy, bold: true },
          paragraph: { spacing: { before: 0, after: 120 }, outlineLevel: 0 },
        },
        {
          id: "Heading2",
          name: "Heading 2",
          basedOn: "Normal",
          next: "Normal",
          quickFormat: true,
          run: { font: FONT_BODY, size: 26, color: C.navy, bold: true },
          paragraph: { spacing: { before: 360, after: 180 }, outlineLevel: 1 },
        },
      ],
    },
    sections: [
      // 1. Couverture full-bleed Navy — pas de header/footer
      {
        properties: {
          page: {
            size: { width: 11906, height: 16838 },
            margin: { top: 300, right: 300, bottom: 300, left: 300 },
          },
        },
        ...EMPTY_HF,
        children: coverPage(),
      },
      // 2. Pages avec header/footer
      {
        properties: {
          page: {
            size: { width: 11906, height: 16838 },
            margin: { top: 1701, right: 1701, bottom: 1701, left: 1701 },
          },
        },
        headers: { default: buildHeader() },
        footers: { default: buildFooter() },
        children: [
          ...tocPage(),
          ...sectionDirection(),
          ...sectionPaletteMain(),
          ...sectionPaletteSecondary(),
          ...sectionFamilies(),
          ...sectionTypography(),
          ...sectionIconsSpacing(),
          ...sectionComponents(),
          ...sectionCSSTokens(),
        ],
      },
    ],
  });
}

async function main() {
  console.log("[skillnav] Building Charte DOCX (premium v2)...");
  const doc = buildDoc();
  const buffer = await Packer.toBuffer(doc);
  mkdirSync(dirname(OUT_DOCX), { recursive: true });
  writeFileSync(OUT_DOCX, buffer);
  console.log("[skillnav] Wrote", OUT_DOCX);
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
