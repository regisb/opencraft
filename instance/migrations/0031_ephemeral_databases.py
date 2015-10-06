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
            name='ephemeral_databases',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
