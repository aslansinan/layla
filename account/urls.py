from django.urls import path
from . import views

urlpatterns = [
    path('', views.anasayfa, name="anasayfa"),
    path('login', views.login_request, name="login"),
    path('register', views.yeni_uye_kayit, name="register"),
    path('logout', views.logout_request, name="logout"),
    path("forget-password/", views.forget_password, name="forget-password"),
    path("mail/change-password/<code>/", views.mail_change_password, name="password-change-with-mail"),
    path('sifre-degistir', views.change_password, name='sifre_degistir'),
    path('yeni-adres-ekle', views.yeni_adres_ekle, name='yeni_adres_ekle'),
    path('siparis-detay/<int:siparis_id>/', views.siparis_detay, name='siparis_detay'),
]
