# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-11 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rcs', '0007_solicitudinspeccion_numero_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudinspeccion',
            name='numero_ticket',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]