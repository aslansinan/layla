from django.urls import path
from . import views
from .views import sepetim

urlpatterns = [
    path('sepetim/', sepetim, name='sepetim'),
]
