import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import spacy

# Automatically download required NLTK resources
for resource in ['stopwords', 'wordnet', 'omw-1.4', 'punkt']:
    try:
        nltk.data.find(f'corpora/{resource}' if resource != 'punkt' else f'tokenizers/{resource}')
    except LookupError:
        nltk.download(resource, quiet=True)

# Try loading spaCy model, otherwise fall back to NLTK-based preprocessor
nlp = None
try:
    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
except OSError:
    # If not found, try downloading it programmatically, otherwise we'll fall back
    try:
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
    except Exception:
        print("Warning: Could not load or download spaCy 'en_core_web_sm'. Falling back to NLTK-based processing.")

class TextPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()
        
        # Extend stopwords with standard resume metadata words that don't add semantic value to classification
        self.stop_words.update([
            "email", "phone", "mobile", "address", "github", "linkedin", "phone", 
            "com", "www", "http", "https", "profile", "summary", "key", "details",
            "experience", "projects", "education", "certifications", "skills"
        ])

    def clean_text(self, text: str) -> str:
        """Applies basic text cleaning: lowercasing, regex filtering for emails, URLs, and punctuation."""
        if not isinstance(text, str):
            return ""
        
        # 1. Lowercase
        text = text.lower()
        
        # 2. Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        
        # 3. Remove Emails
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # 4. Remove Phone Numbers and other standard digits/formatting
        text = re.sub(r'\+?\d[\d\-\(\)\s]{8,}\d', ' ', text)
        
        # 5. Remove special characters and punctuation, leaving letters and simple spaces
        # (keep # and + for languages like C#, C++, etc.)
        text = re.sub(r'[^a-zA-Z0-9\s\#\+]', ' ', text)
        
        # 6. Remove excess whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def preprocess(self, text: str, use_spacy: bool = True) -> str:
        """Cleans, tokenizes, removes stopwords, and lemmatizes the input text."""
        cleaned = self.clean_text(text)
        
        if use_spacy and nlp is not None:
            # spaCy-based lemmatization
            doc = nlp(cleaned)
            tokens = [
                token.lemma_ for token in doc 
                if token.text not in self.stop_words and not token.is_space and len(token.text) > 1
            ]
            return " ".join(tokens)
        else:
            # NLTK-based fallback
            words = cleaned.split()
            tokens = [
                self.lemmatizer.lemmatize(word) for word in words 
                if word not in self.stop_words and len(word) > 1
            ]
            return " ".join(tokens)

if __name__ == "__main__":
    preprocessor = TextPreprocessor()
    sample_resume = """
    John Doe
    john.doe@gmail.com | +1-555-0199 | github.com/johndoe
    
    SUMMARY
    Machine learning engineer with 5 years experience building deep learning systems.
    
    TECHNICAL SKILLS
    Python, C++, PyTorch, TensorFlow, Docker, Kubernetes.
    """
    cleaned_nltk = preprocessor.preprocess(sample_resume, use_spacy=False)
    cleaned_spacy = preprocessor.preprocess(sample_resume, use_spacy=True)
    
    print("Original Text:\n", sample_resume)
    print("\nProcessed (NLTK Fallback):\n", cleaned_nltk)
    print("\nProcessed (spaCy):\n", cleaned_spacy)
