# Generated by Django 5.0 on 2024-01-14 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_urun_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urun',
            name='kod',
            field=models.CharField(blank=True, default=1, max_length=124),
            preserve_default=False,
        ),
    ]
