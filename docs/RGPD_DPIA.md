# RGPD — DPIA simplifiée SKILLNAV

> Analyse d'impact sur la protection des données — projet académique M242.
> Document de référence pour la conformité RGPD du projet SKILLNAV.

**Responsables du traitement** : Karamo Sylla & Bachirou Konaté (étudiants, ENSA-Tétouan)
**Encadrant académique** : Pr. Imad Sassi
**Cadre** : Module M242 — Analyse de Web · Diplôme d'Ingénieur, filière Sciences des Données, Big Data et Intelligence Artificielle (SDBIA)
**Date** : Mai 2026
**Version** : 1.0

---

## 1. Description du traitement

### 1.1 Finalité

SKILLNAV constitue un **observatoire académique des compétences en Intelligence Artificielle et Data Science** dans le cadre d'un projet de fin de module universitaire. La finalité du traitement est :

- **Recherche académique** : démonstration scientifique des techniques de Web Mining (extraction, structuration, modélisation) sur un corpus d'offres d'emploi publiques
- **Évaluation pédagogique** : production des livrables imposés par le sujet du module M242
- **Communication scientifique** : rapport méthodologique académique + soutenance + éventuel article post-soutenance

### 1.2 Données traitées

#### Données collectées

| Donnée | Type | Source | Finalité |
|---|---|---|---|
| Titre de l'offre | Texte | Sites d'emploi publics | Classification, normalisation |
| Description de l'offre | Texte | Sites d'emploi publics | Extraction NER, classification |
| Nom de l'entreprise | Texte (entité juridique) | Sites d'emploi publics | Statistiques agrégées |
| Localisation (ville, pays) | Texte | Sites d'emploi publics | Analyses géographiques |
| Type de contrat | Texte | Sites d'emploi publics | Statistiques agrégées |
| Niveau de séniorité | Texte | Sites d'emploi publics | Statistiques agrégées |
| Compétences requises | Liste de mots | Sites d'emploi publics | Cœur du projet |
| Date de publication | Date | Sites d'emploi publics | Séries temporelles |
| URL de l'annonce | URL | Sites d'emploi publics | Traçabilité, déduplication |
| HTML brut de la page | Texte | Sites d'emploi publics | Extraction (effacé après 6 mois) |

#### Données **expressément exclues** (ne sont jamais collectées ni stockées)

- Noms, prénoms ou initiales de candidats
- Adresses email de contact RH ou de candidats
- Numéros de téléphone
- Photos ou identifiants visuels
- Données personnelles sensibles (santé, religion, opinions politiques, orientation sexuelle, etc.)
- Données de mineurs
- Adresses postales personnelles

