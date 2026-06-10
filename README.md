# ResumeIQ AI

ResumeIQ AI is a full-stack recruitment intelligence platform designed to streamline resume screening, candidate evaluation, and job matching workflows. The system combines machine learning, semantic search, and rule-based analysis to help recruiters identify relevant candidates, assess ATS compatibility, and discover skill gaps efficiently.

## Key Features

### Resume Classification

Predicts the most relevant job category based on resume content using a trained machine learning model.

### ATS Score Analysis

Evaluates resumes using multiple criteria such as skills, projects, experience, and educational background to generate an ATS-style score.

### Skill Extraction

Extracts and normalizes technical skills from resume text using custom NLP pipelines and pattern matching techniques.

### Semantic Job Matching

Uses transformer-based embeddings and vector similarity search to match resumes with relevant job descriptions.

### Candidate Search

Enables recruiters to identify suitable candidates for a given job description through semantic ranking.

### Recommendation Engine

Provides skill-gap insights and learning recommendations based on candidate profiles.

---

## Technology Stack

### Backend

* Python 3.11
* FastAPI
* Pydantic
* Uvicorn
* Scikit-learn
* XGBoost

### Machine Learning & NLP

* Sentence Transformers
* FAISS
* spaCy
* NLTK
* SHAP

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* React Router
* React Query
* Axios
* Recharts

### Testing

* Pytest
* Vitest
* React Testing Library

---

## Project Structure

```text
ResumeIQ-AI
│
├── data/
├── deployment/
├── docs/
├── models/
├── src/
│   ├── api/
│   ├── frontend/
│   ├── ml/
│   ├── nlp/
│   └── search/
├── tests/
├── requirements.txt
└── README.md
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/22-sakshi-08/ResumeIQ-AI.git
cd ResumeIQ-AI
```

### Backend Setup

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
uvicorn src.api.main:app --reload
```

API Documentation:

```text
http://localhost:8000/docs
```

---

### Frontend Setup

Navigate to frontend directory:

```bash
cd src/frontend
```

Install packages:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

Application:

```text
http://localhost:5173
```

---

## Running Tests

Backend:

```bash
pytest tests/
```

Frontend:

```bash
cd src/frontend
npm run test
```

---

## API Endpoints

| Endpoint              | Description                    |
| --------------------- | ------------------------------ |
| POST /predict-role    | Predict candidate role         |
| POST /ats-score       | Generate ATS score             |
| POST /extract-skills  | Extract technical skills       |
| POST /job-match       | Match jobs against resumes     |
| POST /candidate-match | Match candidates against jobs  |
| POST /recommendations | Generate skill recommendations |

---

## Future Enhancements

* Resume PDF parsing with advanced formatting support
* Persistent candidate database
* Authentication and recruiter accounts
* Advanced analytics and reporting
* Large-scale vector indexing for enterprise datasets

---

## Author

**Sakshi Sahu**

B.Tech – Artificial Intelligence & Machine Learning

Lakshmi Narain College of Technology Excellence, Bhopal
