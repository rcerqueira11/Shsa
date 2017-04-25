# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0005_auto_20170425_0231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudinspeccion',
            name='siendo_verificada',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
