from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone


class UyeManager(BaseUserManager):
    def create_user(self, email, isim, soyisim, password=None):
        if not email:
            raise ValueError('Kullanıcının Mail Adresi Olmalı')

        user = Uye(
            email=UyeManager.normalize_email(email),
            isim=isim,
            soyisim=soyisim
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, isim, soyisim, password, **extra_fields):
        if not email:
            raise ValueError('Kullanıcının Mail Adresi Olmalı')
        user = Uye(
            email=UyeManager.normalize_email(email),
            isim=isim,
            soyisim=soyisim
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)

        user.save(using=self._db)
        return user


class Uye(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    isim = models.CharField(max_length=255)
    soyisim = models.CharField(max_length=255)
    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    tc = models.CharField(max_length=255, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UyeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['isim','soyisim']

    class Meta:
        verbose_name = u"Üye"
        verbose_name_plural = u"Üyeler"

    def get_full_name(self):
        full_name = '%s' % (self.isim)
        return full_name.strip()

    def get_short_name(self):
        return self.isim

    def _str_(self):
        full_name = '%s' % (self.isim)
        return full_name.strip()

class Il(models.Model):
    kod = models.CharField(max_length=32)
    isim = models.CharField(max_length=1024)

    class Meta:
        verbose_name = 'İl'
        verbose_name_plural = 'İller'
        ordering = ['isim']

    def __str__(self):
        return self.isim


class Ilce(models.Model):
    il = models.ForeignKey(Il, on_delete=models.PROTECT)
    isim = models.CharField(max_length=1024)
    kod = models.CharField(max_length=32)
    yurtici_kod = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'İlçe'
        verbose_name_plural = 'İlçeler'
        ordering = ['isim']

    def __str__(self):
        return self.isim


class Mahalle(models.Model):
    ilce = models.ForeignKey(Ilce, on_delete=models.PROTECT)
    isim = models.CharField(max_length=1024)
    kod = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'Mahalle'
        verbose_name_plural = 'Mahalleler'
        ordering = ['isim']

    def __str__(self):
        return self.isim

class UyeAdresi(models.Model):
    user = models.ForeignKey(Uye, on_delete=models.PROTECT)

    baslik = models.CharField(max_length=255)
    isim = models.CharField(max_length=1024)
    adres = models.TextField()
    posta_kodu = models.CharField(max_length=16, blank=True)
    il = models.CharField(max_length=16, blank=True)
    ilce = models.CharField(max_length=16, blank=True)
    mahalle = models.CharField(max_length=16, blank=True)

    tel = models.CharField(max_length=255)
    faks = models.CharField(max_length=255, blank=True)

    firma = models.CharField(max_length=1024, blank=True)
    vergi_dairesi = models.CharField(max_length=1024, blank=True)
    vergi_no = models.CharField(max_length=1024, blank=True)

    Bireysel = 'B'
    Kurumsal = 'K'
    TIP_CHOICES = (
        (Bireysel, 'Bireysel'),
        (Kurumsal, 'Kurumsal'),
    )
    tip = models.CharField(max_length=1, choices=TIP_CHOICES, blank=True, default='B')

    Teslimat = 'T'
    Fatura = 'F'
    Adres_CHOICES = (
        (Teslimat, 'Teslimat'),
        (Fatura, 'Fatura'),
    )
    adres_tipi = models.CharField(max_length=1, choices=Adres_CHOICES, blank=True, default='T')
    silindi = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Kullanıcı Adresi'
        verbose_name_plural = 'Kullanıcı Adresleri'

    def __str__(self):
        return "%s, %s V:%s-%s" % (self.isim, self.adres, self.vergi_dairesi, self.vergi_no)
