# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0032_ephemeral_databases'),
    ]

    operations = [
        migrations.AddField(
            model_name='openedxinstance',
            name='database_pass',
            field=models.CharField(max_length=32, blank=True),
        ),
        migrations.AddField(
            model_name='openedxinstance',
            name='database_user',
            field=models.CharField(max_length=16, blank=True),
        ),
    ]
