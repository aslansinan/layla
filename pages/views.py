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

def products(request):
    details = "products.html"
    urunler = Urun.objects.filter(aktif='True').order_by('fiyat')

    context = {
        'urunler':urunler
    }
    return render(request, details, context)

def search(request):
    details = "products.html"

    urunler = Urun.objects.filter(aktif='True')

    search_query = request.GET.get('search', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    if search_query:
        urunler = urunler.filter(isim__icontains=search_query)

    if min_price and max_price:
        urunler = urunler.filter(fiyat__range=(min_price, max_price))
    elif min_price:
        urunler = urunler.filter(fiyat__gte=min_price)
    elif max_price:
        urunler = urunler.filter(fiyat__lte=max_price)

    urunler = urunler.order_by('fiyat')

    context = {
        'urunler': urunler
    }

    return render(request, details, context)