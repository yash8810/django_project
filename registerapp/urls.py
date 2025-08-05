from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
        path('', views.register, name="registerPage"),  # Registration URL
        path('login/', views.login, name="signinPage"),
        path('logout/', views.logout, name="logout"),
        path('change-password/', views.updatepassword, name="changePasswordPage"),
        path('updateprofile/', views.updateprofile, name="updateprofilePage"),
        path('profile/', views.profile, name="profilePage"),
        
        
      
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
