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
#    Copyright (c) 2013-2014 Wind River Systems, Inc.
#

from ceilometerclient.common import base
from ceilometerclient.common import utils
from ceilometerclient.v2 import options


UPDATABLE_ATTRIBUTES = [
    'enabled',
    'location',
    'max_bytes',
    'backup_count',
    'compress'
]

CREATION_ATTRIBUTES = UPDATABLE_ATTRIBUTES + ['name', ]


class Pipeline(base.Resource):
    def __repr__(self):
        return "<Pipeline %s>" % self._info


class PipelineManager(base.Manager):
    resource_class = Pipeline

    @staticmethod
    def _path(pipeline_name=None):
        return ('/v2/wrs-pipelines/%s' % pipeline_name
                if pipeline_name else '/v2/wrs-pipelines')

    def get(self, pipeline_name):
        try:
            return self._list(self._path(pipeline_name), expect_single=True)[0]
        except IndexError:
            return None

    def list(self, pipeline_name=None, q=None, limit=None):
        path = self._path(pipeline_name)
        params = ['limit=%s' % str(limit)] if limit else None
        return self._list(options.build_url(path, q, params))

    def create(self, **kwargs):
        new = dict((key, value) for (key, value) in kwargs.items()
                   if key in CREATION_ATTRIBUTES)
        url = self._path(pipeline_name=kwargs['pipeline_name'])
        body = self.api.post(url, json=[new]).json()
        if body:
            return [Pipeline(self, b) for b in body]

    def update(self, pipeline_name, **kwargs):
        updated = self.get(pipeline_name).to_dict()
        kwargs = dict((k, v) for k, v in kwargs.items()
                      if k in updated and k in UPDATABLE_ATTRIBUTES)
        utils.merge_nested_dict(updated, kwargs, depth=1)
        return self._update(self._path(pipeline_name), updated)
