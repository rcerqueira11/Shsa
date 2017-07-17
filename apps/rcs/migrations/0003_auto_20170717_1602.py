# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-17 16:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0002_auto_20170717_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiculo',
            name='fk_marca',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rcs.MarcaVehiculo'),
        ),
        migrations.AlterField(
            model_name='vehiculo',
            name='fk_modelo',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rcs.ModeloVehiculo'),
        ),
    ]
