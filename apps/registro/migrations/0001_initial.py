# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('username', models.CharField(unique=True, max_length=255)),
                ('nombre', models.CharField(max_length=255)),
                ('apellido', models.CharField(max_length=255)),
                ('cedula', models.CharField(unique=True, max_length=255)),
                ('correo_electronico', models.EmailField(unique=True, max_length=255, blank=True)),
                ('intentos_login', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255, blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoUsuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField(blank=True)),
                ('codigo', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='usuario',
            name='fk_status',
            field=models.ForeignKey(db_column=b'fk_status', default=1, to='registro.Status'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='fk_tipo_usuario',
            field=models.ForeignKey(to='registro.TipoUsuario'),
        ),
    ]
