from .models import Kategori

def categories(request):
    ana_kategoriler = Kategori.objects.filter(parent__isnull=True, aktif=True)
    return {'ana_kategoriler': ana_kategoriler}