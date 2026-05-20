# Registre des curricula ENSA Maroc - filiere Data / IA / Big Data

> Volet parallele SKILLNAV : gap analysis marche IA Maroc vs formation ENSA.
> Reference rapport L5 chapitre 5.1.
> Index machine-lisible : [registry.yaml](registry.yaml)
> Schema Pydantic associe : `skillnav/schemas/curriculum.py`
> Pipeline d'extraction : `skillnav/pipelines/curriculum_mining/`

## Perimetre

12 ENSA dans le reseau public marocain. **8 ENSA dispensent une filiere Data Science / Big Data / IA** en cycle ingenieur (3 ans, S1 a S5 + Projet de Fin d'Etudes au semestre S6).

**ENSA exclues** (pas de filiere Data/IA dediee cycle ingenieur) : Tanger, Al Hoceima, Kenitra, Marrakech.

Le semestre S6 = PFE (stage / projet final). Il n'est pas modelise dans le schema `Semester` car il ne contient aucun module academique. Le pipeline extrait uniquement les semestres S1 a S5 pour les 8 ecoles.

## Legende statut

| Code | Signification |
|---|---|
| `complete` | Programme integral S1 a S5 extrait, modules et volumes horaires verifies |
| `partial` | Programme partiel (certains semestres manquants ou volumes horaires absents) |
| `placeholder` | Squelette cree avec TODO list, en attente de donnees fiables |
| `pending` | Extraction non encore lancee |

## Statut par ENSA (2026-05-19)

| Ecole | Filiere | Acronyme | URL officielle | Statut |
|---|---|---|---|---|
| ENSA Tetouan | Sciences des Donnees, Big Data et IA | SDBIA | [ensa.ac.ma](http://ensa.ac.ma/) | complete |
| ENSA Safi | Ingenierie des Donnees et IA | IDIA | [ensas.uca.ma](https://ensas.uca.ma/contenu/filieres/info.pdf) | complete |
| ENSA Khouribga | Informatique et Ingenierie des Donnees | IID | [ensak.usms.ac.ma](http://ensak.usms.ac.ma/ensak/wp-content/uploads/2026/04/Depliant-IID-25-26.pdf) | complete |
| ENSA Oujda | Ingenierie Data Sciences et Cloud Computing | IDSCC | [ensao.ump.ma](http://ensao.ump.ma/fr/cycle-ingenieur-ingenierie-data-sciences-et-cloud-computing) | complete |
| ENSA Agadir | Sciences des Donnees, Big Data et IA (Agadir) | SDBDIA | [ensa-agadir.ac.ma](http://www.ensa-agadir.ac.ma/pages/SDBDIA) | complete |
| ENSA Fes | Ingenierie en Science de Donnees et IA | ISDIA | [ensaf.ac.ma](https://ensaf.ac.ma/fil-isdia.php) | complete |
| ENSA Berrechid | Ingenierie des Systemes d'Information et Big Data | ISIBD | [ensab.ac.ma](http://www.ensab.ac.ma/) | placeholder |
| ENSA El Jadida | Ingenierie Informatique et Technologies Emergentes | 2ITE | [ensaj.ucd.ac.ma](http://www.ensaj.ucd.ac.ma/) | placeholder |

**Synthese (2026-05-19)** : 6 ENSA / 8 avec programme detaille exploitable pour le gap analysis quantitatif. ENSA Berrechid et El Jadida conservees dans le registre mais sans donnees curriculaires publiques verifiables. Le notebook 06 fonctionne donc sur n = 6 ENSA.

## Disposition

Chaque ENSA est documentee dans son propre dossier `ensa-<slug>/` :

```
ensa-<slug>/
├── source.yaml      # metadonnees (URL, date fetch, statut)
├── filiere.md       # programme S1 a S5 structure en sections Markdown
└── raw/             # HTML / PDF brut (gitignored sauf .gitkeep)
```

Le fichier `filiere.md` suit un template strict (voir `ensa-tetouan-sdbia/filiere.md`) que le parser `skillnav/pipelines/curriculum_mining/parser.py` consomme.

## Workflow de mise a jour

1. `WebFetch` ou `WebSearch` sur l'URL officielle de la filiere
2. Transcription du programme S1 a S5 dans `ensa-<slug>/filiere.md` (template canonique)
3. Mise a jour du `source.yaml` : `extracted_at`, `status` = `complete` ou `partial`
4. Mise a jour de la ligne correspondante dans ce REGISTRY.md et dans registry.yaml
5. Le pipeline `curriculum_mining` extrait les skills via LLM puis normalise

## RGPD et conformite

Les programmes ENSA sont des documents publics (plaquettes de filieres, sites institutionnels). Aucune donnee personnelle (etudiants, enseignants, recruteurs) n'est collectee. Seules les informations institutionnelles (nom de filiere, modules, volumes horaires) sont stockees.

User-Agent utilise pour les WebFetch : `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)`.

---

**Mai 2026 - Bachirou Konate et Karamo Sylla - M242 ENSA-Tetouan**
