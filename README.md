<<<<<<< HEAD
# ResumeIQ AI: Advanced Recruiting Intelligence Platform

ResumeIQ AI is a production-ready, portfolio-quality recruiter dashboard and semantic search system. It leverages deep learning vector representations, FAISS search, classification modeling, and dynamic NLP analysis to match resumes to jobs and rank talent efficiently.

---

## 💻 Tech Stack

### Machine Learning & NLP
* **Transformers**: `sentence-transformers` (`all-MiniLM-L6-v2`) for generating 384-dimensional semantic text embeddings.
* **Vector Index**: `faiss-cpu` (`IndexFlatIP`) for sub-millisecond candidate/job matching using L2-normalized cosine similarity.
* **Classification**: `scikit-learn` (Logistic Regression role classification) and `xgboost`.
* **Explainability**: `shap` for linear prediction token attribution plotting.
* **Extraction**: Regular expressions with custom word boundary checks for matching technical terms (`C++`, `C#`, `.NET`).
* **Text Processing**: `spaCy` (`en_core_web_sm`) and `nltk`.

### Backend Service
* **Framework**: `FastAPI` (Python 3.11)
* **Web Server**: `Uvicorn`
* **Validation**: `Pydantic v2` schemas
* **Client Client**: `HTTPX` (Mock API testing)

### Frontend Dashboard
* **Framework**: `React` (v19) with `TypeScript` and `Vite` (v8)
* **Styling**: `TailwindCSS` (v3) for dark-mode responsive styling.
* **Routing**: `React Router` (v6) HashRouter client-side routing.
* **Charts**: `Recharts` for radar comparisons, category pies, monthly lines, and funnel visualizers.
* **API State**: `@tanstack/react-query` and `Axios`.
* **Testing**: `Vitest` and `React Testing Library`.

---

## 🛠️ Architecture

```mermaid
graph TD
    subgraph Client Application React
        D[Dashboard Page]
        RA[Analyzer Page]
        JM[Job Matcher Page]
        CS[Candidate Search Page]
        A[Analytics Page]
        Axios[Axios API Client]
    end

    subgraph Service Backend FastAPI
        Health[/health]
        Predict[/predict-role]
        ATS[/ats-score]
        Skills[/extract-skills]
        MatchJob[/job-match]
        MatchCand[/candidate-match]
        Recs[/recommendations]
    end

    subgraph Core ML Engines
        Class[Logistic Regression Category Model]
        Embed[SentenceTransformer all-MiniLM-L6-v2]
        FAISS[FAISS Inner Product Index]
        Rule[SkillExtractor & GapAnalyzer]
        Predictor[ATS Scorer]
    end

    D --> Axios
    RA --> Axios
    JM --> Axios
    CS --> Axios
    A --> Axios

    Axios -->|HTTP Requests| Health
    Axios -->|HTTP Requests| Predict
    Axios -->|HTTP Requests| ATS
    Axios -->|HTTP Requests| Skills
    Axios -->|HTTP Requests| MatchJob
    Axios -->|HTTP Requests| MatchCand
    Axios -->|HTTP Requests| Recs

    Predict --> Class
    ATS --> Predictor
    Skills --> Rule
    MatchJob --> FAISS
    MatchCand --> FAISS
    Recs --> Rule
    FAISS --> Embed
```

---

## 📂 Project Structure

```text
AMAZONML/
├── .github/workflows/ci.yml         # CI/CD GitHub Action Pipeline
├── data/
│   ├── jobs/                        # Programmatic sample datasets
│   │   ├── sample_jobs.json
│   │   └── sample_resumes.json
│   └── skills.json                  # Normalized skills dictionary database
├── docs/
│   ├── architecture/                # Detailed system architecture reports
│   └── reports/                     # Matching and frontend reports
├── deployment/
│   └── docker/                      # Multi-stage Dockerfiles and compose configuration
│       ├── backend.Dockerfile
│       ├── frontend.Dockerfile
│       └── docker-compose.yml
├── models/                          # Exported classification models and vectors
│   ├── role_classifier.pkl
│   └── tfidf_vectorizer.pkl
├── src/
│   ├── api/                         # FastAPI application and routes
│   │   └── main.py
│   ├── frontend/                    # Vite React SPA client codebase
│   ├── ml/                          # Feature engineering, training, and evaluation scripts
│   ├── nlp/                         # Regex skill extractor and gap analyzers
│   └── search/                      # FAISS search matching pipelines
├── tests/                           # Complete test suite (54 python tests + 8 vitest)
└── requirements.txt                 # Core python dependencies list
```

---

## 🚀 Installation & Running Locally

### 1. Prerequisites
* Python 3.10 or 3.11
* Node.js (v18 or v20) and npm
* Git

### 2. Set Up the Python Backend
1. Clone the repository and navigate to the project directory:
   ```bash
   cd AmazonMl
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the FastAPI development server:
   ```bash
   uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   * The API documentation will be available at `http://localhost:8000/docs`.

### 3. Set Up the React Frontend
1. Navigate to the frontend directory:
   ```bash
   cd src/frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Launch the Vite dev server:
   ```bash
   npm run dev
   ```
   * Open `http://localhost:5173` (or `http://localhost:3000` via Compose) in your browser.

---

## 🐳 Docker Containerization Setup

Run the entire stack containerized using Docker Compose:

1. Ensure Docker is installed and running.
2. Spin up the containers using the compose manifest:
   ```bash
   docker compose -f deployment/docker/docker-compose.yml up --build -d
   ```
3. Access:
   * **React Frontend Dashboard**: `http://localhost:3000`
   * **FastAPI Backend Server**: `http://localhost:8000/docs`

---

## 🧪 Running Tests

### Backend Test Execution
Validate models, schemas, and router integrations:
```bash
pytest tests/
```

### Frontend Test Execution
Validate React pages, forms, and Recharts containers:
```bash
cd src/frontend
npm run test
```

---

## 🔗 API Documentation

All request payloads use Pydantic models. Below is the endpoint catalog:

* `POST /predict-role`: Predicts class name from resume text (weighted F1 accuracy: 100%).
* `POST /ats-score`: Returns a 0-100 rating based on keyword coverage, project size, and certifications.
* `POST /extract-skills`: Identifies normalized canonical tags using regex.
* `POST /job-match`: Returns ranked job descriptions matching a resume.
* `POST /candidate-match`: Identifies candidate resumes matching a JD using FAISS cosine vector searches.
* `POST /recommendations`: Performs skill gap analysis and returns dynamic recommendations.

---

## 🔮 Future Improvements

1. **Vector Index Partitioning**: Migrate to IVF FAISS index for high-scale document sets (>1M).
2. **Context Window Expansion**: Replace MiniLM with a larger context transformer (e.g. `bge-large-en`) for longer resume processing.
3. **Database Integration**: Set up SQLite persistence for saving matches and historical uploads.
=======
# ResumeIQ-AI
AI-powered recruitment intelligence platform with resume screening, ATS scoring, semantic job matching, skill extraction, and candidate ranking using FastAPI, React, FAISS, and Machine Learning.
>>>>>>> 1fd5a86c5ac67a8193c4aa621772baa938415ff8
