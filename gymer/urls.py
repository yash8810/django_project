

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from . import views

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
