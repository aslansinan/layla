# Generated by Django 5.0 on 2024-01-14 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kategori',
            name='sira',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
