#!/usr/bin/python

import json

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KeystoneMiddlewareProvides(RelationBase):
    scope = scopes.GLOBAL

    @hook('{provides:keystone-middleware}-relation-joined')
    def keystone_middleware_joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.joined')
        self.set_state('{relation_name}.connected')
        self.set_state('{relation_name}.available')

    @hook('{provides:keystone-middleware}-relation-changed')
    def keystone_middleware_changed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.configured')
        if conv.get_remote('configured'):
            conv.set_state('{relation_name}.configured')
        if conv.get_remote('create-defs'):
            conv.set_state('keystone-middleware.create-defs')

    @hook('{provides:keystone-middleware}-relation-{broken, departed}')
    def keystone_middleware_departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.joined')
        conv.set_state('{relation_name}.departing')
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    def configure_principal(self, service_name=None, keystone_conf=None):
        """Send principle keystone-middleware configuration"""
        conv = self.conversation()
        relation_info = {"service_name": service_name,
                         "keystone_conf": keystone_conf
                         }
        conv.set_remote(**relation_info)
