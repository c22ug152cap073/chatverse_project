import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count

from .models import ChatData, ChatHistory
from .nlp_engine import preprocess, extract_entities
from .intent_model import predict_intent


analyzer = SentimentIntensityAnalyzer()


def chatbot_response(user_input):

    data = ChatData.objects.all().values()

    if not data:
        return "Chatbot has no training data."

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

        intent = predict_intent(user_input)

        if intent == "greeting":
            response = "Hello! Welcome to ChatVerse"

        elif intent == "goodbye":
            response = "Goodbye! Have a great day."

        elif intent == "thanks":
            response = "You're welcome!"

        else:
            response = chatbot_response(user_input)

        entities = extract_entities(user_input)

        if entities:
            entity_text = ", ".join([f"{e[0]} ({e[1]})" for e in entities])
            response += f" | Detected entities: {entity_text}"

        sentiment = analyzer.polarity_scores(user_input)

        if sentiment['compound'] >= 0.5:
            response = "😊 " + response

        elif sentiment['compound'] <= -0.5:
            response = "😔 I'm sorry you're feeling upset. " + response

        ChatHistory.objects.create(
            user_message=user_input,
            bot_response=response
        )

        return JsonResponse({"response": response})

    history = []   # prevents old chats from showing

    return render(request, "chat.html", {"history": history})


def dashboard(request):

    total_chats = ChatHistory.objects.count()

    common_questions = (
        ChatHistory.objects.values("user_message")
        .annotate(count=Count("user_message"))
        .order_by("-count")[:5]
    )

    return render(request, "dashboard.html", {
        "total_chats": total_chats,
        "common_questions": common_questions
    })