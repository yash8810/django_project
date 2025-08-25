from django.urls import path
from . import views
from payment.views import stripe_webhook

app_name = 'payment'

urlpatterns = [
    path('plans/', views.PlanListView.as_view(), name='plans'),  # This name fixes the NoReverseMatch
    path('create-checkout-session/', views.CheckoutSessionView.as_view(), name='create_checkout_session'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('success/', views.subscription_success, name='subscription_success'),
    path('cancel/', views.subscription_cancel, name='subscription_cancel'),
]