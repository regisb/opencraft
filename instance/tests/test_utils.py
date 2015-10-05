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
Utils module - Tests
"""

# Imports #####################################################################

from tempfile import NamedTemporaryFile

from instance.tests.base import TestCase
from instance.utils import read_files


# Tests #######################################################################

class UtilsTestCase(TestCase):
    """
    Test cases for functions in the utils module
    """
    def test_read_files(self):
        """
        Ensure that the lines read are in the order they were written
        """
        with NamedTemporaryFile() as wfile1:
            with NamedTemporaryFile() as wfile2:

                rfile1 = open(wfile1.name, "rb")
                rfile2 = open(wfile2.name, "rb")
                lines = read_files(rfile1, rfile2)

                wfile1.write(b"FILE1,LINE1\n")
                wfile2.write(b"FILE2,LINE1\n")
                wfile1.write(b"FILE1,LINE2\n")
                wfile2.write(b"FILE2,LINE2\n")
                wfile2.write(b"FILE2,LINE3\n")

                wfile1.flush()
                wfile2.flush()

                self.assertEqual(next(lines), (rfile1, b"FILE1,LINE1\n"))
                self.assertEqual(next(lines), (rfile2, b"FILE2,LINE1\n"))
                self.assertEqual(next(lines), (rfile1, b"FILE1,LINE2\n"))
                self.assertEqual(next(lines), (rfile2, b"FILE2,LINE2\n"))
                self.assertEqual(next(lines), (rfile2, b"FILE2,LINE3\n"))
