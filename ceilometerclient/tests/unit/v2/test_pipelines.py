# Copyright 2014 Hewlett-Packard Development Company, L.P.
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
import copy
import six

from ceilometerclient.apiclient import client
from ceilometerclient.apiclient import fake_client
from ceilometerclient.tests.unit import utils
import ceilometerclient.v2.pipelines

AN_PIPELINE = {
    u'name': u'test_pipeline',
    u'enabled': u'enabled',
    u'location': u'location',
    u'max_bytes': u'max_bytes',
    u'backup_count': u'5',
    u'compress': u'True',
}

UPDATED_PIPELINE = copy.deepcopy(AN_PIPELINE)
UPDATED_PIPELINE['enabled'] = 'False'
UPDATED_PIPELINE['max_bytes'] = '1000'
UPDATE_PIPELINE = copy.deepcopy(UPDATED_PIPELINE)
del UPDATE_PIPELINE['compress']

GET_PIPELINE1 = {
    'name': 'csv_sink',
    'enabled': 'False',
    'location': '/opt/cgcs/ceilometer/csv/pm.csv',
    'max_bytes': '10000000',
    'backup_count': '5',
    'compress': 'True',
}

GET_PIPELINE2 = {
    'name': 'vswitch_avg_sink',
    'enabled': 'True',
    'location': '/opt/cgcs/ceilometer/csv/vswitch.csv',
    'max_bytes': '10000000',
    'backup_count': '5',
    'compress': 'True',
}

fixtures = {
    '/v2/wrs-pipelines': {
        'GET': (
            {},
            [GET_PIPELINE1, GET_PIPELINE2]
        ),
    },

    '/v2/wrs-pipelines/csv_sink':
    {
        'GET': (
            {},
            GET_PIPELINE1
        ),
    },

    '/v2/wrs-pipelines/test_pipeline':
    {
        'GET': (
            {},
            AN_PIPELINE,
        ),
        'PUT': (
            {},
            UPDATED_PIPELINE,
        ),
    },
}


class PipelineManagerTest(utils.BaseTestCase):

    def setUp(self):
        super(PipelineManagerTest, self).setUp()
        self.http_client = fake_client.FakeHTTPClient(fixtures=fixtures)
        self.api = client.BaseClient(self.http_client)
        self.mgr = ceilometerclient.v2.pipelines.PipelineManager(self.api)

    def test_list_all(self):
        pipelines = list(self.mgr.list())
        expect = [
            'GET', '/v2/wrs-pipelines'
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(len(pipelines), 2)
        self.assertEqual(pipelines[0].name, 'csv_sink')
        self.assertEqual(pipelines[1].name, 'vswitch_avg_sink')

    def test_list_one(self):
        pipeline = self.mgr.get('csv_sink')
        expect = [
            'GET', '/v2/wrs-pipelines/csv_sink'
        ]
        self.http_client.assert_called(*expect)
        self.assertIsNotNone(pipeline)
        self.assertEqual(pipeline.location, '/opt/cgcs/ceilometer/csv/pm.csv')

    def test_get_from_pipeline_class(self):
        pipeline = self.mgr.get(GET_PIPELINE1['name'])
        self.assertIsNotNone(pipeline)
        expect = [
            'GET', '/v2/wrs-pipelines/csv_sink'
        ]
        self.http_client.assert_called(*expect)
        self.assertEqual(GET_PIPELINE1, pipeline.to_dict())

    def test_update(self):
        pipeline = self.mgr.update('test_pipeline', **UPDATE_PIPELINE)
        expect_get = [
            'GET', '/v2/wrs-pipelines/test_pipeline'
        ]
        expect_put = [
            'PUT', '/v2/wrs-pipelines/test_pipeline', UPDATED_PIPELINE
        ]
        self.http_client.assert_called(*expect_get, pos=0)
        self.http_client.assert_called(*expect_put, pos=1)
        self.assertIsNotNone(pipeline)
        self.assertEqual(pipeline.name, 'test_pipeline')
        for (key, value) in six.iteritems(UPDATED_PIPELINE):
            self.assertEqual(getattr(pipeline, key), value)
