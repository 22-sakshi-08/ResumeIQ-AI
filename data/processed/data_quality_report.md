# Data Quality & Validation Report

Generated automatically during Phase 2 setup.

## 1. Dataset Overview

### Resumes Dataset
* **Total Records**: 10000
* **Columns**: `['resume_id', 'category', 'resume_text']`
* **Average Word Count**: 147.5 (Min: 115, Max: 183)
* **Missing/Null Values**:
{
  "resume_id": 0,
  "category": 0,
  "resume_text": 0
}

### Job Descriptions Dataset
* **Total Records**: 1200
* **Columns**: `['jd_id', 'category', 'jd_text']`
* **Average Word Count**: 92.3 (Min: 78, Max: 108)
* **Missing/Null Values**:
{
  "jd_id": 0,
  "category": 0,
  "jd_text": 0
}

---

## 2. Class Imbalance Analysis

An imbalance ratio of `1.0` represents a perfectly balanced dataset.

* **Resume Imbalance Ratio**: 1.001
* **Job Description Imbalance Ratio**: 1.000

### Category Distributions

| Role Category | Resumes Count | Job Descriptions Count |
| :--- | :---: | :---: |
| Software Engineer | 834 | 100 |
| Data Scientist | 834 | 100 |
| Machine Learning Engineer | 834 | 100 |
| Data Analyst | 834 | 100 |
| AI Engineer | 833 | 100 |
| Backend Developer | 833 | 100 |
| Frontend Developer | 833 | 100 |
| Full Stack Developer | 833 | 100 |
| DevOps Engineer | 833 | 100 |
| Cloud Engineer | 833 | 100 |
| Cybersecurity Engineer | 833 | 100 |
| Business Analyst | 833 | 100 |

---
## 3. Data Integrity & Schema Validation Check
* **Check 1: Columns Exist** - PASS
* **Check 2: Non-empty Texts** - PASS
* **Check 3: Clean Tokenizable Text Structure** - PASS
