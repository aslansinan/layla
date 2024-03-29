from django.db import models
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

class Kategori(MPTTModel):
    baslik = models.CharField(max_length=30)
    sira = models.IntegerField()
    aktif = models.BooleanField(default=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    class MPTTMeta:
        order_insertion_by = ['baslik']

    class Meta:
        app_label = 'pages'
    def __str__(self):
        full_path = [self.baslik]
        k = self.parent
        while k is not None:
            full_path.append(k.baslik)
            k = k.parent
        return '/'.join(full_path[::-1])

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'aktif': self.aktif})

class Urun(models.Model):
    kategori = models.ForeignKey(Kategori, on_delete=models.CASCADE)
    aciklama = models.CharField(max_length=255)
    isim = models.CharField(max_length=255, verbose_name='İSİM')
    kod = models.CharField(max_length=4, blank=True, null=True)
    aciklama = models.CharField(max_length=255, blank=True)
    kod = models.CharField(max_length=24, blank=True)
    fiyat = models.DecimalField(max_digits=10, decimal_places=2)
    stok_durumu = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    resim = models.ImageField(upload_to="products/%Y/%m/%d/", default="products/default_product_image.jpg")

    aktif = models.BooleanField(default=True)
    class Meta:
        ordering = ['-aktif', 'isim']
        verbose_name = u'Urun'
        verbose_name_plural = u'Urunler(Urunlar)'

    def __str__(self):
        return self.isim

class ContactForm(models.Model):
    YENI = 'Y'
    OKUNDU = 'O'
    KAPANDI = 'K'
    DURUM_SECENEKLERI = (
        (YENI, 'Yeni'),
        (OKUNDU, 'Okundu'),
        (KAPANDI, 'Kapandı'),
    )
    isim = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    telefon = models.CharField(blank=True, max_length=20)
    baslik = models.CharField(blank=True, max_length=50)
    mesaj = models.CharField(blank=True, max_length=255)
    ip = models.CharField(blank=True, max_length=20)
    admin_notu = models.CharField(blank=True, max_length=100)
    durum = models.CharField(max_length=10, choices=DURUM_SECENEKLERI, default=YENI)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, blank=True)
    guncelleme_tarihi = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.isim
    class Meta:
        verbose_name = 'İletişim Formu'
        verbose_name_plural = 'İletişim Formları'
