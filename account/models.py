from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
class UyeManager(BaseUserManager):
    def create_user(self, email, isim_soyisim, password=None):
        if not email:
            raise ValueError('Kullanıcının Mail Adresi Olmalı')

        user = Uye(
            email=UyeManager.normalize_email(email),
            isim_soyisim=isim_soyisim,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, isim_soyisim, password, **extra_fields):
        if not email:
            raise ValueError('Kullanıcının Mail Adresi Olmalı')
        user = Uye(
            email=UyeManager.normalize_email(email),
            isim_soyisim=isim_soyisim,
        )
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)

        user.save(using=self._db)
        return user


class Uye(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    isim_soyisim = models.CharField(max_length=255)
    is_active = models.BooleanField('active', default=True, help_text= 'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UyeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['isim_soyisim']
    class Meta:
        verbose_name = u"Üye"
        verbose_name_plural = u"Üyeler"

    def get_full_name(self):
        full_name = '%s' % (self.isim_soyisim)
        return full_name.strip()

    def get_short_name(self):
        return self.isim_soyisim

    def _str_(self):
        full_name = '%s' % (self.isim_soyisim)
        return full_name.strip()

