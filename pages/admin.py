from django.contrib import admin
from pages.models import Urun, Kategori, ContactForm


# Register your models here.
class UrunAdmin(admin.ModelAdmin):
    list_display = ['kod', 'isim','fiyat']
    search_fields = ['isim']

class KategoriAdmin(admin.ModelAdmin):
    list_display = ['baslik', 'parent', 'aktif']
    list_filter = ['aktif']
    search_fields = ['baslik']
    ordering = ['parent_id', 'baslik']

class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['isim', 'email', 'baslik', 'mesaj','durum']
    list_filter = ['durum']
    readonly_fields = ['isim','telefon', 'ip', 'email', 'baslik', 'mesaj']


admin.site.register(Urun, UrunAdmin)
admin.site.register(Kategori, KategoriAdmin)
admin.site.register(ContactForm, ContactFormAdmin)
