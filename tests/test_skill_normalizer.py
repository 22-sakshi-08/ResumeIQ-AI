import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nlp.skill_normalizer import SkillNormalizer

@pytest.fixture
def normalizer():
    return SkillNormalizer()

def test_normalize_casing(normalizer):
    assert normalizer.normalize("PYTHON") == "python"
    assert normalizer.normalize("PyTorch") == "pytorch"
    assert normalizer.normalize("FastAPI") == "fastapi"

def test_normalize_aliases(normalizer):
    assert normalizer.normalize("py") == "python"
    assert normalizer.normalize("js") == "javascript"
    assert normalizer.normalize("ts") == "typescript"
    assert normalizer.normalize("k8s") == "kubernetes"
    assert normalizer.normalize("sklearn") == "scikit-learn"

def test_normalize_punctuation(normalizer):
    assert normalizer.normalize("machine-learning") == "machine learning"
    assert normalizer.normalize("machine_learning") == "machine learning"
    assert normalizer.normalize("node.js") == "node.js"

def test_normalize_list(normalizer):
    raw_list = ["PyTorch", "sklearn", "JS", "py", "PyTorch"]
    norm_list = normalizer.normalize_list(raw_list)
    # Deduplicated, canonical, sorted order is not required but normalizer_list preserves input order
    assert norm_list == ["pytorch", "scikit-learn", "javascript", "python"]
