from django.shortcuts import redirect
from django.urls import reverse

class SubscriptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # List of paths that don't require subscription
        open_paths = [
            reverse('home'),
            reverse('login'),
            reverse('register'),
            reverse('payment:plans'),
            reverse('payment:subscription_success'),  # Now it will use the success template
            reverse('payment:subscription_cancel'),
            reverse('payment:stripe_webhook'),
            reverse('payment:create_checkout_session'),
        
            
        ]
        
        response = self.get_response(request)
        
        # Skip for anonymous users or API requests
        if not request.user.is_authenticated or request.path.startswith('/api/'):
            return response
            
        # Skip for open paths
        if request.path in open_paths:
            return response
            
        # Check subscription for premium paths
        if not request.user.has_active_subscription and request.path not in open_paths:
            return redirect('payment:plans')  # Ensure this redirects properly to 'payment:plans'
        
        return response
