# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import utils.HelpMethods.helpers
from django.conf import settings
import utils.validate_files


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='AccesoriosVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accesorio', models.CharField(max_length=255)),
                ('existe', models.BooleanField(default=True)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CondicionesGeneralesBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parte', models.CharField(max_length=255)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='CondicionesGeneralesVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parte', models.CharField(max_length=255)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DetallesDatos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pieza', models.CharField(max_length=255)),
                ('tipo_dano', models.CharField(max_length=255, null=True)),
                ('costo_aproximado', models.DecimalField(null=True, max_digits=21, decimal_places=2)),
                ('codigo', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentosPresentados',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('recibido', models.BooleanField(default=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentosPresentadosBase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('recibido', models.BooleanField(default=False)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoSolicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EstadoVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
                ('clase', models.CharField(max_length=255, null=True)),
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
        migrations.CreateModel(
            name='MecanicaVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parte', models.CharField(max_length=255)),
                ('observacion', models.TextField(null=True, blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
                ('fk_estado_vehiculo', models.ForeignKey(blank=True, to='rcs.EstadoVehiculo', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MotivoSolicitud',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('motivo', models.CharField(max_length=255)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SolicitudInspeccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('siendo_verificada', models.IntegerField(null=True, blank=True)),
                ('editable', models.BooleanField(default=True)),
                ('fecha_creacion', models.DateTimeField(auto_now=True, verbose_name=[b'%d/%m/%Y'], null=True)),
                ('observaciones', models.TextField(null=True, blank=True)),
                ('ruta', utils.validate_files.ContentTypeRestrictedFileField(max_length=500, null=True, upload_to=utils.HelpMethods.helpers.get_file_path_solicitud, blank=True)),
                ('fk_estado_solicitud', models.ForeignKey(default=1, to='rcs.EstadoSolicitud')),
                ('fk_inspector', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('fk_motivo_solicitud', models.ForeignKey(to='rcs.MotivoSolicitud')),
            ],
        ),
        migrations.CreateModel(
            name='TipoManejo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TipoVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='TitularVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('cedula', models.CharField(unique=True, max_length=255)),
                ('telefono', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrajoVehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('cedula', models.CharField(unique=True, max_length=255)),
                ('parentesco', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placa', models.CharField(unique=True, max_length=255)),
                ('cap_puestos', models.IntegerField(null=True)),
                ('cilindros', models.CharField(max_length=255, null=True)),
                ('peso', models.DecimalField(null=True, max_digits=21, decimal_places=2)),
                ('color', models.CharField(max_length=255, null=True)),
                ('kilometraje', models.CharField(max_length=255, null=True)),
                ('serial_carroceria', models.CharField(max_length=255, null=True)),
                ('serial_motor', models.CharField(max_length=255, null=True)),
                ('valor_estimado', models.DecimalField(null=True, max_digits=21, decimal_places=2)),
                ('modelo', models.CharField(max_length=255, null=True)),
                ('marca', models.CharField(max_length=255, null=True)),
                ('anho', models.IntegerField(null=True)),
                ('accesorios_vehiculo', models.ManyToManyField(to='rcs.AccesoriosVehiculo')),
                ('condiciones_generales_vehiculo', models.ManyToManyField(to='rcs.CondicionesGeneralesVehiculo')),
                ('detalles_datos', models.ManyToManyField(to='rcs.DetallesDatos')),
                ('documentos_presentados', models.ManyToManyField(to='rcs.DocumentosPresentados')),
                ('fk_inspector', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
                ('fk_tipo_manejo', models.ForeignKey(to='rcs.TipoManejo', null=True)),
                ('fk_tipo_vehiculo', models.ForeignKey(to='rcs.TipoVehiculo', null=True)),
                ('fk_titular_vehiculo', models.ForeignKey(to='rcs.TitularVehiculo')),
                ('fk_trajo_vehiculo', models.ForeignKey(blank=True, to='rcs.TrajoVehiculo', null=True)),
                ('mecanica_vehiculo', models.ManyToManyField(to='rcs.MecanicaVehiculo')),
            ],
        ),
        migrations.AddField(
            model_name='solicitudinspeccion',
            name='fk_titular_vehiculo',
            field=models.ForeignKey(to='rcs.TitularVehiculo'),
        ),
        migrations.AddField(
            model_name='solicitudinspeccion',
            name='fk_vehiculo',
            field=models.OneToOneField(to='rcs.Vehiculo'),
        ),
        migrations.AddField(
            model_name='condicionesgeneralesvehiculo',
            name='fk_estado_vehiculo',
            field=models.ForeignKey(blank=True, to='rcs.EstadoVehiculo', null=True),
        ),
        migrations.AddField(
            model_name='condicionesgeneralesbase',
            name='fk_estado_vehiculo',
            field=models.ForeignKey(blank=True, to='rcs.EstadoVehiculo', null=True),
        ),
    ]
