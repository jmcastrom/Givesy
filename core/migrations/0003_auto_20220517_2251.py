# Generated by Django 2.2.14 on 2022-05-17 22:51

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_customuser_productos_ofertados'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='productos_ofertados',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, default=list, null=True, size=None),
        ),
    ]
