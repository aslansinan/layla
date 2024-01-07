from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('iletisim/', views.contact, name="contact"),
    path('urunler/', views.products, name="products"),
    path('urunler/<int:kategori_id>/', views.urunler_by_kategori, name='urunler_by_kategori'),
    path('urun-detay/<int:urun_id>/', views.urun_detay, name='urun_detay'),
    path('search/', views.search, name="search"),
    path('search/<int:kategori_id>', views.search, name="search"),
]
