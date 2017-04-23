# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-23 03:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0003_auto_20170422_0848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='accesorios_vehiculo',
            field=models.ManyToManyField(null=True, to='rcs.AccesoriosVehiculo'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='anho',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='cap_puestos',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='cilindros',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='color',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='condiciones_generales_vehiculo',
            field=models.ManyToManyField(null=True, to='rcs.CondicionesGeneralesVehiculo'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='detalles_datos',
            field=models.ManyToManyField(null=True, to='rcs.DetallesDatos'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='documentos_presentados',
            field=models.ManyToManyField(null=True, to='rcs.DocumentosPresentados'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='fk_inspector',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='fk_tipo_vehiculo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rcs.TipoVehiculo'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='kilometraje',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='marca',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='mecanica_vehiculo',
            field=models.ManyToManyField(null=True, to='rcs.MecanicaVehiculo'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='modelo',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='peso',
            field=models.DecimalField(decimal_places=2, max_digits=21, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='serial_carroceria',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='serial_motor',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='valor_estimado',
            field=models.DecimalField(decimal_places=2, max_digits=21, null=True),
        ),
    ]
