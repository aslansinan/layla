from django.shortcuts import render
from . models import Urun


def index(request):
    details = "index.html"
    urunler = Urun.objects.all().order_by('isim')[:6]

    context = {
        'urunler':urunler
    }

    return render(request, details, context)

def contact(request):
    details = "contact.html"
    return render(request, details)
