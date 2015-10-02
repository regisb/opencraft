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
Worker tasks - Tests
"""

# Imports #####################################################################

import yaml

from django.test import override_settings
from mock import patch

from instance import tasks
from instance.models.instance import OpenEdXInstance
from instance.tests.base import TestCase
from instance.tests.factories.pr import PRFactory
from instance.tests.models.factories.instance import OpenEdXInstanceFactory


# Tests #######################################################################

# Factory boy doesn't properly support pylint+django
#pylint: disable=no-member

class TasksTestCase(TestCase):
    """
    Test cases for worker tasks
    """
    @patch('instance.models.instance.OpenEdXInstance.provision', autospec=True)
    def test_provision_sandbox_instance(self, mock_instance_provision):
        """
        Create sandbox instance
        """
        instance = OpenEdXInstanceFactory()
        tasks.provision_instance(instance.pk)
        self.assertEqual(mock_instance_provision.call_count, 1)
        self.assertEqual(mock_instance_provision.mock_calls[0][1][0].pk, instance.pk)

    @patch('instance.models.instance.github.get_commit_id_from_ref')
    @patch('instance.tasks.provision_instance')
    @patch('instance.tasks.get_pr_list_from_username')
    @patch('instance.tasks.get_username_list_from_team')
    def test_watch_pr_new(self, mock_get_username_list, mock_get_pr_list_from_username,
                          mock_provision_instance, mock_get_commit_id_from_ref):
        """
        New PR created on the watched repo
        """
        mock_get_username_list.return_value = ['itsjeyd']
        settings = 'WATCH: true\r\nDATABASE_URL: mysql://db.opencraft.com\r\nMONGO_URL: mongo://mongo.opencraft.com\r\n'
        pr = PRFactory(
            number=234,
            fork_name='watched/fork',
            branch_name='watch-branch',
            title='Watched PR title which is very long',
            username='bradenmacdonald',
            body='Hello watcher!\n- - -\r\n**Settings**\r\n```\r\n' + settings + '```\r\nMore...',
        )
        mock_get_pr_list_from_username.return_value = [pr]
        mock_get_commit_id_from_ref.return_value = '7' * 40

        tasks.watch_pr()
        self.assertEqual(mock_provision_instance.call_count, 1)
        instance = OpenEdXInstance.objects.get(pk=mock_provision_instance.mock_calls[0][1][0])
        self.assertEqual(instance.sub_domain, 'pr234.sandbox')
        self.assertEqual(instance.fork_name, 'watched/fork')
        self.assertEqual(instance.github_pr_number, 234)
        self.assertEqual(instance.branch_name, 'watch-branch')
        self.assertEqual(instance.database_url, 'mysql://db.opencraft.com')
        self.assertEqual(instance.mongo_url, 'mongo://mongo.opencraft.com')
        self.assertEqual(yaml.load(instance.ansible_extra_settings), {'WATCH': True})
        self.assertEqual(
            instance.name,
            'PR#234: Watched PR title which ... (bradenmacdonald) - watched/watch-branch (7777777)')

    @override_settings(INSTANCE_DATABASE_URL='mysql://db.opencraft.com',
                       INSTANCE_MONGO_URL='mongo://mongo.opencraft.com')
    @patch('instance.models.instance.github.get_commit_id_from_ref')
    @patch('instance.tasks.provision_instance')
    @patch('instance.tasks.get_pr_list_from_username')
    @patch('instance.tasks.get_username_list_from_team')
    def test_watch_pr_ephemeral_databases(self, mock_get_username_list,
                                          mock_get_pr_list_from_username,
                                          mock_provision_instance,
                                          mock_get_commit_id_from_ref):
        """
        Asking for ephemeral databases in the PR should unset external
        database settings, even if the default is to use external databases
        """
        mock_get_username_list.return_value = ['itsjeyd']
        settings = 'EPHEMERAL_DATABASES: yes\r\n'
        pr = PRFactory(
            body='Hello watcher!\n- - -\r\n**Settings**\r\n```\r\n' + settings + '```\r\nMore...',
        )
        mock_get_pr_list_from_username.return_value = [pr]
        mock_get_commit_id_from_ref.return_value = '7' * 40

        tasks.watch_pr()
        self.assertEqual(mock_provision_instance.call_count, 1)
        instance = OpenEdXInstance.objects.get(pk=mock_provision_instance.mock_calls[0][1][0])
        self.assertTrue(instance.ephemeral_databases)
        self.assertFalse(instance.database_url)
        self.assertFalse(instance.mongo_url)
