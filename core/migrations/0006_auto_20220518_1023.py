# Generated by Django 2.2.14 on 2022-05-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20220518_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item2',
            name='es_servicio',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]