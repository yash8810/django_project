from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.loginView, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.logoutView, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("upload/", views.uploadDocument, name="uploadDocument"),
    path("all-documents/", views.allDocuments, name="allDocuments"),
    path("analyze/<int:docId>/", views.analyzePdf, name="analyzePdf"),
    path("ask-ai/", views.askAi, name="askAi"),
    path("document/<int:docId>/", views.viewDocument, name="viewDocument"),
    path("document/<int:docId>/text/", views.extractedContent, name="extractedContent"),
    path("media/user_uploads/<path:path>", views.protectedPdfView, name="protectedPdfView"),
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", views.editProfile, name="editProfile"),
    path("change-password/", views.changePassword, name="changePassword"),
    path('query/', views.query_view, name='query_view'),
    path("api/analyze-pdf/<int:docId>/", views.analyzePdf, name="api_analyze_pdf"),
    path("set-selected-document/", views.set_selected_document, name="set_selected_document"),

    # #  path('subscription/', lambda request: render(request, 'plans.html'), name='subscription'),
    # path('subscription/', views.subscription_plans, name='subscription'),

      

    # path('plans/', views.subscription_plans, name='subscription_plans'),
    # path('status/', views.subscription_status, name='subscription_status'),

    # path('subscription/success/', views.subscription_success, name='subscription_success'),
    # path('subscription/cancel/', views.subscription_cancel, name='subscription_cancel'),
    # path('create-checkout-session/', views.create_checkout_session),
    # path('webhook/', views.my_webhook_view),  # For Stripe events
    # path('subscription/create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),

]
    

 
