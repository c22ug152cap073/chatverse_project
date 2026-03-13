from django.contrib import admin
from django.urls import path
from chatbot.views import chat, dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', chat, name='chat'),
    path('dashboard/', dashboard, name='dashboard'),
]