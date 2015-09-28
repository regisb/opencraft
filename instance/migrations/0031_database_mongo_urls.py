# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0030_auto_20150927_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='openedxinstance',
            name='database_url',
            field=models.CharField(max_length=255, default='', blank=True),
        ),
        migrations.AddField(
            model_name='openedxinstance',
            name='mongo_url',
            field=models.CharField(max_length=255, default='', blank=True),
        ),
    ]
