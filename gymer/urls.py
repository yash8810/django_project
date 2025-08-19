"""
URL configuration for gymer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views
print("")
print("")
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.indexFun, name="homePage"),
    path('homepage/', views.indexFun2, name="homePage2"),
    path('about/', views.aboutFun, name="aboutPage"),
    path('blogdetails/', views.blogdetailFun, name="blogdetailPage"),
    path('supplement/', views.supplementFun, name="supplementPage"),
    path('features/', views.featureFun, name="featurePage"),
    path('register/', include('registerapp.urls'), name="signupPage"),
    path('product/', include('productapp.urls'), name="productPage"),
    path('regapp/', include('regapp.urls')),
    path('faq/', views.faqFun, name="faqPage"),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
