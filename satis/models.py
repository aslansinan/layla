from django.db import models

# Create your models here.
class Sepet(models.Model):
    user = models.ForeignKey('account.Uye', blank=True, null=True, on_delete=models.PROTECT)
    vade_ucreti = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)

    HAZIRLIKTA = 'H'
    ODEME = 'O'
    TAMAMLANDI = 'T'
    DURUM_SECENEKLERI = (
        (HAZIRLIKTA, u'Hazırlanıyor'),
        (ODEME, u'Ödemesi Bekleniyor'),
        (TAMAMLANDI, u'Tamamlandı')
    )
    durum = models.CharField(max_length=2, choices=DURUM_SECENEKLERI, blank=True, null=True, default=HAZIRLIKTA)
    order_id = models.CharField(max_length=255, blank=True, null=True)
    trans_id = models.CharField(max_length=255, blank=True, null=True)
    banka_3d_onay_tarihi = models.DateTimeField(blank=True, null=True)
    banka_odeme_tarihi = models.DateTimeField(blank=True, null=True)
    tarih = models.DateTimeField(auto_now_add=True)
    degisim = models.BooleanField(default=False)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True, blank=True)
    guncelleme_tarihi = models.DateTimeField(auto_now_add=True, blank=True)
    def kdv_haric_toplam(self):
        return sum([sepet_satiri.kdv_haric_fiyat() for sepet_satiri in self.sepetsatiri_set.all()])

    def kdv_toplami(self):
        return sum([sepet_satiri.kdv_tutari() for sepet_satiri in self.sepetsatiri_set.all()])

    def kdv_dahil_toplam(self):
        return self.kdv_haric_toplam() + self.kdv_toplami()

    def muaf_olmayan_urun_var(self):
        return self.sepetsatiri_set.filter(urun__kargo_muafiyeti=False).exists()

    def sepet_temizle(self):
        self.sepetsatiri_set.all().delete()
    
    def sepet_urun_adeti(self):
        return self.sepetsatiri_set.all().count()

    class Meta:
        verbose_name = 'Sepet'
        verbose_name_plural = 'Sepetler'

    def __str__(self):
        return self.vade_ucreti if self.vade_ucreti else ''


class SepetSatiri(models.Model):
    sepet = models.ForeignKey(Sepet, on_delete=models.PROTECT)
    urun = models.ForeignKey('pages.Urun', on_delete=models.PROTECT)
    adet = models.IntegerField()

    class Meta:
        verbose_name = 'Sepet Satırı'
        verbose_name_plural = 'Sepet Satırları'

    def __str__(self):
        return self.urun.isim + ' ' + str(self.adet)


