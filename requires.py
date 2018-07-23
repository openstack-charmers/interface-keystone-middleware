#!/usr/bin/python
#
# Copyright 2017 Canonical Ltd
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

from charms.reactive import hook
from charms.reactive import RelationBase
from charms.reactive import scopes


class KeystoneIcoRequires(RelationBase):
    scope = scopes.GLOBAL

    @hook('{requires:keystone-ico}-relation-{joined,changed}')
    def changed(self):
        self.set_state('{relation_name}.connected')
        self.set_state('{relation_name}.available')

    @hook('{requires:keystone-ico}-relation-{departed,broken}')
    def departed(self):
        self.remove_state('{relation_name}.connected')
        self.remove_state('{relation_name}.available')

    def get_token(self):
        return self.get_remote('token-secret')
