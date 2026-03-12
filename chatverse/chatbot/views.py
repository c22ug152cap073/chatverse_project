from django.shortcuts import render

def chat(request):
    response = ""

    if request.method == "POST":
        user_message = request.POST.get("message")

        if user_message.lower() == "hello":
            response = "Hello! How can I help you?"
        elif user_message.lower() == "hi":
            response = "Hi there!"
        elif user_message.lower() == "who are you":
            response = "I am ChatVerse AI chatbot."
        else:
            response = "Sorry, I am still learning."

    return render(request, "chat.html", {"response": response})