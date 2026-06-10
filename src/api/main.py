import os
import sys
import pickle
import logging
import io
from pypdf import PdfReader
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import CLASSIFIER_PATH, VECTORIZER_PATH, MODELS_DIR
from src.ml.ats_predictor import ATSPredictor
from src.nlp.skill_extractor import SkillExtractor
from src.nlp.skill_normalizer import SkillNormalizer
from src.nlp.skill_gap_analyzer import SkillGapAnalyzer
from src.nlp.recommendation_engine import RecommendationEngine
from src.search.job_matcher import JobMatcher
from src.search.candidate_matcher import CandidateMatcher

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI App
app = FastAPI(
    title="ResumeIQ AI API",
    description="Advanced recruiting intelligence, parsing, semantic job matching, and ATS prediction backend.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load machine learning models globally
classifier = None
vectorizer = None
label_encoder = None

try:
    if os.path.exists(CLASSIFIER_PATH) and os.path.exists(VECTORIZER_PATH):
        logger.info("Loading role classification models...")
        with open(CLASSIFIER_PATH, 'rb') as f:
            classifier = pickle.load(f)
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)
            
        le_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
        if os.path.exists(le_path):
            with open(le_path, 'rb') as f:
                label_encoder = pickle.load(f)
        logger.info("Models loaded successfully.")
    else:
        logger.warning("Classification models not found. Predict-role endpoint will return defaults.")
except Exception as e:
    logger.error(f"Error loading machine learning models: {str(e)}")

# Initialize NLP & Search services
try:
    ats_predictor = ATSPredictor()
    skill_extractor = SkillExtractor()
    skill_normalizer = SkillNormalizer()
    gap_analyzer = SkillGapAnalyzer(skill_normalizer)
    recommendation_engine = RecommendationEngine()
    job_matcher = JobMatcher()
    candidate_matcher = CandidateMatcher()
    logger.info("NLP and Search modules initialized successfully.")
except Exception as e:
    logger.error(f"Error initializing services: {str(e)}")


# --- REQUEST & RESPONSE SCHEMAS ---

class ResumeTextRequest(BaseModel):
    resume_text: str = Field(..., description="Full text parsed from the candidate's resume.")

class PredictRoleResponse(BaseModel):
    predicted_role: str = Field(..., description="Predict role category class name.")
    confidence: float = Field(..., description="Prediction confidence score.")

class ATSScoreRequest(BaseModel):
    resume_text: str = Field(..., description="Full text of the resume.")
    required_skills: List[str] = Field(..., description="List of required skills.")

class ATSScoreResponse(BaseModel):
    ats_score: float = Field(..., description="Calculated ATS score out of 100.")
    breakdown: Dict[str, float] = Field(..., description="Itemized scores for skills, experience, projects, and education.")

class ExtractSkillsRequest(BaseModel):
    text: str = Field(..., description="Text content to extract skills from.")

class ExtractSkillsResponse(BaseModel):
    skills: List[str] = Field(..., description="Unique list of extracted canonical skills.")

class JobDict(BaseModel):
    job_id: str
    job_title: str
    jd_text: str

class CandidateDict(BaseModel):
    candidate_id: str
    resume_text: str

class JobMatchRequest(BaseModel):
    resume_text: str
    jobs: List[JobDict]
    top_k: int = 5

class JobMatchResponse(BaseModel):
    top_jobs: List[Dict[str, Any]]

class CandidateMatchRequest(BaseModel):
    job_description: str
    resumes: List[CandidateDict]
    top_k: int = 10

class CandidateMatchResponse(BaseModel):
    top_candidates: List[Dict[str, Any]]

class RecommendationsRequest(BaseModel):
    resume_skills: List[str]
    jd_skills: List[str]

class RecommendationsResponse(BaseModel):
    matched: List[str]
    missing: List[str]
    extra: List[str]
    match_percentage: float
    recommendations: List[str]


# --- API ROUTES ---

@app.get("/health", tags=["Status"])
def get_health():
    """Simple API health check endpoint."""
    return {"status": "healthy"}

@app.get("/version", tags=["Status"])
def get_version():
    """Returns application API metadata versioning info."""
    return {
        "version": "1.0.0",
        "phase": "Phase 6: FastAPI Backend",
        "framework": "FastAPI"
    }

