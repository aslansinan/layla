# Generated by Django 5.0 on 2024-03-23 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiontokens',
            name='temp',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
