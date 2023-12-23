from django.contrib import admin

from pages.models import Urun


# Register your models here.
class UrunAdmin(admin.ModelAdmin):
    list_display = ['kod', 'iism']
    search_fields = ['isim']



admin.site.register(Urun, UrunAdmin)