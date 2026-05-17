"""Construction des series temporelles hebdomadaires par competence (PRD §N2.3).

Pipeline :
  load_postings()
    -> filtre postings avec posted_date
    -> selection top N skills par occurrence
    -> bucketing hebdomadaire (lundi de chaque ISO week)
    -> fill 0 sur les semaines manquantes
    -> SkillTimeSeries Pydantic par competence

Couverture reelle des donnees SKILLNAV : 5 mois denses (jan-mai 2026).
Sur 22 semaines on garde des series de longueur suffisante pour ARIMA et
Prophet (Train 18 sem / Test 4 sem) et exploitable pour LSTM avec un petit
modele (1 seule couche, hidden_size faible).
"""

from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta
from typing import Any

from skillnav.analysis.loaders import load_postings
from skillnav.schemas.graph import SkillFamily
from skillnav.schemas.timeseries import DataPoint, SkillTimeSeries

# ── Constantes ───────────────────────────────────────────────────────────────

# Date minimale pour considerer un posting comme datable (les donnees
# anterieures a 2026 sont trop eparses pour le forecasting).
_MIN_DATE = date(2026, 1, 1)


# ── Helpers ──────────────────────────────────────────────────────────────────


def _parse_date(raw: Any) -> date | None:
    """Parse une date au format YYYY-MM-DD ; retourne None si invalide."""
    if not raw:
        return None
    try:
        return datetime.fromisoformat(str(raw)[:10]).date()
    except (ValueError, TypeError):
        return None


def _week_start(d: date) -> date:
    """Renvoie le lundi de la semaine ISO contenant `d`."""
    return d - timedelta(days=d.weekday())


def _extract_skills(posting: dict[str, Any]) -> list[str]:
    """Extrait les skills d'un posting (required + optional), dedupliques."""
    required: list[Any] = posting.get("skills_required") or []
    optional: list[Any] = posting.get("skills_optional") or []
    seen: set[str] = set()
    result: list[str] = []
    for raw in list(required) + list(optional):
        if isinstance(raw, str):
            name = raw.strip()
            key = name.lower()
            if name and key not in seen:
                seen.add(key)
                result.append(name)
    return result


def _all_weeks(start: date, end: date) -> list[date]:
    """Toutes les semaines (lundis) entre start (inclus) et end (inclus)."""
    weeks: list[date] = []
    current = _week_start(start)
    end_monday = _week_start(end)
    while current <= end_monday:
        weeks.append(current)
        current += timedelta(weeks=1)
    return weeks


# ── Fonction principale ──────────────────────────────────────────────────────


def build_time_series(
    top_n: int = 10,
    min_date: date = _MIN_DATE,
    sources: list[str] | None = None,
    truncate_last_weeks: int = 3,
) -> list[SkillTimeSeries]:
    """Construit `top_n` series temporelles hebdomadaires depuis les postings.

    Args:
        top_n: nombre de skills a etudier (top par occurrence dans la fenetre).
        min_date: date min pour considerer un posting (defaut : 2026-01-01).
        sources: filtre sur les sources de postings (None = toutes).
        truncate_last_weeks: nombre de semaines a retirer en fin de serie pour
            corriger l'artefact de collecte. Le scraping ayant eu lieu autour
            du 14-16 mai 2026, les 3 dernieres semaines (du 27 avril au 17 mai)
            sont partiellement incompletes et doivent etre exclues du
            forecasting pour eviter des metriques biaisees (defaut : 3).

    Returns:
        Liste de `top_n` SkillTimeSeries Pydantic, ordonnees par occurrence
        decroissante. Chaque serie couvre toutes les semaines entre la
        premiere et (derniere - truncate_last_weeks) date observee, avec un
        count=0 pour les semaines sans occurrence.
    """
    postings = load_postings(sources)

    # 1. Filtrer les postings datables et dans la fenetre
    dated: list[tuple[date, list[str]]] = []
    for posting in postings:
        d = _parse_date(posting.get("posted_date"))
        if d is None or d < min_date:
            continue
        skills = _extract_skills(posting)
        dated.append((d, skills))

    if not dated:
        return []

    # 2. Calcul des semaines (lundis) + troncature des semaines finales
    #    (artefact de collecte : scraping mi-mai 2026 = 3 dernieres semaines partielles)
    all_dates = [d for d, _ in dated]
    weeks = _all_weeks(min(all_dates), max(all_dates))
    if truncate_last_weeks > 0:
        weeks = weeks[:-truncate_last_weeks] if truncate_last_weeks < len(weeks) else []
        if weeks:
            cutoff = weeks[-1] + timedelta(weeks=1)  # debut de la 1re semaine exclue
            dated = [(d, s) for d, s in dated if d < cutoff]

    if not dated or not weeks:
        return []

    # 3. Compter les occurrences globales SUR LA FENETRE TRONQUEE (pour top-N)
    global_count: Counter[str] = Counter()
    canonical: dict[str, str] = {}  # lower -> nom canonique
    for _, skills in dated:
        for s in skills:
            key = s.lower()
            if key not in canonical:
                canonical[key] = s
            global_count[key] += 1

    top_keys: list[str] = [k for k, _ in global_count.most_common(top_n)]

    # 4. Compter par (skill_key, semaine)
    counts: dict[str, Counter[date]] = {k: Counter() for k in top_keys}
    for d, skills in dated:
        wk = _week_start(d)
        for s in skills:
            key = s.lower()
            if key in counts:
                counts[key][wk] += 1

    # 5. Construire les SkillTimeSeries Pydantic (fill 0 sur les trous)
    series_list: list[SkillTimeSeries] = []
    for key in top_keys:
        skill_canonical = canonical[key]
        data_points = [
            DataPoint(period=wk.isoformat(), count=counts[key].get(wk, 0))
            for wk in weeks
        ]
        series_list.append(
            SkillTimeSeries(
                skill_name=skill_canonical,
                family=_infer_family_safe(skill_canonical),
                data_points=data_points,
            )
        )

    return series_list


def _infer_family_safe(skill_name: str) -> str:
    """Importe l'inference de famille du pipeline structure_mining ; en cas
    d'echec retourne la valeur par defaut SkillFamily.OTHER.
    """
    try:
        from skillnav.pipelines.structure_mining.graph_builder import _infer_family

        return _infer_family(skill_name).value
    except (ImportError, AttributeError):
        return SkillFamily.OTHER.value
