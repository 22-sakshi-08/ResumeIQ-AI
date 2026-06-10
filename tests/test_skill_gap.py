import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nlp.skill_gap_analyzer import SkillGapAnalyzer

@pytest.fixture
def analyzer():
    return SkillGapAnalyzer()

def test_full_match(analyzer):
    resume = ["python", "aws", "docker"]
    jd = ["python", "aws", "docker"]
    res = analyzer.analyze(resume, jd)
    
    assert res["matched"] == ["aws", "docker", "python"]
    assert res["missing"] == []
    assert res["match_percentage"] == 100.0

def test_partial_match(analyzer):
    resume = ["python", "docker", "fastapi"]
    jd = ["python", "aws", "docker", "kubernetes"]
    res = analyzer.analyze(resume, jd)
    
    assert res["matched"] == ["docker", "python"]
    assert res["missing"] == ["aws", "kubernetes"]
    assert res["extra"] == ["fastapi"]
    assert res["match_percentage"] == 50.0

def test_no_match(analyzer):
    resume = ["react", "angular", "css"]
    jd = ["python", "pytorch", "aws"]
    res = analyzer.analyze(resume, jd)
    
    assert res["matched"] == []
    assert res["missing"] == ["aws", "python", "pytorch"]
    assert res["match_percentage"] == 0.0

def test_empty_jd(analyzer):
    resume = ["python", "aws"]
    jd = []
    res = analyzer.analyze(resume, jd)
    
    assert res["matched"] == []
    assert res["missing"] == []
    assert res["match_percentage"] == 100.0
