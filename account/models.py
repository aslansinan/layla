from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext as _


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

    def create_superuser(self, email, isim_soyisim, password):
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
    email = models.EmailField(unique=True)
    isim_soyisim = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    olusturma_tarihi = models.DateTimeField(auto_now_add=True)
    guncelleme_tarihi = models.DateTimeField(auto_now=True)
    objects = UyeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['isim_soyisim']
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='custom_user_groups'  # Burada related_name'i değiştirerek çakışmayı gideriyoruz.
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name='custom_user_permissions'  # Burada da related_name'i değiştiriyoruz.
    )

    def __str__(self):
        return self.email
