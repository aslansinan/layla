# Generated by Django 5.0.1 on 2024-01-27 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('satis', '0003_sepetsatiri_fiyat'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='siparissatiri',
            name='sira',
        ),
        migrations.AlterField(
            model_name='siparis',
            name='odeme_tipi',
            field=models.CharField(blank=True, choices=[('K', 'Kredi Kartı'), ('H', 'Havale'), ('KK', 'Kapıda Ödeme (Kredi Kartı - Tek Çekim)'), ('KN', 'Kapıda Ödeme (Nakit)')], max_length=2),
        ),
    ]
