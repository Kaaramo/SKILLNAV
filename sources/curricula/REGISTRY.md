# Registre des curricula ENSA — volet gap analysis SKILLNAV

Le réseau ENSA marocain (Écoles Nationales des Sciences Appliquées) compte 12 écoles publiques.
**8 d'entre elles** proposent une filière Data Science / Big Data / IA en cycle ingénieur (S1-S6).

Le projet SKILLNAV mesure le **désalignement entre les compétences enseignées** par ces filières
et les **compétences demandées** par le marché du travail (corpus de 3 467 offres, MA + INTL,
janvier 2023 → mai 2026).

---

## État de l'extraction par école

| École | Filière | Statut | Notebook gap |
|---|---|---|---|
| **ENSA Tétouan** | SDBIA — Sciences des Données, Big Data & IA | ✅ **extraction-complete** | [`06_gap_analysis_market_vs_curriculum.ipynb`](../../notebooks/06_gap_analysis_market_vs_curriculum.ipynb) |
| ENSA Berrechid | ISIBD — Ingénierie des Systèmes d'Information & Big Data | ⏳ placeholder | — |
| ENSA Safi | IDIA — Ingénierie de la Donnée & Intelligence Artificielle | ⏳ placeholder | — |
| ENSA Khouribga | IID — Ingénierie Informatique et de la Donnée | ⏳ placeholder | — |
| ENSA Oujda | IDSCC — Ingénierie de la Donnée, Sécurité, Cloud & Cybersécurité | ⏳ placeholder | — |
| ENSA Agadir | SDBIA | ⏳ placeholder | — |
| ENSA Fès | ILIA — Ingénierie Logicielle & Intelligence Artificielle | ⏳ placeholder | — |
| ENSA El Jadida | 2ITE — Ingénierie Informatique, Télécoms & Embarqué | ⏳ placeholder | — |

---

## ENSA Tétouan — SDBIA (extraction-complete)

- **Source primaire** : [`docs/Big data et IA de ENSATE.pdf`](../../docs/Big%20data%20et%20IA%20de%20ENSATE.pdf) (5 pages, dernière modif. 2024-02-01)
- **Métadonnées** : [`ensa-tetouan/source.yaml`](ensa-tetouan/source.yaml)
- **Contenu structuré** : [`ensa-tetouan/filiere.md`](ensa-tetouan/filiere.md)
- **Extraction brute** : [`ensa-tetouan/_raw/extraction_brute.txt`](ensa-tetouan/_raw/extraction_brute.txt)
- **Pipeline** : `skillnav/pipelines/curriculum_mining/parser.py`
- **Schemas Pydantic** : `skillnav/schemas/curriculum.py`
- **Notebook gap analysis** : `notebooks/06_gap_analysis_market_vs_curriculum.ipynb`

### Synthèse chiffrée (snapshot 2026-05-18)

| Indicateur | Valeur |
|---|---:|
| Semestres de cours | 5 (S1-S5) |
| Modules total | 31 |
| Volume horaire total | 3 185 h |
| Skills enseignées canonicalisées | 126 |
| Couverture skills marché MA | **27,4 %** (69/252) |
| Couverture offres marché MA | **40,0 %** (pondéré) |
| Couverture skills marché INTL | 6,7 % (canonicalisation INTL imparfaite) |
| Couverture offres marché INTL | 17,3 % (pondéré) |

### Top 5 gaps marché MA (compétences demandées non enseignées)

| Skill | Offres MA | Famille |
|---|---:|---|
| Power BI | 105 | Data Viz / BI |
| GCP | 85 | Cloud |
| Statistics | 81 | Maths |
| Azure | 80 | Cloud |
| R | 69 | Programming |

---

## Comment ajouter une nouvelle école

1. Créer `sources/curricula/<ecole-slug>/source.yaml` (cf. `ensa-tetouan/source.yaml` comme modèle)
2. Créer `sources/curricula/<ecole-slug>/filiere.md` (cf. modèle ENSAT)
3. Lancer `python scripts/build_gap_analysis.py` (adapter le script ou créer une version générique)
4. Mettre à jour ce REGISTRY.md (passer le statut à `extraction-complete`)

Le pipeline `skillnav/pipelines/curriculum_mining/parser.py` est générique et accepte n'importe
quel `filiere.md` respectant le format documenté.
