import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nlp.recommendation_engine import RecommendationEngine

@pytest.fixture
def engine():
    return RecommendationEngine()

def test_one_missing_skill(engine):
    gap = {"missing": ["aws"]}
    recs = engine.generate_recommendations(gap)
    
    assert len(recs) == 1
    assert "aws" in recs[0].lower() or "cloud" in recs[0].lower()

def test_multiple_missing_skills(engine):
    gap = {"missing": ["aws", "docker", "kubernetes"]}
    recs = engine.generate_recommendations(gap)
    
    assert len(recs) == 3
    # Check that it pulls recommendations for all three
    assert any("aws" in r.lower() or "cloud" in r.lower() for r in recs)
    assert any("docker" in r.lower() or "containerized" in r.lower() for r in recs)
    assert any("kubernetes" in r.lower() or "orchestration" in r.lower() for r in recs)

def test_no_missing_skills(engine):
    gap = {"missing": []}
    recs = engine.generate_recommendations(gap)
    assert recs == []

def test_unknown_missing_skill(engine):
    gap = {"missing": ["super_obscure_ml_tool_x"]}
    recs = engine.generate_recommendations(gap)
    
    assert len(recs) == 1
    # Fallback template
    assert "super_obscure_ml_tool_x" in recs[0].lower()
