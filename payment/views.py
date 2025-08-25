import json
import stripe
import logging

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .models import PlanModel, SubscriptionModel
from django.contrib.auth import get_user_model


stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)
User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY
logger = logging.getLogger(__name__)


@method_decorator(login_required, name='dispatch')
class PlanListView(View):
    def get(self, request):
        plans = PlanModel.objects.all()
        current_plan = SubscriptionModel.objects.filter(user=request.user, is_active=True).first()
        return render(request, 'plans.html', {
            'plans': plans,
            'current_plan': current_plan.plan.plan_name if current_plan else None,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
        })

from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

@method_decorator(require_POST, name='dispatch')
class CheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        print("POST data:", request.POST)
        # Ensure the request is AJAX/JSON
        if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            logger.warning("Request missing X-Requested-With header")

            return JsonResponse({'error': 'Invalid request'}, status=400)

        user = request.user
        plan_id = request.POST.get('plan_id')
        logger.info(f"Plan ID received: {plan_id}")

        try:
            plan = PlanModel.objects.get(id=plan_id)
        except PlanModel.DoesNotExist:
            return JsonResponse({'error': 'Plan not found'}, status=404)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': plan.plan_name,
                            'description': plan.plan_description,
                        },
                        'unit_amount': int(plan.plan_price * 100),
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payment/success/'),
                cancel_url=request.build_absolute_uri('/payment/cancel/'),
                metadata={
                    'user_id': str(user.id),
                    'plan_id': str(plan.id),
                }
            )
            return JsonResponse({'sessionId': checkout_session.id})

        except Exception as e:
            logger.error(f"Stripe error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)




@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        logger.error(f"Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error(f"Signature verification failed: {e}")
        return HttpResponse(status=400)

    # Handle the checkout session completion
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session.get('customer_email')
        plan_id = session['metadata'].get('plan_id')  # passed from frontend
        user_id = session['metadata'].get('user_id')  # passed from frontend

        try:
            user = User.objects.get(id=user_id)
            plan = PlanModel.objects.get(id=plan_id)

            # Deactivate existing subscriptions
            #SubscriptionModel.objects.filter(user=user, is_active=True).update(is_active=False)

            # Create new subscription
            SubscriptionModel.objects.create(
                user=user,
                plan=plan,
                remaining_token=plan.plan_token,
                remaining_word_token=plan.plan_word_token,
                is_active=True
            )
            logger.info(f"Subscription created for user {user.email} to plan {plan.plan_name}")
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return HttpResponse(status=500)

    return HttpResponse(status=200)

    return HttpResponse(status=200)


def subscription_success(request):
    return render(request, 'success.html')


def subscription_cancel(request):
    return render(request, 'cancel.html') 
