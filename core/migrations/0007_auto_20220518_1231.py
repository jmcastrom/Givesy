# Generated by Django 2.2.14 on 2022-05-18 12:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20220518_1023'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comunicado',
            fields=[
                ('idComunicado', models.AutoField(primary_key=True, serialize=False)),
                ('es_urgente', models.BooleanField(blank=True, default=False)),
                ('titulo', models.CharField(blank=True, max_length=200)),
                ('descripcion', models.TextField(blank=True)),
                ('departamento', models.TextField()),
                ('ciudad', models.CharField(blank=True, max_length=20)),
                ('direccion', models.CharField(blank=True, max_length=20, null=True)),
                ('telefono', models.CharField(blank=True, max_length=20)),
                ('cuenta_ahorros', models.CharField(blank=True, max_length=20)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Autor', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Servicio',
        ),
    ]