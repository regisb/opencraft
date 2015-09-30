# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('instance', '0024_auto_20150911_2304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='openstackserver',
            name='status',
            field=models.CharField(choices=[('new', 'New - Not yet loaded'), ('started', 'Started - Running but not active yet'), ('active', 'Active - Running but not booted yet'), ('booted', 'Booted - Booted but not ready to be added to the application'), ('provisioned', 'Provisioned - Provisioning is completed'), ('provisioning_failure', 'Provisioning failure - Error during provisioning'), ('rebooting', 'Rebooting - Reboot in progress, to apply changes from provisioning'), ('ready', 'Ready - Rebooted and ready to add to the application'), ('live', 'Live - Is actively used in the application and/or accessed by users'), ('stopping', 'Stopping - Stopping temporarily'), ('stopped', 'Stopped - Stopped temporarily'), ('terminating', 'Terminating - Stopping forever'), ('terminated', 'Terminated - Stopped forever')], default='new', max_length=20, db_index=True),
        ),
    ]
