from django.shortcuts import render

def home(request):
    return render(request, 'pages/index.html')

def dashboard(request):
    return render(request, 'pages/dashboard.html')
