# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0013_auto_20170513_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentospresentadosbase',
            name='recibido',
            field=models.BooleanField(default=False),
        ),
    ]
