# Generated by Django 5.0 on 2024-01-14 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_merge_0002_kategori_sira_0002_urun_stok_durumu'),
    ]

    operations = [
        migrations.AddField(
            model_name='urun',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
