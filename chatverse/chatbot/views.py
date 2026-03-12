import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from django.shortcuts import render
from django.http import JsonResponse

from .models import ChatData, ChatHistory
from .nlp_engine import preprocess


analyzer = SentimentIntensityAnalyzer()


def chatbot_response(user_input):

    # fetch chatbot knowledge base
    data = ChatData.objects.all().values()

    if not data:
        return "Chatbot has no training data."

    # convert to pandas dataframe
    df = pd.DataFrame(data)

    questions = df["question"].apply(preprocess).tolist()
    answers = df["answer"].tolist()

    processed_input = preprocess(user_input)

    questions.append(processed_input)

    vectorizer = TfidfVectorizer()

    tfidf = vectorizer.fit_transform(questions)

    similarity = cosine_similarity(tfidf[-1], tfidf)

    similarity_scores = np.array(similarity[0])

    best_match_index = similarity_scores.argsort()[-2]

    return answers[best_match_index]


def chat(request):

    if request.method == "POST":

        user_input = request.POST.get("message")

        # detect sentiment
        sentiment = analyzer.polarity_scores(user_input)

        if sentiment['compound'] >= 0.5:
            mood = "positive"
        elif sentiment['compound'] <= -0.5:
            mood = "negative"
        else:
            mood = "neutral"

        response = chatbot_response(user_input)

        if mood == "positive":
            response = "😊 I'm glad you're feeling positive! " + response

        if mood == "negative":
            response = "😔 I'm sorry you're feeling upset. " + response

        # save chat history
        ChatHistory.objects.create(
            user_message=user_input,
            bot_response=response
        )

        return JsonResponse({"response": response})

    history = ChatHistory.objects.all().order_by("timestamp")

    return render(request, "chat.html", {"history": history})


def chatbot_response(user_input):

    # fetch database data
    data = ChatData.objects.all().values()

    if not data:
        return "Chatbot has no training data."

    # convert to pandas dataframe
    df = pd.DataFrame(data)

    questions = df["question"].apply(preprocess).tolist()
    answers = df["answer"].tolist()

    processed_input = preprocess(user_input)

    questions.append(processed_input)

    # TF-IDF vectorization
    vectorizer = TfidfVectorizer()

    tfidf = vectorizer.fit_transform(questions)

    # cosine similarity
    similarity = cosine_similarity(tfidf[-1], tfidf)

    # convert to numpy array
    similarity_scores = np.array(similarity[0])

    best_match_index = similarity_scores.argsort()[-2]

    return answers[best_match_index]


def chat(request):

    if request.method == "POST":

        user_input = request.POST.get("message")

        response = chatbot_response(user_input)

        ChatHistory.objects.create(
            user_message=user_input,
            bot_response=response
        )

        return JsonResponse({"response": response})

    history = ChatHistory.objects.all().order_by("timestamp")

    return render(request, "chat.html", {"history": history})