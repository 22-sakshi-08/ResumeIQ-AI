# Changelog

All notable changes to **ResumeIQ AI** will be documented in this file.

---

## [1.0.0] - 2026-06-09

### Added
* **Phase 1 (Data Creation)**: Compiled synthetic data pipeline generating balanced candidate categories.
* **Phase 2 (Preprocessing)**: Engineered text parsing and cleaning routines utilizing SpaCy lemmatization and NLTK fallbacks.
* **Phase 3 (Predictors & XAI)**: Trained Logistic Regression, XGBoost, and SVM classifiers; integrated SHAP linear explainers; implemented ATS Scorer metrics.
* **Phase 4 (Skill Extraction)**: Built 100+ normalized skills JSON database, boundary-safe regex matching, gap analyzers, and learning track generators.
* **Phase 5 (FAISS Vector Search)**: Integrated sentence-transformers (`all-MiniLM-L6-v2`) and FAISS flat inner product indexing for sub-millisecond similarity matching.
* **Phase 6 (FastAPI Services)**: Implemented FastAPI router exposing 8 Pydantic-validated endpoints, logging middleware, and health diagnostics.
* **Phase 7 (React Frontend)**: Created responsive dark-mode Vite recruiter dashboard with Recharts visualizations, Axios client state managers, and Vitest test suites.
* **Phase 8 (MLOps Containerization)**: Configured multi-stage Dockerfiles, compose setups, Kubernetes yaml manifests, and Github Actions CI pipelines.
