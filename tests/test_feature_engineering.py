import os
import sys
import pytest
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ml.feature_engineering import (
    FeatureExtractor,
    compute_cosine_similarity,
    compute_jaccard_similarity,
    compute_skill_overlap_score,
    compute_keyword_coverage_score
)

def test_feature_extractor_tfidf(tmp_path):
    corpus = [
        "Python developer with machine learning experience",
        "React frontend dev building web apps with Javascript",
        "DevOps engineer managing AWS cloud infrastructure"
    ]
    
    extractor = FeatureExtractor(max_features=10)
    extractor.fit_vectorizer(corpus)
    
    tfidf_matrix = extractor.transform_tfidf(corpus)
    assert tfidf_matrix.shape == (3, 10)
    
    # Save/load check
    save_path = tmp_path / "vectorizer.pkl"
    extractor.save_vectorizer(str(save_path))
    assert os.path.exists(save_path)
    
    new_extractor = FeatureExtractor()
    new_extractor.load_vectorizer(str(save_path))
    new_matrix = new_extractor.transform_tfidf(corpus)
    assert np.allclose(tfidf_matrix.toarray(), new_matrix.toarray())

def test_extract_stats():
    text = """
    Jane Doe. Python and AWS.
    Experience: Led team of engineers to build backend databases.
    Projects: Developed React apps on GitHub.
    Education: Master of Science in Computer Science, MIT University, 2021.
    Certifications: AWS Certified Solutions Architect.
    """
    stats = FeatureExtractor.extract_stats(text)
    
    assert stats["word_count"] > 10
    assert stats["unique_word_count"] > 10
    assert stats["avg_sentence_length"] > 1.0
    assert stats["skill_count"] >= 2 # Python, AWS, React, Git
    assert stats["education_keyword_count"] >= 2 # master, science, university
    assert stats["certification_keyword_count"] >= 2 # certified, aws
    assert stats["project_keyword_count"] >= 2 # developed, projects

def test_similarity_functions():
    # Jaccard
    assert compute_jaccard_similarity("python developer", "python developer") == 1.0
    assert compute_jaccard_similarity("python developer", "react developer") == 0.3333333333333333
    
    # Skill overlap
    candidate = ["Python", "PyTorch", "Docker"]
    required = ["Python", "AWS", "PyTorch", "Kubernetes"]
    # matches: Python, PyTorch (2 out of 4)
    assert compute_skill_overlap_score(candidate, required) == 0.5
    
    # Keyword coverage
    assert compute_keyword_coverage_score("Experienced AWS developer", ["aws", "cloud"]) == 0.5
