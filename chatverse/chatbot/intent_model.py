from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

training_sentences = [
"hello",
"hi",
"hey",
"good morning",
"bye",
"goodbye",
"see you",
"thanks",
"thank you"
]

training_labels = [
"greeting",
"greeting",
"greeting",
"greeting",
"goodbye",
"goodbye",
"goodbye",
"thanks",
"thanks"
]

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(training_sentences)

model = MultinomialNB()

model.fit(X, training_labels)

def predict_intent(text):

    X_test = vectorizer.transform([text])

    intent = model.predict(X_test)[0]

    return intent