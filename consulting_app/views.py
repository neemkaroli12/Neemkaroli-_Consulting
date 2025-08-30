from django.shortcuts import render

def home_two(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def vision(request):
    return render(request, "vision.html")

def leadership(request):
    return render(request, "leadership.html")