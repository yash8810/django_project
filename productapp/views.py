# productapp/views.py
from django.shortcuts import get_object_or_404, render, reverse
from requests import request
from .models import FitFusionAIProduct, FitFusionAICategory, FitFusionAIcart,Order
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.shortcuts import redirect
import stripe
from django.conf import settings
from django.views import generic
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from registerapp.models import User
stripe.api_key = settings.STRIPE_SECRET_KEY
endpoint_secret = settings.STRIPE_WEBHOOK_SECRECT

def productlist(request):
    user_name = request.session.get('user_name', None)

    # Fetch products and categories
    products = FitFusionAIProduct.objects.filter(
        fitfusionai_product_active=True,
        fitfusionai_product_status=True
    )
    categories = FitFusionAICategory.objects.filter(fitfusionai_category_isactive=True)

    # Optional category filter
    selected_category = request.GET.get('category')
    if selected_category:
        products = products.filter(fitfusionai_category_id=selected_category)

    # Always return a response!
    return render(request, 'product.html', {
        'products': products,
        'categories': categories,
        'user_name': user_name,
    })

def product_detail(request, product_id):
    user_name = request.session.get('user_name', None)
    product = get_object_or_404(FitFusionAIProduct, pk=product_id)

    # Build a list of all non-empty image fields
    product_images = [
        product.fitfusionai_product_image1,
        product.fitfusionai_product_image2,
        product.fitfusionai_product_image3,
        product.fitfusionai_product_image4,
        product.fitfusionai_product_image5,
    ]
    # Optional: filter out empty images
    product_images = [img for img in product_images if img]

    return render(request, 'product-detail.html', {
        'product': product,
        'product_images': product_images,
        'user_name': user_name})

def product_list_view(request):
    user_name = request.session.get('user_name', None)
    categories = FitFusionAICategory.objects.filter(fitfusionai_category_isactive=True)
    return render(request, 'product.html', {'categories': categories , 'user_name': user_name})


    

def cart_view(request):
    user_id = request.session.get('user_id')
    user_name = request.session.get('user_name', None)

    if not user_id:
        return render(request, 'cart.html', {'cart_items': [], 'total_price': 0})

    cart_items = FitFusionAIcart.objects.filter(fitfusionai_cart_user_id=user_id)

    total_price = sum(
        item.fitfusionai_product.fitfusionai_product_price * item.fitfusionai_cart_quantity
        for item in cart_items
    )

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'user_name': user_name
    })


# def add_to_cart(request, product_id):
#     user_id = request.session.get('user_id', None)
#     product = get_object_or_404(FitFusionAIProduct, pk=product_id)

#     cart_item, created = FitFusionAIcart.objects.get_or_create( 
#         fitfusionai_product=product,
#         fitfusionai_cart_user_id=user_id,
#         defaults={'fitfusionai_cart_quantity': 1}
#     )

#     if not created:
#         cart_item.fitfusionai_cart_quantity += 1
#         cart_item.save()
#         messages.success(request, f"Updated {product.fitfusionai_product_name} quantity in your cart.")
#     else:
#         messages.success(request, f"Added {product.fitfusionai_product_name} to your cart.")

#     return redirect('cart')  # ✅ Replace 'cart' with the name of your cart URL pattern




def add_to_cart(request, product_id):
    user_id = request.session.get('user_id', None)

    if not user_id:
        messages.error(request, "You must be logged in to add items to your cart.")
        return redirect('signinPage') 

    product = get_object_or_404(FitFusionAIProduct, pk=product_id)

    # ✅ Get quantity from the form
    quantity = int(request.POST.get('quantity', 1))

    # ✅ Get or create cart item
    cart_item, created = FitFusionAIcart.objects.get_or_create(
        fitfusionai_product=product,
        fitfusionai_cart_user_id=user_id,
        defaults={'fitfusionai_cart_quantity': quantity}
    )

    if not created:
        cart_item.fitfusionai_cart_quantity += quantity
        cart_item.save()
        messages.success(request, f"Updated quantity of {product.fitfusionai_product_name} in your cart.")
    else:
        messages.success(request, f"Added {product.fitfusionai_product_name} to your cart.")

    return redirect('cart')


def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(FitFusionAIcart, pk=item_id)

    if request.session.get('user_id') != cart_item.fitfusionai_cart_user_id:
        messages.error(request, "You can't remove this item.")
        return redirect('cart')

    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')

