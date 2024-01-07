from django.contrib import admin
from pages.models import Urun, Kategori


# Register your models here.
class UrunAdmin(admin.ModelAdmin):
    list_display = ['kod', 'isim','fiyat']
    search_fields = ['isim']

class KategoriAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'parent', 'aktif']
    list_filter = ['aktif']
    search_fields = ['baslik']
    ordering = ['parent_id', 'baslik']


admin.site.register(Urun, UrunAdmin)
admin.site.register(Kategori, KategoriAdmin)
