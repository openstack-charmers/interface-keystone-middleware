#!/usr/bin/python

import json

from charms.reactive import RelationBase
from charms.reactive import hook
from charms.reactive import scopes


class KeystoneIcoProvides(RelationBase):

    scope = scopes.GLOBAL

    @hook('{provides:keystone-ico}-relation-joined')
    def keystone_ico_joined(self):
        conv = self.conversation()
        conv.set_state('{relation_name}.joined')
        self.set_state('{relation_name}.connected')
        self.set_state('{relation_name}.available')

    @hook('{provides:keystone-ico}-relation-changed')
    def keystone_ico_changed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.configured')
        if conv.get_remote('configured'):
            conv.set_state('{relation_name}.configured')
        if conv.get_remote('create-defs'):
            conv.set_state('keystone-ico.create-defs')

    @hook('{provides:keystone-ico}-relation-{broken, departed}')
    def keystone_ico_departed(self):
        conv = self.conversation()
        conv.remove_state('{relation_name}.joined')
        conv.set_state('{relation_name}.departing')
        self.remove_state('{relation_name}.available')
        self.remove_state('{relation_name}.connected')

    def configure_principal(self, token=None):
        """Send principle keystone-ico token"""
        conv = self.conversation()
        relation_info = {
            'token-secret': token,
        }
        conv.set_remote(**relation_info)
