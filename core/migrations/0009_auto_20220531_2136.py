# Generated by Django 2.2.14 on 2022-05-31 21:36

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20220531_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='contact_link',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone',
        ),
        migrations.AddField(
            model_name='comunicado',
            name='email',
            field=models.CharField(blank=True, default='ejemplo@eafit.edu.co', max_length=40),
        ),
        migrations.AddField(
            model_name='customuser',
            name='comunicados',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(blank=True, null=True), blank=True, default=list, null=True, size=None),
        ),
        migrations.AddField(
            model_name='fundacion',
            name='email',
            field=models.CharField(blank=True, default='ejemplo@eafit.edu.co', max_length=40),
        ),
        migrations.AddField(
            model_name='item2',
            name='email',
            field=models.CharField(blank=True, default='ejemplo@eafit.edu.co', max_length=40),
        ),
        migrations.AddField(
            model_name='item2',
            name='telefono',
            field=models.CharField(blank=True, default='555-666', max_length=40),
        ),
        migrations.AlterField(
            model_name='comunicado',
            name='telefono',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='fundacion',
            name='telefono',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
