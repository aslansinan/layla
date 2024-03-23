from django.db import models

from satis.models import Sepet


# Create your models here.
class SessionTokens(models.Model):
    user = models.ForeignKey('account.Uye', on_delete=models.PROTECT)
    sepet = models.ForeignKey(Sepet, on_delete=models.PROTECT)
    token = models.CharField(max_length=200)
    temp = models.CharField(max_length=200)
    payment_amount = models.CharField(max_length=200)
    active = models.BooleanField(default=True)