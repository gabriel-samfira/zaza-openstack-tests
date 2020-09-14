# Copyright 2020 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import zaza.openstack.charm_tests.test_utils as test_utils

import unit_tests.utils as ut_utils


class TestBaseCharmTest(unittest.TestCase):

    def test_get_my_tests_options(self):

        class FakeTest(test_utils.BaseCharmTest):

            def method(self, test_config):
                self.test_config = test_config
                return self.get_my_tests_options('aKey', 'aDefault')

        f = FakeTest()
        self.assertEquals(f.method({}), 'aDefault')
        self.assertEquals(f.method({
            'tests_options': {
                'unit_tests.charm_tests.test_utils.'
                'FakeTest.method.aKey': 'aValue',
            },
        }), 'aValue')


class TestOpenStackBaseTest(ut_utils.BaseTestCase):

    def test_setUpClass(self):
        self.patch_object(test_utils.openstack_utils, 'get_cacert')
        self.patch_object(test_utils.openstack_utils,
                          'get_overcloud_keystone_session')
        self.patch_object(test_utils.BaseCharmTest, 'setUpClass')

        class MyTestClass(test_utils.OpenStackBaseTest):
            model_name = 'deadbeef'

        MyTestClass.setUpClass('foo', 'bar')
        self.setUpClass.assert_called_with('foo', 'bar')
