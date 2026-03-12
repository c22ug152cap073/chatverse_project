from django.shortcuts import render
from .models import ChatData
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def chatbot_response(user_input):

    data = ChatData.objects.all()

    questions = [d.question for d in data]
    answers = [d.answer for d in data]

    # If database is empty
    if len(questions) == 0:
        return "No chatbot data available."

    questions.append(user_input)

    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(questions)

    similarity = cosine_similarity(tfidf[-1], tfidf)

    # if only one question exists
    if len(questions) <= 1:
        return answers[0]

    index = similarity.argsort()[0][-2]

    return answers[index]


def chat(request):

    response = ""

    if request.method == "POST":
        user_input = request.POST.get("message")
        response = chatbot_response(user_input)

    return render(request, "chat.html", {"response": response})