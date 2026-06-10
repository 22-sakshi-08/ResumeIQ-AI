import os
import sys
import pytest
import pandas as pd

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ml.preprocessor import TextPreprocessor
from src.ml.dataset_loader import DatasetLoader

@pytest.fixture
def preprocessor():
    return TextPreprocessor()

def test_clean_text(preprocessor):
    text = "Contact: test.user@gmail.com, Web: https://example.com, Phone: +1-555-0199-2342!"
    cleaned = preprocessor.clean_text(text)
    
    # Check that email is removed
    assert "test.user@gmail.com" not in cleaned
    # Check that URL is removed
    assert "https://example.com" not in cleaned
    # Check that special chars are removed except # and +
    assert "!" not in cleaned

def test_preprocess(preprocessor):
    text = "Machine Learning Engineers use Python and PyTorch for modeling."
    processed = preprocessor.preprocess(text, use_spacy=False)
    
    # Should be lowercase
    assert "machine" in processed
    # Stopwords should be removed
    assert "and" not in processed
    assert "for" not in processed
    # Lemmatized word check
    assert "engineer" in processed  # Engineers -> engineer

def test_dataset_generation(tmp_path):
    # Setup temporary directories for testing
    raw_dir = tmp_path / "raw"
    processed_dir = tmp_path / "processed"
    
    loader = DatasetLoader(raw_dir=str(raw_dir), processed_dir=str(processed_dir))
    
    resumes_df = loader.generate_resumes(count=24)
    jds_df = loader.generate_job_descriptions(count=12)
    
    # Check shape
    assert len(resumes_df) == 24
    assert len(jds_df) == 12
    
    # Check columns
    assert "resume_text" in resumes_df.columns
    assert "category" in resumes_df.columns
    assert "resume_id" in resumes_df.columns
    
    assert "jd_text" in jds_df.columns
    assert "category" in jds_df.columns
    assert "jd_id" in jds_df.columns
    
    # Validate report creation
    val_rep = loader.validate_dataset(resumes_df, jds_df)
    imb_rep = loader.analyze_class_imbalance(resumes_df, jds_df)
    loader.write_quality_report(val_rep, imb_rep)
    
    assert os.path.exists(processed_dir / "data_quality_report.md")
    assert os.path.exists(processed_dir / "data_quality_report.json")
