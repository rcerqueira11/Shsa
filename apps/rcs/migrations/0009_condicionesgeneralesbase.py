# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0008_auto_20170504_0810'),
    ]

    operations = [
        migrations.CreateModel(
            name='CondicionesGeneralesBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parte', models.CharField(max_length=255)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
                ('fk_estado_vehiculo', models.ForeignKey(blank=True, to='rcs.EstadoVehiculo', null=True)),
            ],
        ),
    ]
