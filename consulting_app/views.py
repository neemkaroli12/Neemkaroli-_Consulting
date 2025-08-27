from django.shortcuts import render

def home_two(request):
    return render(request, "home.html")

def about(request):
    return render(request, "about.html")

def vision(request):
    return render(request, "vision.html")

def management(request):
    return render(request, "management.html")