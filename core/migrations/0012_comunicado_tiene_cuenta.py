# Generated by Django 2.2.14 on 2022-06-01 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_item2_busca_intercambio'),
    ]

    operations = [
        migrations.AddField(
            model_name='comunicado',
            name='tiene_cuenta',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
