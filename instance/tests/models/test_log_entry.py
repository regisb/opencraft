# -*- coding: utf-8 -*-
#
# OpenCraft -- tools to aid developing and hosting free software projects
# Copyright (C) 2015 OpenCraft <xavier@opencraft.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Logger models & mixins - Tests
"""

# Imports #####################################################################

from freezegun import freeze_time
from mock import patch

from instance.tests.base import TestCase
from instance.tests.models.factories.instance import OpenEdXInstanceFactory
from instance.tests.models.factories.server import OpenStackServerFactory


# Tests #######################################################################

# Factory boy doesn't properly support pylint+django
#pylint: disable=no-member

class LogEntryTestCase(TestCase):
    """
    Test cases for LoggerInstanceMixin
    """
    def test_log_entries(self):
        """
        Check `log_entries` output for combination of instance & server logs
        """
        instance = OpenEdXInstanceFactory(sub_domain='my.instance')
        server = OpenStackServerFactory(instance=instance, openstack_id='vm1_id')

        with freeze_time("2015-08-05 18:07:00"):
            instance.logger.info('Line #1, on instance')

        with freeze_time("2015-08-05 18:07:01"):
            server.logger.info('Line #2, on server')

        with freeze_time("2015-08-05 18:07:02"):
            instance.logger.debug('Line #3, on instance (debug, not published by default)')

        with freeze_time("2015-08-05 18:07:03"):
            instance.logger.info('Line #4, on instance')

        with freeze_time("2015-08-05 18:07:04"):
            instance.logger.warn('Line #5, on instance (warn)')

        with freeze_time("2015-08-05 18:07:05"):
            server.logger.info('Line #6, on server')

        with freeze_time("2015-08-05 18:07:06"):
            server.logger.critical('Line #7, exception')

        entries = instance.log_entries
        self.assertEqual(entries[0].level, "INFO")
        self.assertEqual(entries[0].created.strftime("%Y-%m-%d %H:%M:%S"), "2015-08-05 18:07:00")
        self.assertEqual(entries[0].text,
                         "instance.models.instance  | instance=my.instance | Line #1, on instance")

        self.assertEqual(entries[1].level, "INFO")
        self.assertEqual(entries[1].created.strftime("%Y-%m-%d %H:%M:%S"), "2015-08-05 18:07:01")
        self.assertEqual(entries[1].text,
                         "instance.models.server    | instance=my.instance,server=vm1_id | Line #2, on server")
        self.assertEqual(entries[2].level, "INFO")
        self.assertEqual(entries[2].created.strftime("%Y-%m-%d %H:%M:%S"), "2015-08-05 18:07:03")
        self.assertEqual(entries[2].text,
                         "instance.models.instance  | instance=my.instance | Line #4, on instance")

        self.assertEqual(entries[3].level, "WARNING")
        self.assertEqual(entries[3].created.strftime("%Y-%m-%d %H:%M:%S"), "2015-08-05 18:07:04")
        self.assertEqual(entries[3].text,
                         "instance.models.instance  | instance=my.instance | Line #5, on instance (warn)")

        self.assertEqual(entries[4].level, "INFO")
        self.assertEqual(entries[4].created.strftime("%Y-%m-%d %H:%M:%S"), "2015-08-05 18:07:05")
        self.assertEqual(entries[4].text,
                         "instance.models.server    | instance=my.instance,server=vm1_id | Line #6, on server")

        self.assertEqual(entries[5].level, "CRITICAL")
        self.assertEqual(entries[5].created.strftime("%Y-%m-%d %H:%M:%S"), "2015-08-05 18:07:06")
        self.assertEqual(entries[5].text,
                         "instance.models.server    | instance=my.instance,server=vm1_id | Line #7, exception")

    @patch('instance.logging.publish_data')
    def test_log_publish(self, mock_publish_data): #pylint: disable=no-self-use
        """
        Logger sends an event to the client on each new log entry added
        """
        instance = OpenEdXInstanceFactory(sub_domain='my.instance')
        server = OpenStackServerFactory(instance=instance, openstack_id='vm1_id')

        with freeze_time("2015-09-21 21:07:00"):
            instance.logger.info('Text the client should see')

        mock_publish_data.assert_called_with('log', {
            'log_entry': {
                'created': '2015-09-21T21:07:00Z',
                'level': 'INFO',
                'text': 'instance.models.instance  | instance=my.instance | Text the client should see',
            },
            'type': 'instance_log',
            'instance_id': instance.pk,
        })

        with freeze_time("2015-09-21 21:07:01"):
            server.logger.info('Text the client should also see, with unicode «ταБЬℓσ»')

        mock_publish_data.assert_called_with('log', {
            'log_entry': {
                'created': '2015-09-21T21:07:01Z',
                'level': 'INFO',
                'text': ('instance.models.server    | instance=my.instance,server=vm1_id | Text the client '
                         'should also see, with unicode «ταБЬℓσ»'),
            },
            'type': 'instance_log',
            'instance_id': instance.pk,
            'server_id': server.pk,
        })
