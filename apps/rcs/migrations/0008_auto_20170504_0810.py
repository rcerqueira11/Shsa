# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0007_auto_20170426_0443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudinspeccion',
            name='editable',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='solicitudinspeccion',
            name='fk_inspector',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
