# Copyright 2012 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
#
# Copyright (c) 2016 Wind River Systems, Inc.
#
from ceilometerclient.apiclient import client
from ceilometerclient.apiclient import fake_client
from ceilometerclient.tests.unit import utils
import ceilometerclient.v2.metertypes

fixtures = {
    '/v2/wrs-metertypes': {
        'GET': (
            {},
            [
                {
                    'name': 'image.size',
                    'type': 'gauge',
                    'unit': 'B',
                },
                {
                    'name': 'platform.cpu.util',
                    'type': 'delta',
                    'unit': '%',
                },
            ]
        ),
    },
}


class MeterTypeManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(MeterTypeManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = ceilometerclient.v2.metertypes.MeterTypeManager(self.api)

    def test_list_all(self):
        metertypes = list(self.mgr.list())
        expect = [
            'GET', '/v2/wrs-metertypes'
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(len(metertypes), 2)
        self.assertEqual(metertypes[0].name, 'image.size')
        self.assertEqual(metertypes[1].name, 'platform.cpu.util')
