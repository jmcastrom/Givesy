# Generated by Django 2.2.14 on 2022-05-18 09:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_fundacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='item2',
            name='ciudad',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='item2',
            name='departamento',
            field=models.CharField(blank=True, max_length=15),
        ),
        migrations.AddField(
            model_name='item2',
            name='es_servicio',
            field=models.BooleanField(blank=True, default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item2',
            name='intercambio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='fundacion',
            name='nombre',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('idServicio', models.AutoField(primary_key=True, serialize=False)),
                ('titulo', models.CharField(blank=True, max_length=50)),
                ('descripcion', models.TextField(blank=True)),
                ('departamento', models.CharField(blank=True, max_length=15)),
                ('ciudad', models.CharField(blank=True, max_length=20)),
                ('categoria', models.CharField(blank=True, max_length=20, null=True)),
                ('tipo', models.CharField(blank=True, max_length=15)),
                ('intercambio', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('ofertante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Ofertante_servicio', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]