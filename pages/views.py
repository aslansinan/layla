from django.shortcuts import render
from . models import Urun, Kategori, ContactForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
import random

def index(request):
    details = "index.html"
    urunler = Urun.objects.all().order_by('-count')[:6]

    context = {
        'urunler':urunler
    }

    return render(request, details, context)

def contact(request):
    details = "contact.html"
    return render(request, details)

def create_contact_form(request):
    if request.method == 'POST':
        if all(key in request.POST for key in ['isim', 'email', 'telefon', 'baslik', 'mesaj']):
            isim = request.POST['isim']
            email = request.POST['email']
            telefon = request.POST['telefon']
            baslik = request.POST['baslik']
            mesaj = request.POST['mesaj']
            user_ip = request.META.get('REMOTE_ADDR', None)
            ip = user_ip

            new_contact_form = ContactForm(isim=isim, email=email, telefon=telefon, baslik=baslik, mesaj=mesaj, ip=ip)
            new_contact_form.save()
            success = isim + ' için ileti başarı ile gönderilmiştir.'
            return HttpResponse(success)
        else:
            return HttpResponseBadRequest("Form verileri eksik veya hatalı.")


def products(request):
    ana_kategoriler = Kategori.objects.filter(parent__isnull=True, aktif=True)
    details = "products.html"
    urunler = Urun.objects.filter(aktif='True').order_by('fiyat')

    context = {
        'urunler':urunler,
        'ana_kategoriler':ana_kategoriler
    }
    return render(request, details, context)

def urunler_by_kategori(request, kategori_id):
    ana_kategoriler = Kategori.objects.filter(parent__isnull=True, aktif=True)
    secili_kategori = get_object_or_404(Kategori, id=kategori_id, aktif=True)
    alt_kategoriler = secili_kategori.get_descendants(include_self=True)
    urunler = Urun.objects.filter(kategori__in=alt_kategoriler, aktif=True).order_by('fiyat')

    context = {
        'urunler': urunler,
        'ana_kategoriler': ana_kategoriler,
        'secili_kategori': secili_kategori,
    }
    return render(request, 'products_by_category.html', context)

def search(request, kategori_id=None):
    details = "products.html"

    ana_kategoriler = Kategori.objects.filter(parent__isnull=True, aktif=True)
    urunler = Urun.objects.filter(aktif='True')

    if kategori_id:
        details = 'products_by_category.html'
        secili_kategori = get_object_or_404(Kategori, id=kategori_id, aktif=True)
        alt_kategoriler = secili_kategori.get_descendants(include_self=True)
        urunler = Urun.objects.filter(kategori__in=alt_kategoriler, aktif=True).order_by('fiyat')
    
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

    if kategori_id:
        context = {
            'urunler': urunler,
            'ana_kategoriler': ana_kategoriler,
            'secili_kategori': secili_kategori
        }
    else:
        context = {
            'urunler': urunler,
            'ana_kategoriler': ana_kategoriler
        }

    return render(request, details, context)

def urun_detay(request, urun_id):
    urun = get_object_or_404(Urun, id=urun_id)
    
    ana_kategori = urun.kategori.get_ancestors().filter(level=0).first()

    urunler = Urun.objects.filter(kategori__in=ana_kategori.get_descendants(include_self=True), aktif=True).exclude(id=urun_id)
    
    urunler = random.sample(list(urunler), min(4, len(urunler)))

    context = {
        'urun': urun,
        'urunler': urunler
    }
    return render(request, 'product_detail.html', context)