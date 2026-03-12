import nltk
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_nlp():
    """
    Download required NLTK data for NLP processing.
    Safe to call multiple times - NLTK checks if data already exists.
    """
    required_data = [
        'punkt',           # Tokenizers
        'stopwords',       # Stopwords list
        'wordnet',         # Lemmatization
        'averaged_perceptron_tagger',  # POS tagging
    ]
    
    for item in required_data:
        try:
            nltk.download(item, quiet=True)
            logger.info(f"✓ Downloaded NLTK data: {item}")
        except Exception as e:
            logger.warning(f"⚠ Could not download {item}: {e}")

# Run setup when module is imported
setup_nlp()