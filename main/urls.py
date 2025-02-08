from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('mint-memory/', views.mint_memory, name='mint_memory'),
    path('waitlist/', views.waitlist, name='waitlist'),
    path('demo/', views.demo, name='demo'),
    path('chatbot-reply/', views.chatbot_reply, name='chatbot_reply'),
    path('register/', views.register, name='register'),
]