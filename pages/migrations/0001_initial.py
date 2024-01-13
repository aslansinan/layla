# Generated by Django 5.0 on 2024-01-13 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urun',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(max_length=25, verbose_name='İSİM')),
                ('kod', models.CharField(blank=True, max_length=4, null=True)),
                ('aciklama', models.CharField(blank=True, max_length=124)),
                ('fiyat', models.DecimalField(decimal_places=2, max_digits=10)),
                ('resim', models.ImageField(default='products/default_product_image.jpg', upload_to='products/%Y/%m/%d/')),
                ('aktif', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Urun',
                'verbose_name_plural': 'Urunler(Urunlar)',
                'ordering': ['-aktif', 'isim'],
            },
        ),
    ]
