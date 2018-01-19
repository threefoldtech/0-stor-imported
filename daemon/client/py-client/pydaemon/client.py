# Copyright (C) 2017-2018 GIG Technology NV and Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import grpc

from . import namespace
from . import file
from . import data
from . import metadata


class Client:
    def __init__(self, address='172.0.0.1:8080'):
        '''
        Create a new client instance

        :param address: address of the client daemon
        '''
        channel = grpc.insecure_channel(address)

        # initialize stubs
        self._namespace = namespace.Namespace(channel)
        self._file = file.File(channel)
        self._data = data.Data(channel)
        self._metadata = metadata.Metadata(channel)

    @property
    def namespace(self):
        return self._namespace

    @property
    def file(self):
        return self._file

    @property
    def data(self):
        return self._data

    @property
    def metadata(self):
        return self._metadata
