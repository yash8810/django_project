import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from regapp.generate_response import generate_response  # Import the generate_response function

# Render chatbot HTML page
def chatfunction(request):
    return render(request, 'chatbot.html')

# Function to generate static response
# def generate_response(query):
#     return "I'm a gym assistant bot! Let's crush your fitness goals together. 💪"

# Handle AJAX POST request from frontend
@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '').strip()
            if not query:
                return JsonResponse({'response': 'Please enter a valid question.'}, status=400)

            response = generate_response(query)
            return JsonResponse({'response': response})

        except Exception as e:
            print("❌ Error in chat_api:", str(e))
            return JsonResponse({'response': f"An error occurred: {str(e)}"}, status=500)

    return JsonResponse({'response': 'Only POST method is allowed.'}, status=405)
