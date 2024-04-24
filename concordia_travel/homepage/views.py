from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render(request, "homepage/index.html")

def about(request):
    return render(request, "homepage/about_us.html")

def search(request):
    pass

def error_page(request):
    pass

