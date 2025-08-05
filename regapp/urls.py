from django.urls import path
from . import views




urlpatterns = [
    path('chatbot/', views.chatfunction, name='chatfun'),
    path('chat/', views.chat_api, name='chatAPIPage'),
        
]