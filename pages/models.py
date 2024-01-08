from django.db import models


# Create your models here.
class Urun(models.Model):
    isim = models.CharField(max_length=25, verbose_name='İSİM')
    kod = models.CharField(max_length=4, blank=True, null=True)
    aciklama = models.CharField(max_length=124, blank=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    resim = models.ImageField(upload_to="products/%Y/%m/%d/", default="products/default_product_image.jpg")

    aktif = models.BooleanField(default=True)
    class Meta:
        ordering = ['-aktif', 'isim']
        verbose_name = u'Urun'
        verbose_name_plural = u'Urunler(Urunlar)'

    def __str__(self):
        return self.isim
