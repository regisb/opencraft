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
Test factories
"""

# Imports #####################################################################

import factory

from instance import github


# Classes #####################################################################

class PRFactory(factory.Factory):
    """
    Factory for PR instances
    """
    class Meta: #pylint: disable=missing-docstring
        model = github.PR

    number = factory.Sequence(int)
    fork_name = 'edx/edx-platform'
    branch_name = 'master'
    title = factory.Sequence('PR #{}'.format)
    username = 'edx'
    body = ''
