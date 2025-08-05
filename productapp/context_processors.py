from .models import FitFusionAIcart

def cart_items_processor(request):
    user_id = request.session.get('user_id')
    cart_items = []

    if user_id:
        cart_items = FitFusionAIcart.objects.filter(fitfusionai_cart_user_id=user_id)

    return {
        'cart_items': cart_items
    }
