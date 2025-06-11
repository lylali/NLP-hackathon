import spacy
from transformers import pipeline

class NewsAnalyzer:
    def __init__(self):
        # Load models
        self.ner_model = spacy.load("en_core_web_sm")
        self.sentiment_model = pipeline("sentiment-analysis")

    def run_ner(self, text):
        """Extract named entities: PERSON, ORG, GPE"""
        doc = self.ner_model(text)
        entities = [ent.text for ent in doc.ents if ent.label_ in {"PERSON", "ORG", "GPE"}]
        return list(set(entities))  # Deduplicate

    def run_sentiment(self, text):
        """Return sentiment label and score"""
        try:
            result = self.sentiment_model(text[:512])[0]  # Limit length
            return result['label'], result['score']
        except Exception as e:
            return "ERROR", 0.0
