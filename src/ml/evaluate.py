import os
import sys
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import label_binarize, LabelEncoder
from sklearn.metrics import (
    confusion_matrix, 
    roc_curve, 
    auc, 
    precision_recall_curve, 
    average_precision_score,
    classification_report,
    roc_auc_score
)

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import CLASSIFIER_PATH, VECTORIZER_PATH, MODELS_DIR

def run_model_evaluation():
    print("Initializing model evaluation script...")
    
    # 1. Paths
    eval_dir = "evaluation"
    os.makedirs(eval_dir, exist_ok=True)
    
    # Load models
    if not os.path.exists(CLASSIFIER_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Classifier or Vectorizer model not found. Please train first.")
        
    with open(CLASSIFIER_PATH, 'rb') as f:
        model = pickle.load(f)
        
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
        
    le_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
    with open(le_path, 'rb') as f:
        label_encoder = pickle.load(f)
        
    # 2. Load dataset and reproduce the test split (15%)
    processed_resumes_path = "data/processed/preprocessed_resumes.csv"
    df = pd.read_csv(processed_resumes_path)
    df["cleaned_text"] = df["cleaned_text"].fillna("")
    
    X_raw = df["cleaned_text"].values
    y_raw = df["category"].values
    
    y = label_encoder.transform(y_raw)
    
    # Re-run train/val/test split to get exact test indices
    from sklearn.model_selection import train_test_split
    X_train_val, X_test_raw, y_train_val, y_test, _, indices_test = train_test_split(
        X_raw, y, df.index, test_size=0.15, stratify=y, random_state=42
    )
    
    # Transform test set
    X_test = vectorizer.transform(X_test_raw).toarray()
    classes = label_encoder.classes_
    n_classes = len(classes)
    
    # Predict labels and probabilities
    y_pred = model.predict(X_test)
    y_score = model.predict_proba(X_test)
    
    # 3. Calculate Overall Metrics
    report_dict = classification_report(y_test, y_pred, target_names=classes, output_dict=True)
    
    # Multi-class ROC-AUC (One-vs-Rest)
    # Binarize y_test
    y_test_binarized = label_binarize(y_test, classes=range(n_classes))
    roc_auc_ovr = roc_auc_score(y_test_binarized, y_score, multi_class="ovr", average="weighted")
    
    print("\n--- TEST METRICS REPORT ---")
    print(f"Accuracy: {report_dict['accuracy']:.4f}")
    print(f"Weighted F1: {report_dict['weighted avg']['f1-score']:.4f}")
    print(f"ROC-AUC (OVR, Weighted): {roc_auc_ovr:.4f}")
    
    # Write summary metrics to markdown file inside evaluation/
    metrics_summary_md = f"""# Test Metrics Summary Report

* **Accuracy**: {report_dict['accuracy']:.4f}
* **Weighted Precision**: {report_dict['weighted avg']['precision']:.4f}
* **Weighted Recall**: {report_dict['weighted avg']['recall']:.4f}
* **Weighted F1 Score**: {report_dict['weighted avg']['f1-score']:.4f}
* **ROC-AUC (OVR, Weighted)**: {roc_auc_ovr:.4f}

## Detailed Metrics per Target Class

| Class Category | Precision | Recall | F1-Score | Support |
| :--- | :---: | :---: | :---: | :---: |
"""
    for cls in classes:
        cls_rep = report_dict[cls]
        metrics_summary_md += f"| {cls} | {cls_rep['precision']:.4f} | {cls_rep['recall']:.4f} | {cls_rep['f1-score']:.4f} | {int(cls_rep['support'])} |\n"
        
    metrics_report_path = os.path.join(eval_dir, "metrics_report.md")
    with open(metrics_report_path, "w", encoding="utf-8") as f:
        f.write(metrics_summary_md)
    print(f"Saved metrics report to {metrics_report_path}")

    # 4. Visualization 1: Confusion Matrix
    print("Generating Confusion Matrix plot...")
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    plt.title('Confusion Matrix on Test Set', fontsize=14, pad=15)
    plt.ylabel('Actual Label', fontsize=12)
    plt.xlabel('Predicted Label', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    plt.tight_layout()
    cm_plot_path = os.path.join(eval_dir, "confusion_matrix.png")
    plt.savefig(cm_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {cm_plot_path}")

    # 5. Visualization 2: ROC Curve (One-vs-Rest for top classes)
    print("Generating ROC Curve plot...")
    plt.figure(figsize=(10, 8))
    
    # Compute ROC curve and ROC area for each class
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test_binarized[:, i], y_score[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])
        
    # Plot top 6 classes for visual clarity, plus micro-average
    # Compute micro-average ROC curve
    fpr["micro"], tpr["micro"], _ = roc_curve(y_test_binarized.ravel(), y_score.ravel())
    roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    
    plt.plot(fpr["micro"], tpr["micro"],
             label=f'micro-average ROC curve (area = {roc_auc["micro"]:.2f})',
             color='deeppink', linestyle=':', linewidth=4)
             
    for i in range(min(6, n_classes)):
        plt.plot(fpr[i], tpr[i], label=f'ROC curve of class {classes[i]} (area = {roc_auc[i]:.2f})')
        
    plt.plot([0, 1], [0, 1], 'k--', lw=2)
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=12)
    plt.ylabel('True Positive Rate', fontsize=12)
    plt.title('Multi-Class ROC Curve (One-vs-Rest)', fontsize=14, pad=15)
    plt.legend(loc="lower right")
    plt.tight_layout()
    roc_plot_path = os.path.join(eval_dir, "roc_curve.png")
    plt.savefig(roc_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {roc_plot_path}")

    # 6. Visualization 3: Precision-Recall Curve (for top classes)
    print("Generating Precision-Recall Curve plot...")
    plt.figure(figsize=(10, 8))
    
    precision = dict()
    recall = dict()
    average_precision = dict()
    for i in range(n_classes):
        precision[i], recall[i], _ = precision_recall_curve(y_test_binarized[:, i], y_score[:, i])
        average_precision[i] = average_precision_score(y_test_binarized[:, i], y_score[:, i])
        
    # Averages
    precision["micro"], recall["micro"], _ = precision_recall_curve(y_test_binarized.ravel(), y_score.ravel())
    average_precision["micro"] = average_precision_score(y_test_binarized, y_score, average="micro")
    
    plt.plot(recall["micro"], precision["micro"],
             label=f'micro-average Precision-recall (area = {average_precision["micro"]:.2f})',
             color='gold', linestyle=':', linewidth=4)
             
    for i in range(min(6, n_classes)):
        plt.plot(recall[i], precision[i], label=f'P-R curve of class {classes[i]} (area = {average_precision[i]:.2f})')
        
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('Recall', fontsize=12)
    plt.ylabel('Precision', fontsize=12)
    plt.title('Multi-Class Precision-Recall Curve', fontsize=14, pad=15)
    plt.legend(loc="lower left")
    plt.tight_layout()
    pr_plot_path = os.path.join(eval_dir, "pr_curve.png")
    plt.savefig(pr_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {pr_plot_path}")

    # 7. Visualization 4: Model Comparison Chart
    print("Generating Model Comparison plot...")
    results_csv_path = "classification_results.csv"
    if os.path.exists(results_csv_path):
        results_df = pd.read_csv(results_csv_path)
        
        # Melt dataframe for easy seaborn plotting
        df_melted = pd.melt(
            results_df, 
            id_vars=['Model'], 
            value_vars=['Val_Accuracy', 'Test_Accuracy', 'Test_Weighted_F1'],
            var_name='Metric', 
            value_name='Value'
        )
        
        plt.figure(figsize=(10, 6))
        sns.barplot(data=df_melted, x='Model', y='Value', hue='Metric', palette='muted')
        plt.title('Classifier Models Performance Comparison', fontsize=14, pad=15)
        plt.ylim(0, 1.1)
        plt.ylabel('Score Value', fontsize=12)
        plt.xlabel('Model', fontsize=12)
        plt.legend(loc='lower right')
        plt.tight_layout()
        comparison_plot_path = os.path.join(eval_dir, "model_comparison.png")
        plt.savefig(comparison_plot_path, dpi=150)
        plt.close()
        print(f"Saved: {comparison_plot_path}")
    else:
        print("Warning: classification_results.csv not found. Skipping Comparison Chart.")
        
    print("Model evaluation plots generation completed successfully.")

if __name__ == "__main__":
    run_model_evaluation()
