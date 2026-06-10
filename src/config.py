import os

# Project root path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Data directories
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')

# Models directory
MODELS_DIR = os.path.join(PROJECT_ROOT, 'models')

# Database path
SQLITE_DB_PATH = os.path.join(DATA_DIR, 'resumeiq.db')
DATABASE_URL = f"sqlite:///{SQLITE_DB_PATH}"

# Ensure directories exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
os.makedirs(MODELS_DIR, exist_ok=True)

# Target Role Categories
CATEGORIES = [
    "Software Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Data Analyst",
    "AI Engineer",
    "Backend Developer",
    "Frontend Developer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Cloud Engineer",
    "Cybersecurity Engineer",
    "Business Analyst"
]

# ML / NLP Configurations
SPACY_MODEL = "en_core_web_sm"
SENTENCE_TRANSFORMER_MODEL = "all-MiniLM-L6-v2"
FAISS_INDEX_PATH = os.path.join(MODELS_DIR, "resumes_faiss.index")
CLASSIFIER_PATH = os.path.join(MODELS_DIR, "role_classifier.pkl")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")
SHAP_EXPLAINER_PATH = os.path.join(MODELS_DIR, "shap_explainer.pkl")
