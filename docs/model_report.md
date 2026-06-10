# Model Training and Performance Report

This report summarizes the design, training setup, evaluation results, and explainability findings for the **ResumeIQ AI** resume classification and ranking models.

---

## 1. Dataset & Split Summary
- **Total Records**: 10,000 resumes and 1,200 job descriptions across 12 target role categories.
- **Classes**:
  1. Software Engineer
  2. Data Scientist
  3. Machine Learning Engineer
  4. Data Analyst
  5. AI Engineer
  6. Backend Developer
  7. Frontend Developer
  8. Full Stack Developer
  9. DevOps Engineer
  10. Cloud Engineer
  11. Cybersecurity Engineer
  12. Business Analyst
- **Train/Val/Test Split**: Stratified split preserving label ratio:
  - **Train**: 70% (6,999 samples)
  - **Val**: 15% (1,501 samples)
  - **Test**: 15% (1,500 samples)

---

## 2. Features Used
- **TF-IDF Features**: unigrams and bigrams, capped at `max_features=1000` to support fast model training and prevent SHAP runtime issues.
- **Statistical Features**:
  - `word_count`
  - `unique_word_count`
  - `avg_sentence_length`
  - `skill_count`
  - `education_keyword_count`
  - `certification_keyword_count`
  - `project_keyword_count`

---

## 3. Model Performance Comparison

All models were tuned via 3-Fold Stratified Cross-Validation on the training subset:

| Model | Val Accuracy | Test Accuracy | Test Weighted F1 | Best Hyperparameters |
| :--- | :---: | :---: | :---: | :--- |
| **Logistic Regression** | 1.0000 | 1.0000 | 1.0000 | `{'C': 0.1}` |
| **Random Forest** | 1.0000 | 1.0000 | 1.0000 | `{'max_depth': 10, 'n_estimators': 100}` |
| **Support Vector Machine (SVM)** | 1.0000 | 1.0000 | 1.0000 | `{'C': 0.1, 'kernel': 'linear'}` |
| **XGBoost** | 0.9993 | 1.0000 | 1.0000 | `{'learning_rate': 0.05, 'n_estimators': 100}` |

> [!NOTE]
> Due to the clear vocabulary distinctions and keyword configurations built into our synthetic resume generator, all four models converged to 100% test accuracy. The **Logistic Regression** model was selected as the winning architecture due to its lightweight serialization footprint (under 1MB) and high-speed multi-class inference capabilities.

---

## 4. Explainability Analysis (SHAP)
- **Methodology**: Applied `shap.LinearExplainer` on a representative validation subset (100 samples) to inspect local and global token contributions.
- **Key Findings**:
  - Technical keyphrases (e.g. `pytorch` for ML Engineer, `react` for Frontend, `docker`/`kubernetes` for DevOps, and `scrum`/`agile` for Business Analyst) act as dominant predictive vectors.
  - The model ignores standard stopwords and resume boilerplate, matching clean resume terms.

---

## 5. Limitations & Future Improvements
- **Synthetic Data Bias**: The current models are trained on highly structured, synthetic resumes. In real-world environments, resumes will contain unstructured layouts, tables, mixed fonts, and messy text formatting.
- **Feature Sparsity**: Capping TF-IDF at 1,000 features ensures model training stability but might discard less frequent, highly specific domain terms.
- **Next Steps**:
  - Integrate a neural sequence model (e.g. BERT or Sentence-BERT embeddings) directly in the classification step.
  - Gather real-world resumes from public datasets (Kaggle, Github) to fine-tune model boundaries.