def checkout_success(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('cart')

    cart_items = FitFusionAIcart.objects.filter(fitfusionai_cart_user_id=user_id)

    total_quantity = sum(item.fitfusionai_cart_quantity for item in cart_items)
    total_amount = sum(
        item.fitfusionai_product.fitfusionai_product_price * item.fitfusionai_cart_quantity
        for item in cart_items
    )

    # OPTIONAL: Clear cart after successful checkout
    cart_items.delete()

    return render(request, 'checkout-success.html', {
        'total_quantity': total_quantity,
        'total_amount': total_amount,
    })

def checkout_cancel(request):
    return render(request, 'checkout-cancel.html')


class CreateCheckoutSessionView(generic.View):

    # def get(self, args, *kwargs):

        
    #     host = self.request.get_host()

    #     checkout_session = stripe.checkout.Session.create(
    #         success_url="http://{}{}".format(host, reverse('checkout_success')),
    #         cancel_url="http://{}{}".format(host, reverse('checkout_cancel')),
    #         line_items=[
    #             {
    #                 'price_data':{
    #                     'currency': 'inr',
    #                     'unit_amount': 10000,
    #                     'product_data': {
    #                         'name': 'Basic Plan',

    #                     },
    #                 },
    #                 'quantity': 2,
    #             },
    #         ],
    #         mode='payment',
           
    #     )

    #     return redirect(checkout_session.url, code=303)

   def get(self, request, *args, **kwargs):
        user_id = request.session.get('user_id')
        host = request.get_host()

        if not user_id:
            # Optionally redirect to login if user is not logged in
            return redirect('login')

        cart_items = FitFusionAIcart.objects.filter(fitfusionai_cart_user_id=user_id)

        if not cart_items.exists():
            # If cart is empty, send back to cart page
            return redirect('cart')

        line_items = []

        for item in cart_items:
            product_name = item.fitfusionai_product.fitfusionai_product_name
            unit_amount = int(item.fitfusionai_product.fitfusionai_product_price * 100)  # ₹ → paise
            quantity = item.fitfusionai_cart_quantity

            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': unit_amount,
                    'product_data': {
                        'name': product_name,
                    },
                },
                'quantity': quantity,
            })

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url="http://{}{}".format(host, reverse('checkout_success')),
            cancel_url="http://{}{}".format(host, reverse('checkout_cancel')),
        )

        return redirect(checkout_session.url, code=303)

        
def successFun(request):
    return render(request, 'success.html')

def cancelFun(request):
    return render(request, 'cancel.html')
        
def successFun(request):
    return render(request, 'success.html')

def cancelFun(request):
    return render(request, 'cancel.html')

@csrf_exempt
def my_webhook_view(request):
  print("Webhook triggered")
  payload = request.body

  #print(payload)

  sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
  if sig_header is None:
    return HttpResponse("Missing Stripe Signature Header", status=400)

  event = None

  try:
    event = stripe.Webhook.construct_event(
      payload, sig_header, endpoint_secret
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)

  # Handle the checkout.session.completed event
  if event['type']=='checkout.session.completed':
    session = event['data']['object']

    # Save an order in your database, marked as 'awaiting payment'
    create_order(session)

    # Check if the order is already paid (for example, from a card payment)
    #
    # A delayed notification payment will have an `unpaid` status, as
    # you're still waiting for funds to be transferred from the customer's
    # account.
    if session.payment_status == "paid":
      # Fulfill the purchase
      fulfill_order(session)

  elif event['type'] == 'checkout.session.async_payment_succeeded':
    session = event['data']['object']

    # Fulfill the purchase
    fulfill_order(session)

  elif event['type'] == 'checkout.session.async_payment_failed':
    session = event['data']['object']

    # Send an email to the customer asking them to retry their order
    email_customer_about_failed_payment(session)

  # Passed signature verification
  return HttpResponse(status=200)

def fulfill_order(session):
  print("Fulfilling order")


def create_order(session):
    print("Creating order with session:", session)
  
    try:
        email = (
            session.get('customer_email') or
            (session.get('customer_details') or {}).get('email') or
            'unknown@example.com'
        )
        
        order, created = Order.objects.get_or_create(
            fitfusionai_order_cart_id=session['id'],
            defaults={
                'fitfusionai_order_customer_email': email,
                'fitfusionai_order_amount_total_inr': session.get('amount_total', 0) / 100,
                'fitfusionai_order_currency': session.get('currency', 'INR').upper(),
                'fitfusionai_order_payment_status': session.get('payment_status', 'pending'),
                'fitfusionai_order_payment_intent': session.get('payment_intent'),
                'fitfusionai_order_customer_id': session.get('customer'),
            }
        )
        print("Order created:", created)
    except IntegrityError as e:
        print("Database error:", e)
    except Exception as e:
        print("Unexpected error creating order:", e)

def email_customer_about_failed_payment(session):
  print("Emailing customer")

