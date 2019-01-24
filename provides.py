#!/usr/bin/python
from charms.reactive import Endpoint
from charms.reactive import set_flag, clear_flag
from charms.reactive import when
from charms.reactive import scopes


class KeystoneMiddlewareProvides(Endpoint):
    scope = scopes.GLOBAL

    @when('endpoint.{endpoint_name}.changed.release')
    @when('endpoint.keystone-middleware.joined')
    def new_release(self):
        set_flag(self.expand_name('endpoint.{endpoint_name}.new-release'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed.release'))

    @when('endpoint.keystone-middleware.changed')
    @when('endpoint.keystone-middleware.joined')
    def changed(self):
        set_flag(self.expand_name('endpoint.{endpoint_name}.connected'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.changed'))

    @when('endpoint.keystone-middleware.departed')
    def broken(self):
        clear_flag(self.expand_name('endpoint.{endpoint_name}.connected'))
        clear_flag(self.expand_name('endpoint.{endpoint_name}.departed'))

    def configure_principal(self, middleware_name, configuration):
        """Send principle keystone-middleware configuration"""
        middleware_config = {
            "keystone": {
                "/etc/keystone/keystone.conf": {
                    "sections": configuration
                }
            }
        }

        for relation in self.relations:
            relation.to_publish.update({'middleware_name': middleware_name,
                                        'subordinate_configuration': middleware_config
                                        })

    def release_version(self):
        """retrieve release version"""
        release = None
        for relation in self.relations:
            for unit in relation.units:
                release = unit.received['release']
                if release:
                    break
        return release
