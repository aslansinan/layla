from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index.html"),
    path('iletisim/', views.contact, name="contact"),
    path('iletisim/form_olustur', views.create_contact_form, name="form_olustur"),
    path('urunler/', views.products, name="products"),
    path('urunler/<int:kategori_id>/', views.urunler_by_kategori, name='urunler_by_kategori'),
    path('urun-detay/<int:urun_id>/', views.urun_detay, name='urun_detay'),
    path('search/', views.search, name="search"),
    path('search/<int:kategori_id>', views.search, name="search"),
]
