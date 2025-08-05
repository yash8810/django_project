from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from productapp.models import FitFusionAIProduct

def indexFun(request):
    user_name = request.session.get('user_name', None)
    print(f"User  session: {user_name}")
    
    # Fetch all active & status=True products (you can filter as needed)
    products = FitFusionAIProduct.objects.filter(
        fitfusionai_product_active=True,
        fitfusionai_product_status=True
    ).order_by('-fitfusionai_product_id')[:10]  # limit to 10 latest

    return render(request, 'index.html', {
        'user_name': user_name,
        'products': products,
    })

def indexFun2(request):
    user_name = request.session.get('user_name', None)
    print(f"User  session: {user_name}")
    products = FitFusionAIProduct.objects.filter(
        fitfusionai_product_active=True,
        fitfusionai_product_status=True
    ).order_by('-fitfusionai_product_id')[:10]  # limit to 10 latest

    return render(request, 'index2.html', {
        'user_name': user_name,
        'products': products,
    })

def aboutFun(request):
    user_name = request.session.get('user_name', None)
    return render(request, 'about.html', {'user_name': user_name})

def blogdetailFun(request):
    user_name = request.session.get('user_name', None)
    return render(request, 'blog-details.html', {'user_name': user_name})

def supplementFun(request):
    user_name = request.session.get('user_name', None)  # Default to 'Guest' if no name in session
    return render(request, 'supplement.html', {'user_name': user_name})

def featureFun(request):
    user_name = request.session.get('user_name', None)  # Default to 'Guest' if no name in session
    return render(request, 'feature.html', {'user_name': user_name})

def signupFun(request):
    user_name = request.session.get('user_name', None)  # Default to 'Guest' if no name in session
    return render(request, 'registerapp/templates/sign-up.html', {'user_name': user_name})

def faqFun(request):
    user_name = request.session.get('user_name', None)  # Default to 'Guest' if no name in session
    return render(request, 'faq.html', {'user_name': user_name})
    


