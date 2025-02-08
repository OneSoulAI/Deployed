from django.shortcuts import render


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