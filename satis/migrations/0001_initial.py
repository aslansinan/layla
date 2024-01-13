# Generated by Django 5.0 on 2024-01-13 12:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pages', '0002_urun_stok_durumu'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sepet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vade_ucreti', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('durum', models.CharField(blank=True, choices=[('H', 'Hazırlanıyor'), ('O', 'Ödemesi Bekleniyor'), ('T', 'Tamamlandı')], default='H', max_length=2, null=True)),
                ('order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('trans_id', models.CharField(blank=True, max_length=255, null=True)),
                ('banka_3d_onay_tarihi', models.DateTimeField(blank=True, null=True)),
                ('banka_odeme_tarihi', models.DateTimeField(blank=True, null=True)),
                ('tarih', models.DateTimeField(auto_now_add=True)),
                ('degisim', models.BooleanField(default=False)),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True)),
                ('guncelleme_tarihi', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sepet',
                'verbose_name_plural': 'Sepetler',
            },
        ),
        migrations.CreateModel(
            name='SepetSatiri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adet', models.IntegerField()),
                ('sepet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='satis.sepet')),
                ('urun', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pages.urun')),
            ],
            options={
                'verbose_name': 'Sepet Satırı',
                'verbose_name_plural': 'Sepet Satırları',
            },
        ),
        migrations.CreateModel(
            name='Siparis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tarih', models.DateTimeField()),
                ('order_id', models.CharField(blank=True, max_length=255, null=True)),
                ('trans_id', models.CharField(blank=True, max_length=255, null=True)),
                ('odeme_tipi', models.CharField(blank=True, choices=[('K', 'Kredi Kartı'), ('H', 'Havale'), ('KK', 'Kapıda Ödeme (Kredi Kartı - Tek Çekim)'), ('KN', 'Kapıda Ödeme (Nakit)'), ('O', 'Okulda Ödeme')], max_length=2)),
                ('durum', models.CharField(choices=[('S', 'Sevkiyat Bekleniyor'), ('B', 'Ödemesi Bekleniyor'), ('G', 'Ödemesi Geldi'), ('T', 'Tamamlandı'), ('I', 'İptal'), ('K', 'Kargolandı'), ('F', 'Faturalandı')], max_length=2)),
                ('kargo_ucreti', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('vade_ucreti', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('kapida_odeme_hizmet_bedeli', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('toplam_tutar', models.DecimalField(blank=True, decimal_places=2, max_digits=19, null=True)),
                ('kargo_notu', models.CharField(blank=True, max_length=255, verbose_name='Sipariş Notu')),
                ('bilgilendirme_maili_gonderildi', models.BooleanField(default=False)),
                ('mail_hata_logu', models.CharField(blank=True, max_length=1024, null=True)),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True, null=True)),
                ('guncelleme_tarihi', models.DateTimeField(auto_now=True, null=True)),
                ('iptal_tarihi', models.DateTimeField(blank=True, null=True)),
                ('iade_talebi', models.BooleanField(default=False)),
                ('sepet', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='satis.sepet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Sipariş',
                'verbose_name_plural': 'Siparişler',
            },
        ),
        migrations.CreateModel(
            name='SiparisSatiri',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adet', models.IntegerField()),
                ('kalan_adet', models.IntegerField(default=0)),
                ('iade_talep_adet', models.IntegerField(blank=True, null=True)),
                ('iade_talep_tarih', models.DateTimeField(blank=True, null=True)),
                ('birim_fiyat', models.DecimalField(decimal_places=2, max_digits=19)),
                ('sira', models.IntegerField()),
                ('sinif_ismi', models.CharField(blank=True, max_length=255, null=True)),
                ('ogrenci_ismi', models.CharField(blank=True, max_length=1024, null=True)),
                ('tc_kimlik_no', models.CharField(blank=True, max_length=1024, null=True)),
                ('durum', models.CharField(choices=[('H', 'Hazırlanıyor'), ('I', 'İptal'), ('K', 'Kargolandı'), ('F', 'Faturalandı'), ('T', 'Tamamlandı'), ('R', 'İade Talebi'), ('D', 'Değişim Talebi')], default='H', max_length=1)),
                ('siparis', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='satis.siparis')),
                ('urun', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pages.urun')),
            ],
            options={
                'verbose_name': 'Sipariş Satırı',
                'verbose_name_plural': 'Sipariş Satırları',
            },
        ),
    ]
