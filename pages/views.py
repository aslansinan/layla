from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def deneme(request):
    return render(request, 'index.html')