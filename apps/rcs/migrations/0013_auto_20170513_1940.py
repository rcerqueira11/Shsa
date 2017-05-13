# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0012_auto_20170513_1935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentospresentadosbase',
            name='recibido',
            field=models.BooleanField(default=True),
        ),
    ]
