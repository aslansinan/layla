from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexaccount, name="account_index"),
    path('login', views.login_request, name="login"),
    path('register', views.yeni_uye_kayit, name="register"),
    path('logout', views.logout_request, name="logout"),
    path("forget-password/", views.forget_password, name="forget-password"),
]
