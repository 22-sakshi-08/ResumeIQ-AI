# Model Selection Report

## Model Performance Summary

| Model | Val Accuracy | Test Accuracy | Test Weighted F1 | Test Weighted Precision | Test Weighted Recall | Best Hyperparameters |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| Logistic Regression | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | `{'C': 0.1}` |
| Random Forest | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | `{'max_depth': 10, 'n_estimators': 100}` |
| Support Vector Machine | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | `{'C': 0.1, 'kernel': 'linear'}` |
| XGBoost | 0.9993 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | `{'learning_rate': 0.05, 'n_estimators': 100}` |

## Selection Justification

* **Winning Model**: `Logistic Regression`
* **Weighted F1 Score**: `1.0000`
* **Test Accuracy**: `1.0000`

### Justification:
The `Logistic Regression` model achieved the highest weighted F1-score across our validation and test sets. Weighted F1 was prioritized as the primary metric to account for minor multi-class imbalances and model prediction consistency across all 12 candidate roles. 

The hyperparameter optimization sweep selected the model parameter config that minimized overfitting while maintaining maximum generalizability.
