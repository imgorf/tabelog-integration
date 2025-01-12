from django.shortcuts import render

def map(request):
    return render(request, 'map.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

