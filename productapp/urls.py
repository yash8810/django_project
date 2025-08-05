from django.urls import path
from . import views
from .views import CreateCheckoutSessionView, successFun, cancelFun, my_webhook_view



urlpatterns = [
   
    path('products/', views.productlist, name='productfun'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/cart/', views.cart_view, name='cart'),  # ✅ Your cart view
    path('product/add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),
    #path('create-checkout-session', CreateCheckoutSessionView.as_view(), name="checkoutPage"),
    path('success', successFun, name="successPage"),
    path('cancel', cancelFun, name="cancelPage"),
    path('stripe/webhook/', views.my_webhook_view, name="webhook-stripe"),
    path('create-checkout-session', CreateCheckoutSessionView.as_view(), name="checkoutPage"),


    
]