class Siparis(models.Model):
    user = models.ForeignKey('account.Uye', on_delete=models.PROTECT)
    sepet = models.ForeignKey(Sepet, on_delete=models.PROTECT)
    tarih = models.DateTimeField()
    order_id = models.CharField(max_length=255, blank=True, null=True)
    trans_id = models.CharField(max_length=255, blank=True, null=True)

    KREDI_KARTI = 'K'
    HAVALE = 'H'
    KAPIDA_ODEME_KREDI_KARTI = 'KK'
    KAPIDA_ODEME_NAKIT = 'KN'
    OKULDA_ODEME = 'O'
    ODEME_TIPLERI = (
        (KREDI_KARTI, 'Kredi Kartı'),
        (HAVALE, 'Havale'),
        (KAPIDA_ODEME_KREDI_KARTI, 'Kapıda Ödeme (Kredi Kartı - Tek Çekim)'),
        (KAPIDA_ODEME_NAKIT, 'Kapıda Ödeme (Nakit)'),
        (OKULDA_ODEME, 'Okulda Ödeme'),
    )
    odeme_tipi = models.CharField(max_length=2, choices=ODEME_TIPLERI, blank=True)

    SEVKIYAT_BEKLENIYOR = 'S'
    ODEMESI_BEKLENIYOR = 'B'
    ODEMESI_GELDI = 'G'
    TAMAMLANDI = 'T'
    IPTAL = 'I'
    KARGOLANDI = 'K'
    FATURALANDI = 'F'
    SIPARIS_DURUMLARI = (
        (SEVKIYAT_BEKLENIYOR, 'Sevkiyat Bekleniyor'),
        (ODEMESI_BEKLENIYOR, 'Ödemesi Bekleniyor'),
        (ODEMESI_GELDI, 'Ödemesi Geldi'),
        (TAMAMLANDI, 'Tamamlandı'),
        (IPTAL, 'İptal'),
        (KARGOLANDI, 'Kargolandı'),
        (FATURALANDI, 'Faturalandı')
    )

    TESLIMAT_ADRESI = 'T'
    KARGO_SUBESI = 'S'
    OKUL = 'O'

    durum = models.CharField(max_length=2, choices=SIPARIS_DURUMLARI)

    kargo_ucreti = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    vade_ucreti = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    kapida_odeme_hizmet_bedeli = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    toplam_tutar = models.DecimalField(max_digits=19, decimal_places=2, null=True, blank=True)
    kargo_notu = models.CharField("Sipariş Notu", max_length=255, blank=True)

    bilgilendirme_maili_gonderildi = models.BooleanField(default=False)
    mail_hata_logu = models.CharField(max_length=1024, null=True, blank=True)

    olusturma_tarihi = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True, null=True, blank=True)
    iptal_tarihi = models.DateTimeField(null=True, blank=True)

    iade_talebi = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Sipariş'
        verbose_name_plural = 'Siparişler'

    def kdv_haric_toplam(self):
        return sum([siparis_satiri.kdv_haric_fiyat() for siparis_satiri in self.siparissatiri_set.all()])

    def kdv_toplami(self):
        return sum([siparis_satiri.kdv_tutari() for siparis_satiri in self.siparissatiri_set.select_related().all()])

    def kdv_dahil_toplam(self):
        return self.kdv_haric_toplam() + self.kdv_toplami()

    def muaf_olmayan_urun_var(self):
        return self.siparissatiri_set.filter(urun__kargo_muafiyeti=False).exists()


    def kdv_ve_vade_dahil_toplam(self):
        return self.kdv_dahil_toplam() + self.vade_farki()

    def toplam_siparis_tutari(self):
        toplam = self.kdv_ve_vade_dahil_toplam()

        if self.kargo_ucreti:
            toplam += self.kargo_ucreti

        if self.kapida_odeme_hizmet_bedeli:
            toplam += self.kapida_odeme_hizmet_bedeli

        return toplam

    def satir_durumu(self):
        satirlar = self.siparissatiri_set.all()
        if len(satirlar.filter(durum='T')) == len(satirlar):
            return u"Tamamlandı"

        if len(satirlar.filter(durum='F')) == len(satirlar):
            return u"Faturalandı"

        if len(satirlar.filter(durum='K')) == len(satirlar):
            return u"Kargolandı"

        if len(satirlar.filter(durum='I')) == len(satirlar):
            return u"İptal"

        if len(satirlar.filter(durum='K')) > 0:
            return u"Kısmi Kargolandı"

        return "Hazırlanıyor"


    def __str__(self):
        return str(self.pk)


class SiparisSatiri(models.Model):
    siparis = models.ForeignKey(Siparis, on_delete=models.PROTECT)
    urun = models.ForeignKey('pages.Urun', on_delete=models.PROTECT)
    adet = models.IntegerField()
    kalan_adet = models.IntegerField(default=0)
    iade_talep_adet = models.IntegerField(blank=True, null=True)
    iade_talep_tarih = models.DateTimeField(blank=True, null=True)
    birim_fiyat = models.DecimalField(max_digits=19, decimal_places=2)
    sira = models.IntegerField()
    ogrenci_ismi = models.CharField(max_length=1024, blank=True, null=True)
    tc_kimlik_no = models.CharField(max_length=1024, blank=True, null=True)

    HAZIRLANIYOR = 'H'
    IPTAL = 'I'
    KARGOLANDI = 'K'
    FATURALANDI = 'F'
    TAMAMLANDI = 'T'
    IADE_TALEBI = 'R'
    DEGISIM_TALEBI = 'D'

    DURUMLAR = (
        (HAZIRLANIYOR, 'Hazırlanıyor'),
        (IPTAL, 'İptal'),
        (KARGOLANDI, 'Kargolandı'),
        (FATURALANDI, 'Faturalandı'),
        (TAMAMLANDI, 'Tamamlandı'),
        (IADE_TALEBI, 'İade Talebi'),
        (DEGISIM_TALEBI, 'Değişim Talebi'),
    )

    durum = models.CharField(max_length=1, choices=DURUMLAR, default=HAZIRLANIYOR)

    ERKEK = 'E'
    KIZ = 'K'
    OGRENCI_CINSIYET_SECENEKLERI = (
        (ERKEK, 'Erkek'),
        (KIZ, 'Kız'),
    )

    class Meta:
        verbose_name = 'Sipariş Satırı'
        verbose_name_plural = 'Sipariş Satırları'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.urun.stok_durumu -= self.adet
        if self.urun.stok_durumu <= 0:
            return "yeterli sayıda ürün sayısı yok"
        else:
            self.urun.save()