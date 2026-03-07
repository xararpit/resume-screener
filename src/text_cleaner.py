import re
import spacy

# Load the medium english model. Disable unused pipeline components to keep it fast.
nlp = spacy.load("en_core_web_md", disable=["ner", "parser"])

def clean_text(text):
    if not text:
        return ""
    
    # 1. Basic regex cleanup (urls, weird spacing)
    text = text.lower()
    text = re.sub(r"http\S+\s*", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    # 2. Advanced NLP via SpaCy (Lemmatization)
    doc = nlp(text)
    
    # Keep only alphabetic tokens that are not stop words or punctuation
    clean_tokens = [
        token.lemma_ for token in doc 
        if token.is_alpha and not token.is_stop and not token.is_punct
    ]
    
    return " ".join(clean_tokens)