@app.post("/extract-text", tags=["Parser"])
async def extract_text(file: UploadFile = File(...)):
    """Extracts text content from uploaded .pdf or .txt file."""
    filename = file.filename or ""
    content_type = file.content_type or ""
    
    # Check extension
    if not (filename.endswith(".pdf") or filename.endswith(".txt") or "pdf" in content_type or "text" in content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a .pdf or .txt file."
        )
        
    try:
        file_bytes = await file.read()
        
        if filename.endswith(".pdf") or "pdf" in content_type:
            # Parse PDF
            reader = PdfReader(io.BytesIO(file_bytes))
            text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if not text.strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="No text could be extracted from this PDF. It might be scanned or empty."
                )
            return {"text": text.strip()}
            
        else:
            # Parse TXT
            try:
                text = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                # Try latin-1 as fallback
                text = file_bytes.decode("latin-1")
            return {"text": text.strip()}
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error parsing file {filename}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to parse file: {str(e)}"
        )

@app.post("/predict-role", response_model=PredictRoleResponse, tags=["Machine Learning"])
def predict_role(payload: ResumeTextRequest):
    """Predicts candidate category based on resume text using trained classification model."""
    if not payload.resume_text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume text cannot be empty."
        )
        
    if classifier is None or vectorizer is None or label_encoder is None:
        logger.warning("ML Model files not found. Using fallback prediction.")
        return PredictRoleResponse(predicted_role="Software Engineer", confidence=1.0)
        
    try:
        features = vectorizer.transform([payload.resume_text]).toarray()
        pred = classifier.predict(features)[0]
        probs = classifier.predict_proba(features)[0]
        
        predicted_role = label_encoder.inverse_transform([pred])[0]
        confidence = float(probs[pred])
        
        return PredictRoleResponse(
            predicted_role=str(predicted_role),
            confidence=round(confidence, 4)
        )
    except Exception as e:
        logger.error(f"Error during role prediction: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}"
        )

@app.post("/ats-score", response_model=ATSScoreResponse, tags=["Machine Learning"])
def predict_ats_score(payload: ATSScoreRequest):
    """Calculates parsed resume ATS score and detail breakdown relative to required skills list."""
    try:
        res = ats_predictor.predict_ats_score(
            payload.resume_text,
            required_skills=payload.required_skills
        )
        return ATSScoreResponse(
            ats_score=float(res["ats_score"]),
            breakdown=res["breakdown"]
        )
    except Exception as e:
        logger.error(f"Error during ATS scoring: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/extract-skills", response_model=ExtractSkillsResponse, tags=["NLP"])
def extract_skills(payload: ExtractSkillsRequest):
    """Extracts unique lowercase canonical skills from raw input text."""
    try:
        skills = skill_extractor.extract_skills(payload.text)
        normalized = skill_normalizer.normalize_list(skills)
        return ExtractSkillsResponse(skills=normalized)
    except Exception as e:
        logger.error(f"Error extracting skills: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/job-match", response_model=JobMatchResponse, tags=["Search"])
def match_jobs(payload: JobMatchRequest):
    """Searches and matches candidate resume against a set of input job descriptions."""
    try:
        # Convert Pydantic job dictionaries to list of raw dicts for matcher
        jobs_list = [{"job_id": j.job_id, "job_title": j.job_title, "jd_text": j.jd_text} for j in payload.jobs]
        
        # We can rank using the hybrid scoring system to provide the full breakdown
        ranked = job_matcher.rank_jobs(payload.resume_text, jobs_list)
        
        # Cap top_k
        top_jobs = ranked[:payload.top_k]
        
        return JobMatchResponse(top_jobs=top_jobs)
    except Exception as e:
        logger.error(f"Error matching jobs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/candidate-match", response_model=CandidateMatchResponse, tags=["Search"])
def match_candidates(payload: CandidateMatchRequest):
    """Searches and matches a job description against candidate resumes using hybrid scoring."""
    try:
        # Convert resumes Pydantic dicts to raw list
        resumes_list = [{"candidate_id": r.candidate_id, "resume_text": r.resume_text} for r in payload.resumes]
        
        # Rank candidates using hybrid ranker
        ranked = candidate_matcher.rank_candidates(resumes_list, payload.job_description)
        
        # Cap top_k
        top_candidates = ranked[:payload.top_k]
        
        return CandidateMatchResponse(top_candidates=top_candidates)
    except Exception as e:
        logger.error(f"Error matching candidates: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.post("/recommendations", response_model=RecommendationsResponse, tags=["NLP"])
def get_recommendations(payload: RecommendationsRequest):
    """Performs skill gap analysis and returns dynamic recommendations for skill gaps."""
    try:
        gap = gap_analyzer.analyze(payload.resume_skills, payload.jd_skills)
        recs = recommendation_engine.generate_recommendations(gap)
        
        return RecommendationsResponse(
            matched=gap["matched"],
            missing=gap["missing"],
            extra=gap["extra"],
            match_percentage=float(gap["match_percentage"]),
            recommendations=recs
        )
    except Exception as e:
        logger.error(f"Error computing recommendations: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
