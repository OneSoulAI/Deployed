from django.shortcuts import render


def landing_page(request):
    return render(request, 'main/landing-page.html')

def login_page(request):
    return render(request, 'main/login.html')