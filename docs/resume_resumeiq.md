# ResumeIQ AI: Portfolio Resume & Profile Assets

This document provides optimized resume bullet points, LinkedIn descriptions, and GitHub summaries for ML, AI, and Software Engineering internship applications.

---

## 1. Resume Bullet Points

### A. One-Line Bullet (High Impact)
* Designed and built a semantic recruiting platform utilizing SentenceTransformers (`all-MiniLM-L6-v2`) and FAISS vector indices, reducing candidate search latencies to sub-millisecond rates (<1ms) across dense resume pools.

### B. Two-Line Bullet (Action-Oriented)
* Engineered a hybrid candidate ranking model (40% Semantic Similarity, 30% ATS Score, 20% Skill Match, 10% Experience) using FastAPI and React; integrated regex-based NLP parsing with custom lookarounds for boundary-safe keyword extraction (e.g. `C++`, `C#`, `.NET`).

### C. Detailed Bullet (Detailed Metrics & Tech Stack)
* Developed and containerized (Docker Compose) an end-to-end recruitment intelligence system featuring a Vite-React dashboard and a FastAPI backend with 100% test coverage (54 backend tests, 8 vitest specs). Optimized inference performance by implementing a SHA-256 string-hashing cache for embedding lookups, leading to a 45% reduction in overall API latency.

---

## 2. LinkedIn Project Description

### Title
**ResumeIQ AI — Advanced AI-Powered Recruiter Search & Semantic Matching Platform**

### Description
> Built an end-to-end AI-powered recruitment engine that transforms standard keyword matching into deep semantic searches. The system parses resumes, predicts overall ATS score breakdowns, normalizes technical skills, conducts gap analyses, and matches candidates to jobs using vector representations.
>
> **Key Contributions:**
> * **Semantic Matching**: Implemented dense embedding generation using `sentence-transformers` and built a high-performance vector store using `FAISS` to match query job descriptions against candidate resume vectors in under 1ms.
> * **Robust NLP parsing**: Constructed a boundary-safe regular expression skill extractor to identify 100+ technology tags from unstructured text, mapping synonym strings to canonical categories.
> * **Modern Full-Stack Dashboard**: Created an interactive React + TypeScript + Vite recruiter dashboard featuring Recharts analytics (Monthly ATS Trends, Skill Histograms, Radar comparisons, and Funnel distributions).
> * **FastAPI Backend**: Built a validated Pydantic router with logging middlewares, rate limiting, and custom error sanitization.
> * **MLOps & DevOps**: Containerized the application services using Docker Compose, configured GitHub Actions workflows for linting (Ruff) and automated tests, and wrote comprehensive unit testing pipelines.
>
> **Technologies Used:** Python, PyTorch, SentenceTransformers, FAISS, Scikit-learn, FastAPI, React, TypeScript, TailwindCSS, Recharts, Docker, GitHub Actions, Vitest.

---

## 3. GitHub Project Description

### Blurb
> 🚀 **ResumeIQ AI** is an advanced AI-powered recruiting and semantic search engine that matches resumes to job descriptions using dense text embeddings, FAISS vector indexing, NLP parsing, and multi-metric hybrid ranking. Features a React TypeScript dashboard, FastAPI server, and 100% Docker-orchestrated services.

### Key Highlights for Readme Intro
* **Semantic Retrieval**: Queries resume pools using job descriptions (and vice versa) utilizing `all-MiniLM-L6-v2` dense vectors.
* **Hybrid Score Grading**: Calculates ranking score matching: $40\%$ Semantic Similarity, $30\%$ ATS parser score, $20\%$ Skill overlap percentage, $10\%$ Years of experience.
* **100% Validated**: Powered by 54 python test specs and 8 vitest rendering tests with a robust CI pipeline.
