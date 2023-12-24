from django.urls import path
from . import views

urlpatterns = [
    path('', views.indexaccount, name="account_index"),
]
