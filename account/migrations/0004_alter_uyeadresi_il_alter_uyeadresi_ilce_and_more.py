# Generated by Django 5.0.1 on 2024-01-27 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_remove_uyeadresi_gsm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uyeadresi',
            name='il',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='uyeadresi',
            name='ilce',
            field=models.CharField(blank=True, max_length=16),
        ),
        migrations.AlterField(
            model_name='uyeadresi',
            name='mahalle',
            field=models.CharField(blank=True, default=1, max_length=16),
            preserve_default=False,
        ),
    ]