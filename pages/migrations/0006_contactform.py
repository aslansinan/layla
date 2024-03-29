# Generated by Django 5.0 on 2024-02-03 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_alter_urun_kod'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(blank=True, max_length=20)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('telefon', models.CharField(blank=True, max_length=20)),
                ('baslik', models.CharField(blank=True, max_length=50)),
                ('mesaj', models.CharField(blank=True, max_length=255)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('admin_notu', models.CharField(blank=True, max_length=100)),
                ('durum', models.CharField(choices=[('Y', 'Yeni'), ('O', 'Okundu'), ('K', 'Kapandı')], default='Y', max_length=10)),
                ('olusturma_tarihi', models.DateTimeField(auto_now_add=True)),
                ('guncelleme_tarihi', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'İletişim Formu',
                'verbose_name_plural': 'İletişim Formları',
            },
        ),
    ]
