from django.shortcuts import render


def index(request):
    details = "index.html"
    return render(request, details)
