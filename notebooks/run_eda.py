import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# Add src to python path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.ml.dataset_loader import DatasetLoader
from src.ml.preprocessor import TextPreprocessor

def run_eda_and_preprocess():
    print("Starting EDA and Preprocessing...")
    
    # 1. Paths
    raw_dir = os.path.abspath("data/raw")
    processed_dir = os.path.abspath("data/processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    resumes_path = os.path.join(raw_dir, "resumes.csv")
    jds_path = os.path.join(raw_dir, "job_descriptions.csv")
    
    # Check if files exist, if not generate them
    if not os.path.exists(resumes_path) or not os.path.exists(jds_path):
        print("Raw data not found. Generating datasets first...")
        loader = DatasetLoader(raw_dir=raw_dir, processed_dir=processed_dir)
        resumes_df = loader.generate_resumes(count=10000)
        jds_df = loader.generate_job_descriptions(count=1200)
        
        val_rep = loader.validate_dataset(resumes_df, jds_df)
        imb_rep = loader.analyze_class_imbalance(resumes_df, jds_df)
        loader.write_quality_report(val_rep, imb_rep)
    else:
        print("Loading existing raw datasets...")
        resumes_df = pd.read_csv(resumes_path)
        jds_df = pd.read_csv(jds_path)
        
    print(f"Loaded {len(resumes_df)} resumes and {len(jds_df)} job descriptions.")
    
    # 2. Category Distribution Plot
    print("Plotting category distribution...")
    plt.figure(figsize=(12, 6))
    resume_counts = resumes_df["category"].value_counts().sort_values(ascending=True)
    resume_counts.plot(kind="barh", color="skyblue")
    plt.title("Resume Distribution by Role Category")
    plt.xlabel("Number of Resumes")
    plt.ylabel("Role Category")
    plt.tight_layout()
    dist_path = os.path.join(processed_dir, "category_distribution.png")
    plt.savefig(dist_path)
    plt.close()
    print(f"Saved category distribution plot to {dist_path}")
    
    # 3. Word Count Distributions
    print("Calculating word counts...")
    resumes_df["word_count"] = resumes_df["resume_text"].apply(lambda x: len(str(x).split()))
    jds_df["word_count"] = jds_df["jd_text"].apply(lambda x: len(str(x).split()))
    
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.hist(resumes_df["word_count"], bins=30, color="lightgreen", edgecolor="black")
    plt.title("Resume Word Count Distribution")
    plt.xlabel("Word Count")
    plt.ylabel("Frequency")
    
    plt.subplot(1, 2, 2)
    plt.hist(jds_df["word_count"], bins=30, color="orange", edgecolor="black")
    plt.title("Job Description Word Count Distribution")
    plt.xlabel("Word Count")
    plt.ylabel("Frequency")
    
    plt.tight_layout()
    wc_path = os.path.join(processed_dir, "word_count_distribution.png")
    plt.savefig(wc_path)
    plt.close()
    print(f"Saved word count distribution plot to {wc_path}")
    
    # 4. Text Preprocessing
    print("Initializing Text Preprocessor...")
    preprocessor = TextPreprocessor()
    
    # Preprocess resumes
    print("Preprocessing resume texts (this might take a few minutes)...")
    # Using use_spacy=True if loaded, else fallback
    # We will print progress every 1000 items
    preprocessed_resumes = []
    for idx, row in resumes_df.iterrows():
        clean_t = preprocessor.preprocess(row["resume_text"], use_spacy=True)
        preprocessed_resumes.append(clean_t)
        if (idx + 1) % 2000 == 0:
            print(f"Processed {idx + 1}/10000 resumes...")
            
    resumes_df["cleaned_text"] = preprocessed_resumes
    
    # Preprocess job descriptions
    print("Preprocessing job description texts...")
    preprocessed_jds = []
    for idx, row in jds_df.iterrows():
        clean_t = preprocessor.preprocess(row["jd_text"], use_spacy=True)
        preprocessed_jds.append(clean_t)
        
    jds_df["cleaned_text"] = preprocessed_jds
    
    # 5. Save Preprocessed Data
    prep_resumes_path = os.path.join(processed_dir, "preprocessed_resumes.csv")
    prep_jds_path = os.path.join(processed_dir, "preprocessed_job_descriptions.csv")
    
    resumes_df[["resume_id", "category", "resume_text", "cleaned_text"]].to_csv(prep_resumes_path, index=False)
    jds_df[["jd_id", "category", "jd_text", "cleaned_text"]].to_csv(prep_jds_path, index=False)
    
    print(f"Saved preprocessed resumes to {prep_resumes_path}")
    print(f"Saved preprocessed job descriptions to {prep_jds_path}")
    
    # 6. Analyze Top N-grams / Keywords
    print("Analyzing top keywords per category...")
    keyword_summary = {}
    for cat in resumes_df["category"].unique():
        cat_texts = resumes_df[resumes_df["category"] == cat]["cleaned_text"]
        all_words = " ".join(cat_texts).split()
        most_common = Counter(all_words).most_common(15)
        keyword_summary[cat] = [word for word, count in most_common]
        
    summary_path = os.path.join(processed_dir, "top_keywords_per_category.json")
    with open(summary_path, "w") as f:
        json.dump(keyword_summary, f, indent=4)
    print(f"Saved keyword summary to {summary_path}")
    
    print("EDA and Preprocessing completed successfully.")

if __name__ == "__main__":
    run_eda_and_preprocess()
