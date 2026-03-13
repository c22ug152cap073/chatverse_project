import nltk
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK datasets
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Load stopwords
stop_words = set(stopwords.words('english'))

def preprocess(text):

    # convert to lowercase
    text = text.lower()

    # tokenize text
    tokens = word_tokenize(text)

    # remove stopwords
    tokens = [word for word in tokens if word not in stop_words]

    # spaCy lemmatization
    doc = nlp(" ".join(tokens))

    lemmas = [token.lemma_ for token in doc]

    return " ".join(lemmas)


def extract_entities(text):

    doc = nlp(text)

    entities = []

    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    return entities