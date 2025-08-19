from django.urls import path
from . import views
import os
from groq import Groq



urlpatterns = [
    path('chatbot/', views.chatfunction, name='chatfun'),
    path('chat/', views.chat_api, name='chatAPIPage'),
        
]


client = Groq(api_key=os.getenv("GROQ_API_KEY"))