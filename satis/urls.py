from django.urls import path
from . import views
from .views import sepetim, sepete_ekle

urlpatterns = [
    path('sepetim/', sepetim, name='sepetim'),
    path('sepete-ekle/<int:urun_id>/', sepete_ekle, name='sepete_ekle'),
    path('miktar_degistir/<int:sepet_satiri_id>/<str:operation>/', views.miktar_degistir, name='miktar_degistir'),
    path('sepetten_kaldir/<int:sepet_satiri_id>/', views.sepetten_kaldir, name='sepetten_kaldir'),
    path('sepeti_temizle/', views.sepeti_temizle, name='sepeti_temizle'),
    path('sepet_urun_adeti/', views.sepet_urun_adeti, name='sepet_urun_adeti'),
]
