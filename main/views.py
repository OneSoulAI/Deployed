from django.shortcuts import render
import json
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import requests
from openai import OpenAI

from .models import Waitlist
from django.http import JsonResponse
from .models import Waitlist
from datetime import datetime

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = os.getenv("DEEPSEEK_API_URL")

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_API_URL)

def landing_page(request):
    return render(request, 'main/landing-page.html')

def login_page(request):
    return render(request, 'main/login.html')

def mint_memory(request):
    return render(request, 'main/mint-memory.html')

def waitlist(request):
    return render(request, 'main/waitlist.html')

def demo(request):
    return render(request, 'main/demo.html')

@csrf_exempt
def chatbot_reply(request):
    if request.method == "POST":
        data = json.loads(request.body)
        messages = data.get("messages")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": """You are Cupid, the AI matchmaker. Your aim is to find out more about the user and help build a complete profile of them while being entertaining. You will be provided with a array of messages of the form [messages of the following form..., {'role': 'system', 'content': the most recent message from Cupid}, {'role': 'user', 'content': what the user has typed into the bot}] where the last item in the array contains the most recent user message. Using the entire conversation history, you want to generate a response which either seeks to gain more information about the user where it would help build a better picture of their personality profile. You can also use this information to make a joke or a witty comment. Remember, the user is here to have fun and get to know you better, so make sure to keep the conversation light and entertaining. Return a single message in the form {"role": "system", "content": your response, try using emojis to make your responses more engaging}."""},
                {"role": "user", "content": str(messages)}
            ],
            temperature=0.9,
            max_tokens=200,
            top_p=0.8
        )
        print(response.choices[0].message.content)
        return JsonResponse({"reply": json.loads(response.choices[0].message.content)["content"]})

    return JsonResponse({"error": "Invalid request method"}, status=405)

@csrf_exempt  # Allow API calls without CSRF token (remove in production)
def register(request):
    if request.method == "POST":
        try:
            # Extract form data
            fullname = request.POST.get("fullname")
            email = request.POST.get("email")
            location = request.POST.get("location")
            date_of_birth = request.POST.get("date_of_birth")
            gender = request.POST.get("gender")
            preference = request.POST.get("preference")
            social_handle = request.POST.get("social_handle")
            mbti = request.POST.get("mbti")
            partner_preferences = request.POST.get("partner_preferences")

            # Convert date_of_birth from YYYY-MM-DD to proper date format
            if date_of_birth:
                try:
                    date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d").date()
                except ValueError:
                    return JsonResponse({"message": "Invalid date format. Use YYYY-MM-DD", "status": "error"})

            # Ensure all required fields are present
            if not all([fullname, email, location, date_of_birth, gender, preference, social_handle, mbti, partner_preferences]):
                return JsonResponse({"message": "Missing required fields", "status": "error"})

            # ✅ Check if email already exists
            if Waitlist.objects.filter(email=email).exists():
                return JsonResponse({"message": "This email is already registered!", "status": "error"})

            # Save to database
            waiter = Waitlist(
                fullname=fullname,
                email=email,
                location=location,
                date_of_birth=date_of_birth,
                gender=gender,
                preference=preference,
                social_handle=social_handle,
                mbti=mbti,
                partner_preferences=partner_preferences
            )
            waiter.save()

            return JsonResponse({"message": "You have been successfully added to the waitlist!", "status": "success"})
        
        except Exception as e:
            print("Error:", e)
            return JsonResponse({"message": "An error occurred while adding to the waitlist.", "status": "error"})

    return JsonResponse({"message": "Invalid request method", "status": "error"})