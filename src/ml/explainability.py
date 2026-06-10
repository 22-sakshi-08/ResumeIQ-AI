import os
import sys
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.config import CLASSIFIER_PATH, VECTORIZER_PATH, MODELS_DIR

def run_explainability_analysis():
    print("Initializing SHAP explainability analysis...")
    
    # 1. Load models
    if not os.path.exists(CLASSIFIER_PATH) or not os.path.exists(VECTORIZER_PATH):
        raise FileNotFoundError("Classifier or Vectorizer model not found. Please run train_classifier.py first.")
        
    with open(CLASSIFIER_PATH, 'rb') as f:
        model = pickle.load(f)
        
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
        
    le_path = os.path.join(MODELS_DIR, "label_encoder.pkl")
    with open(le_path, 'rb') as f:
        label_encoder = pickle.load(f)
        
    # 2. Load dataset validation slice
    processed_resumes_path = "data/processed/preprocessed_resumes.csv"
    df = pd.read_csv(processed_resumes_path)
    df["cleaned_text"] = df["cleaned_text"].fillna("")
    
    # Use validation slice (cap at 200 samples for fast SHAP execution)
    sample_size = min(200, len(df))
    df_sample = df.sample(n=sample_size, random_state=42)
    
    X_sample_tfidf = vectorizer.transform(df_sample["cleaned_text"]).toarray()
    feature_names = vectorizer.get_feature_names_out()
    
    X_sample_df = pd.DataFrame(X_sample_tfidf, columns=feature_names)
    
    # Create directories for outputs
    reports_dir = "docs/reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    summary_plot_path = os.path.join(reports_dir, "shap_summary.png")
    importance_plot_path = os.path.join(reports_dir, "shap_importance.png")
    waterfall_plot_path = os.path.join(reports_dir, "shap_waterfall.png")
    csv_importance_path = os.path.join(reports_dir, "feature_importance.csv")
    
    # 3. Initialize SHAP Explainer
    print("Computing SHAP values (this may take a few seconds)...")
    # Selection of explainer based on model type
    if isinstance(model, LogisticRegression):
        explainer = shap.LinearExplainer(model, X_sample_tfidf)
        shap_values = explainer.shap_values(X_sample_tfidf)
    elif isinstance(model, RandomForestClassifier) or "XGB" in str(type(model)):
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample_tfidf)
    else:
        # Generic explainer fallback
        explainer = shap.Explainer(model.predict_proba, X_sample_tfidf)
        # 100 background samples
        shap_values = explainer(X_sample_tfidf)
        
    # Handle SHAP output shapes across versions & model types
    # TreeExplainer for RF in multiclass returns a list of arrays (one per class)
    # XGBClassifier or new Explainer may return a 3D array: (num_samples, num_features, num_classes)
    
    is_list = isinstance(shap_values, list)
    if is_list:
        # Multiclass list format
        num_classes = len(shap_values)
        num_samples, num_features = shap_values[0].shape
    else:
        # Array format
        if len(shap_values.shape) == 3:
            num_samples, num_features, num_classes = shap_values.shape
            # Convert to list to make plotting code uniform
            shap_values = [shap_values[:, :, i] for i in range(num_classes)]
            is_list = True
        else:
            num_classes = 1
            num_samples, num_features = shap_values.shape
            shap_values = [shap_values]
            
    # 4. Generate SHAP Feature Importance Plot (Global Bar Chart across classes)
    print("Generating SHAP feature importance plot...")
    plt.figure(figsize=(12, 8))
    # Pass list of values to plot average magnitude across all classes
    shap.summary_plot(shap_values, X_sample_df, plot_type="bar", show=False, max_display=15)
    plt.title("SHAP Global Feature Importance (Average across Categories)", fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(importance_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {importance_plot_path}")
    
    # 5. Generate SHAP Summary Plot (For class 0 / Software Engineer as default benchmark)
    print("Generating SHAP summary density plot...")
    plt.figure(figsize=(12, 8))
    class_to_plot = 0
    class_label = label_encoder.inverse_transform([class_to_plot])[0]
    shap.summary_plot(shap_values[class_to_plot], X_sample_df, show=False, max_display=15)
    plt.title(f"SHAP Summary Density Plot: {class_label}", fontsize=14, pad=15)
    plt.tight_layout()
    plt.savefig(summary_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {summary_plot_path}")
    
    # 6. Generate SHAP Waterfall Plot (Explaining 1st sample prediction)
    print("Generating SHAP waterfall plot...")
    plt.figure(figsize=(12, 6))
    
    # Explain first sample
    sample_idx = 0
    # Predict class for first sample
    sample_pred_class = model.predict(X_sample_tfidf[sample_idx:sample_idx+1])[0]
    sample_pred_label = label_encoder.inverse_transform([sample_pred_class])[0]
    
    # Get SHAP values for the predicted class for this sample
    sample_shap = shap_values[sample_pred_class][sample_idx]
    
    # Sort features by impact magnitude
    sorted_indices = np.argsort(np.abs(sample_shap))[::-1][:15]
    sorted_shap = sample_shap[sorted_indices]
    sorted_features = [feature_names[i] for i in sorted_indices]
    
    # Plot as horizontal bar
    colors = ['#ff0051' if val >= 0 else '#008bfb' for val in sorted_shap]
    y_pos = np.arange(len(sorted_features))
    plt.barh(y_pos, sorted_shap, color=colors, align='center')
    plt.yticks(y_pos, sorted_features)
    plt.gca().invert_yaxis() # Top features first
    plt.xlabel('SHAP value (impact on model output)')
    plt.title(f"SHAP Waterfall explanation for Sample 1 (Predicted: {sample_pred_label})", fontsize=14, pad=15)
    plt.axvline(0, color='gray', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(waterfall_plot_path, dpi=150)
    plt.close()
    print(f"Saved: {waterfall_plot_path}")
    
    # 7. Generate Top Features Report (feature_importance.csv)
    print("Generating top features report...")
    # Calculate average absolute SHAP values across all samples and all classes
    mean_abs_shaps = np.zeros(num_features)
    for class_idx in range(num_classes):
        mean_abs_shaps += np.mean(np.abs(shap_values[class_idx]), axis=0)
    mean_abs_shaps /= num_classes
    
    importance_df = pd.DataFrame({
        "Feature": feature_names,
        "Mean_Absolute_SHAP": mean_abs_shaps
    }).sort_values(by="Mean_Absolute_SHAP", ascending=False).reset_index(drop=True)
    
    # Save top 100 features
    importance_df.head(100).to_csv(csv_importance_path, index=False)
    print(f"Saved: {csv_importance_path}")
    print("SHAP explainability analysis completed successfully.")

if __name__ == "__main__":
    run_explainability_analysis()
