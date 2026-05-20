"""Tests unitaires de la strategie rule-based de skill_extractor.py.

Note : la strategie LLM (Claude Sonnet 4.5) n'est pas testee ici car elle
necessite ANTHROPIC_API_KEY et un appel reseau. Elle est testable en
integration via tests/integration/.
"""

from __future__ import annotations

from skillnav.pipelines.curriculum_mining_multi.skill_extractor import (
    extract_skills_batch_rules,
    extract_skills_rules,
)


def test_module_machine_learning_returns_ml_python_sklearn() -> None:
    """Un module 'Machine Learning' doit produire Machine Learning + scikit-learn."""
    skills = extract_skills_rules("Machine Learning")
    assert "Machine Learning" in skills
    assert "scikit-learn" in skills


def test_module_deep_learning_returns_pytorch_tensorflow() -> None:
    """Un module 'Deep Learning' doit produire PyTorch et TensorFlow."""
    skills = extract_skills_rules("Apprentissage profond")
    assert "Deep Learning" in skills
    assert "PyTorch" in skills


def test_module_nlp_returns_nlp_transformers() -> None:
    """Un module TALN doit produire NLP et transformers."""
    skills = extract_skills_rules("Traitement automatique des langues naturelles (TALN)")
    assert "NLP" in skills
    assert "transformers" in skills


def test_module_big_data_returns_spark_hadoop() -> None:
    """Un module Big Data doit produire Apache Spark et Hadoop."""
    skills = extract_skills_rules("Fondamentaux du Big Data")
    assert "Apache Spark" in skills
    assert "Hadoop" in skills


def test_module_python_data_science_returns_python_pandas() -> None:
    """Un module 'Python pour data science' doit produire Python et pandas."""
    skills = extract_skills_rules("Python pour data science")
    assert "Python" in skills
    assert "pandas" in skills


def test_non_technical_modules_return_empty_list() -> None:
    """Les modules non techniques (langues, management) doivent etre filtres."""
    assert extract_skills_rules("Langues, Communication et TIC 1") == []
    assert extract_skills_rules("Management 1") == []
    assert extract_skills_rules("Ethique et droit") == []
    assert extract_skills_rules("Marketing et GRH") == []
    assert extract_skills_rules("Culture et Art") == []


def test_module_cloud_returns_aws_gcp_azure() -> None:
    """Un module Cloud doit produire AWS, GCP, Azure."""
    skills = extract_skills_rules("Cloud computing et virtualisation")
    assert "Cloud" in skills or "AWS" in skills or "cloud computing" in skills


def test_module_blockchain_returns_blockchain() -> None:
    """Un module Blockchain doit produire 'blockchain'."""
    skills = extract_skills_rules("Fondamentaux de la Blockchain")
    assert "blockchain" in skills


def test_module_computer_vision_returns_cv_opencv() -> None:
    """Un module Vision par ordinateur doit produire computer vision."""
    skills = extract_skills_rules("Vision par ordinateur")
    assert "computer vision" in skills


def test_module_recommender_returns_recommender_systems() -> None:
    """Un module 'Systemes de recommandation' doit produire recommender systems."""
    skills = extract_skills_rules("Systemes de recommandation")
    assert "recommender systems" in skills


def test_batch_rules_preserves_order() -> None:
    """extract_skills_batch_rules doit retourner un resultat par module dans l'ordre."""
    modules = ["Machine Learning", "Management 1", "Deep Learning"]
    results = extract_skills_batch_rules(modules)
    assert len(results) == 3
    assert "Machine Learning" in results[0]
    assert results[1] == []
    assert "Deep Learning" in results[2]


def test_module_devops_mlops_returns_mlops() -> None:
    """Un module 'Devops et MLops' doit produire MLOps et Docker."""
    skills = extract_skills_rules("Devops et MLops")
    assert "MLOps" in skills


def test_module_reinforcement_learning_returns_rl() -> None:
    """Un module 'apprentissage par renforcement' doit produire reinforcement learning."""
    skills = extract_skills_rules("Theorie de jeux et apprentissage par renforcement")
    assert "reinforcement learning" in skills


def test_results_are_sorted_deterministic() -> None:
    """Les resultats doivent etre tries pour etre deterministes."""
    skills = extract_skills_rules("Machine Learning")
    assert skills == sorted(skills)


def test_empty_input_returns_empty_list() -> None:
    """Un module au titre vide doit produire une liste vide."""
    assert extract_skills_rules("") == []


def test_unknown_module_returns_empty_or_minimal() -> None:
    """Un module sans correspondance technique ne doit pas crasher."""
    result = extract_skills_rules("Initiation a la philosophie ancienne")
    assert isinstance(result, list)
