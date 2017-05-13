# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0010_accesoriosbase_documentospresentadosbase_mecanicabase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detallesdatos',
            name='codigo',
            field=models.CharField(max_length=255),
        ),
    ]
