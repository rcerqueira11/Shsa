# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0004_estadovehiculo_clase'),
    ]

    operations = [
        migrations.RenameField(
            model_name='accesoriosvehiculo',
            old_name='comentario',
            new_name='observacion',
        ),
        migrations.RenameField(
            model_name='condicionesgeneralesvehiculo',
            old_name='comentario',
            new_name='observacion',
        ),
        migrations.RenameField(
            model_name='mecanicavehiculo',
            old_name='comentario',
            new_name='observacion',
        ),
    ]
