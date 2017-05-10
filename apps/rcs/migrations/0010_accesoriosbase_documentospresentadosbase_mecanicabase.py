# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0009_condicionesgeneralesbase'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccesoriosBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accesorio', models.CharField(max_length=255)),
                ('existe', models.BooleanField(default=True)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentosPresentadosBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('recibido', models.BooleanField(default=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MecanicaBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parte', models.CharField(max_length=255)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
                ('fk_estado_vehiculo', models.ForeignKey(blank=True, to='rcs.EstadoVehiculo', null=True)),
            ],
        ),
    ]
