import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nlp.skill_extractor import SkillExtractor

@pytest.fixture
def extractor():
    return SkillExtractor()

def test_extract_single_skill(extractor):
    text = "Candidate has python coding skills."
    skills = extractor.extract_skills(text)
    assert skills == ["python"]

def test_extract_multiple_skills(extractor):
    text = "Candidate knows PyTorch, Docker, and AWS."
    skills = extractor.extract_skills(text)
    # Alphabetically sorted
    assert skills == ["aws", "docker", "pytorch"]

def test_extract_duplicate_skills(extractor):
    text = "Knows python, also writes python, and runs python scripts."
    skills = extractor.extract_skills(text)
    # Deduplicated
    assert skills == ["python"]

def test_extract_uppercase_skills(extractor):
    text = "Experienced in KUBERNETES, TENSORFLOW, and DJANGO."
    skills = extractor.extract_skills(text)
    assert skills == ["django", "kubernetes", "tensorflow"]

def test_extract_special_characters(extractor):
    text = "Expert in C++ and C# and .NET."
    skills = extractor.extract_skills(text)
    assert "c++" in skills
    assert "c#" in skills

def test_extract_empty_and_mixed(extractor):
    assert extractor.extract_skills("") == []
    assert extractor.extract_skills("random sentence without skills") == []
