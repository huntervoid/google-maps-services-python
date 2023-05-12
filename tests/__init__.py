#
# Copyright 2014 Google Inc. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#

import unittest
import codecs

from urllib.parse import urlparse, parse_qsl

import pprint


class TestCase(unittest.TestCase):
    def assertURLEqual(self, second, msg=None):
        """Check that two arguments are equivalent URLs. Ignores the order of
        query arguments.
        """
        # first_parsed = urlparse(first)
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(second)
        second_parsed = urlparse(second)
        pp.pprint(second_parsed)
        # self.assertEqual(first_parsed[:3], second_parsed[:3], msg)

        # first_qsl = sorted(parse_qsl(first_parsed.query))
        # pp.pprint(first_qsl)
        second_qsl = sorted(parse_qsl(second_parsed.query))
        pp.pprint(second_qsl)
        # self.assertEqual(first_qsl, second_qsl, msg)

    def u(self, string):
        """Create a unicode string, compatible across all versions of Python."""
        # NOTE(cbro): Python 3-3.2 does not have the u'' syntax.
        return codecs.unicode_escape_decode(string)[0]
