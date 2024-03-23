from django.urls import path
from .views import (
    index,
    success,
    fail, paytr_payment, callback,

)

urlpatterns = [
    path('', index, name='index'),
    path('payment/', paytr_payment, name='payment'),
    path('result/', callback, name='result'),
    path('success/', success, name='success'),
    path('failure/', fail, name='failure'),

]