Si l'une de ces données apparaît accidentellement dans un texte d'offre (ex. nom du contact RH dans le pied de l'annonce), le pipeline Pydantic AI est **explicitement instruit de ne pas l'extraire** (règle RE-7 du PRD §10.1) et la quarantaine manuelle vérifie l'absence de leak résiduel.

### 1.3 Catégories de personnes concernées

| Catégorie | Statut | Volumétrie estimée |
|---|---|---|
| Entreprises (entités juridiques) | Données publiques (raison sociale, secteur, ville) | ~ 200–500 entreprises |
| Personnes physiques (candidats, recruteurs) | **Aucune donnée collectée** | 0 |

### 1.4 Volume

- **MVP** : 500–2 000 offres analysées
- **V1.5** : jusqu'à 10 000 offres
- **Période couverte** : 3–6 mois glissants

---

## 2. Base légale

Le traitement repose sur l'**intérêt légitime** au sens de l'**article 6.1.f du RGPD**, justifié par :

| Critère | Analyse |
|---|---|
| Finalité légitime | Recherche académique encadrée institutionnellement (ENSA-Tétouan, Diplôme d'Ingénieur — filière SDBIA Sciences des Données, Big Data et IA) |
| Nécessité du traitement | Démonstration empirique des techniques Web Mining requise par le sujet imposé du module M242 |
| Mise en balance avec les droits des personnes | Aucune donnée personnelle de personnes physiques n'est traitée — seules des données publiques d'entités juridiques (entreprises) le sont |
| Attente raisonnable | Les sites d'emploi publient ces offres précisément pour qu'elles soient lues et analysées publiquement |

L'intérêt légitime est ici **fortement** soutenu car le périmètre du traitement est restreint aux entreprises (personnes morales) sans aucune extraction de données identifiantes individuelles.

---

## 3. Mesures techniques et organisationnelles

### 3.1 Sécurité des données

| Mesure | Implémentation |
|---|---|
| Chiffrement en transit | TLS 1.2+ obligatoire sur toutes les connexions vers MongoDB Atlas, Neo4j AuraDB, Elasticsearch Cloud, APIs Anthropic / Apify / Firecrawl |
| Chiffrement au repos | Géré par les fournisseurs cloud (Mongo Atlas, Neo4j Aura — AES-256) |
| Secrets | Stockés dans `.env` non versionné ; CI : variables protégées GitHub Actions |
| Accès | Limité aux deux membres du binôme + Pr. Sassi (sur demande) |
| Logs d'accès | Activés sur MongoDB Atlas et Neo4j AuraDB (logs natifs des fournisseurs) |
| Audit | Journal `data/audit/optout_log.jsonl` pour les demandes d'opposition |

### 3.2 Limitation et minimisation

| Principe RGPD | Application SKILLNAV |
|---|---|
| Minimisation | Seules les données strictement nécessaires aux 3 axes Web Mining sont collectées |
| Limitation à la finalité | Aucun usage commercial, aucun partage avec des tiers, aucune réutilisation hors module académique |
| Exactitude | Pipeline d'extraction validé par confidence Pydantic AI ≥ 0.75 ; quarantaine manuelle des cas litigieux |
| Conservation limitée | `raw_html` ≤ 6 mois ; `extracted_jobs` ≤ 24 mois ; logs ≤ 3 mois ; après ces durées, suppression automatique scriptée |

### 3.3 Anonymisation des datasets publiés

Lors de tout export public (datasets ouverts publiés sur GitHub) :

| Champ | Transformation |
|---|---|
| `company` si l'entreprise apparaît dans < 10 offres / mois | Remplacé par hash SHA-256 tronqué à 8 caractères |
| `url` | Domaine conservé, chemin tronqué (`https://www.rekrute.com/.../`) |
| `raw_html` | **Exclu** des exports publics |
| `raw_text` | Tronqué à 500 caractères + ellipsis |
| `city` | Conservé seulement si > 10 offres ; sinon `<masked>` |

Cette stratégie évite tout profilage indirect d'une petite entreprise par recoupement.

---

## 4. Sous-traitants

Le projet repose sur plusieurs services tiers. Tous sont conformes au RGPD ou opèrent sous DPA disponible.

| Sous-traitant | Service | Localisation des données | DPA / Conformité |
|---|---|---|---|
| **Anthropic** | API Claude (extraction structurée) | US (avec EU available) | DPA disponible publiquement |
| **HuggingFace** | Téléchargement de modèles open source | Inférence **locale** (pas d'envoi de données) | RGPD-friendly (modèles, pas de données envoyées) |
| **MongoDB Inc.** | MongoDB Atlas (Free M0) | EU possible (Frankfurt) | DPA Atlas |
| **Neo4j** | AuraDB (Free) | EU possible | DPA Aura |
| **Elastic NV** | Elasticsearch Cloud (Free 14j) | EU possible | DPA Elastic |
| **Apify** | LinkedIn scraping | EU | DPA disponible |
| **Mendable (Firecrawl)** | Scraping pages JS | US | DPA disponible |
| **Vercel** | Hébergement frontend | EU possible | DPA Vercel |
| **GitHub (Microsoft)** | Repository code + CI | EU possible | DPA GitHub |
| **Render** | Hébergement API FastAPI | EU possible | DPA Render |

Configuration recommandée : choisir les régions EU (Frankfurt, Ireland) à chaque création de cluster / projet.

---

## 5. Robots.txt et conformité éthique

### 5.1 Protocole strict

```python
import urllib.robotparser

def check_robots(url: str) -> bool:
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(f"{base_url(url)}/robots.txt")
    rp.read()
    return rp.can_fetch("SkillnavBot/1.0", url)
```

**Règles strictes** :

- Si `Disallow: /` sur le chemin cible → la source est **désactivée** dans `sources/registry.yaml` ; aucune collecte n'est effectuée
- Si `Crawl-delay: N` est spécifié → le rate limit est **toujours respecté** (N ou plus)
- Le User-Agent identifie clairement l'origine académique : `SkillnavBot/1.0 (Academic; M242 ENSA-Tetouan)`
- À chaque session de scraping, un log est produit : URL `robots.txt`, date de lecture, décision (allow / deny par chemin)

### 5.2 Rate limiting par défaut

| Source | Rate limit appliqué |
|---|---|
| Sources statiques (Rekrute, EmploiTIC, Indeed, builtin.com) | 5 secondes / requête |
| LinkedIn (via Apify) | Quota natif Apify (~ 200 / heure / acteur) |
| Google Trends (pytrends) | 1 requête / 60 secondes (politique pytrends) |
| GitHub Trending | 5 secondes / requête |

### 5.3 Revue des conditions d'utilisation (TOS)

Chaque source est inscrite dans `sources/registry.yaml` avec un champ `tos_reviewed_at` daté et un nom de revieweur. Toute source dont les TOS interdisent explicitement le scraping académique est exclue.

---

## 6. Droits des personnes concernées

Bien qu'aucune donnée personnelle individuelle ne soit collectée, des **entreprises** (personnes morales) peuvent se trouver représentées dans les datasets. Pour respecter l'esprit du RGPD :

### 6.1 Droit d'opposition

- **Email dédié** : `optout@skillnav.example` (alias technique vers email Karamo)
- **Procédure** :
  1. Réception d'une demande mentionnant un domaine entreprise ou une URL d'offre
  2. Vérification de la légitimité (entité juridique reconnaissable)
  3. Suppression de l'enregistrement dans MongoDB (cascade vers Neo4j et Elasticsearch)
  4. Réponse écrite au demandeur **sous 30 jours**
  5. Log de la suppression dans `data/audit/optout_log.jsonl`

### 6.2 Droit à l'information

Une page **`/methodology`** publique sur le dashboard SKILLNAV documente :

- La finalité du traitement
- Les sources utilisées
- La base légale (art. 6.1.f)
- Le contact opposition
- Les durées de conservation

### 6.3 Droit d'accès et de rectification

Sur demande motivée à `optout@skillnav.example`, les enregistrements concernant une entreprise peuvent être communiqués (extrait MongoDB JSON) ou rectifiés (correction puis re-extraction).

---

## 7. Évaluation des risques

| Risque | Niveau | Probabilité | Mitigation |
|---|:---:|:---:|---|
| Une offre contient un nom de candidat dans le texte libre | Bas | Faible | RE-7 (PRD §10.1) : prompt Pydantic AI excluant explicitement les noms ; quarantaine manuelle |
| Profilage indirect d'une petite entreprise (< 5 offres) | Moyen | Modérée | Hashage sous seuil dans tous les exports publics |
| Récupération automatisée du dataset par un tiers à des fins commerciales | Faible | Faible | Datasets publiés sous **licence académique non commerciale**, mention dans README |
| Fuite de credentials API (Anthropic, MongoDB) | Élevé | Faible | `.env` non versionné, secret scanning GitHub activé, rotation possible |
| Infraction TOS d'une source tierce | Moyen | Faible | Revue TOS systématique avant ajout d'une source ; respect strict de robots.txt |
| Perte de données dans MongoDB Atlas | Faible | Très faible | Backup mensuel manuel + freezing du dataset MVP avant la soutenance |

---

## 8. Conclusion DPIA

Le traitement SKILLNAV est **compatible avec le RGPD** sous réserve de :

1. Respect strict du périmètre des données collectées (entreprises uniquement, jamais d'individus)
2. Mise en œuvre effective des durées de conservation (jobs de purge à scripter Sprint 2)
3. Maintien à jour du registre des sources (`sources/registry.yaml`) avec TOS reviewed
4. Disponibilité du contact opposition tout au long de la vie du projet
5. Anonymisation systématique des datasets publiés

Aucune transmission de données personnelles d'individus n'est effectuée vers des sous-traitants. Les données traitées concernent exclusivement des entités juridiques (entreprises) sur la base de leurs publications publiques (offres d'emploi).

**Validation** : Karamo Sylla & Bachirou Konaté — Mai 2026 — pour soumission au Pr. Imad Sassi dans le cadre du module M242.

---

## 9. Annexe — Modèle de réponse à une demande d'opposition

```
Objet : SKILLNAV — Demande d'opposition reçue [REF-XXXX]

Madame, Monsieur,

Nous accusons réception de votre demande d'opposition au traitement
des données concernant [entité ou URL].

Suite à vérification, nous confirmons la suppression effective de ces
données de notre base au [DATE]. Cette suppression couvre :
   - La base MongoDB Atlas (collection extracted_jobs)
   - L'index Elasticsearch jobs_search
   - Le graphe Neo4j (nœuds et arêtes associés)

Le dataset public publié sur GitHub a également été régénéré sans
ces données.

Nous restons à votre disposition pour toute question.

Cordialement,
Karamo Sylla & Bachirou Konaté
SKILLNAV — Projet académique M242, ENSA-Tétouan
```

---

**Référence** : voir aussi `docs/PRD.md` §N4 pour la version intégrée du protocole RGPD.
