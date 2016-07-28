# coding: utf-8

"""
Implements the plugin API for MkDocs.

"""

from __future__ import unicode_literals

import pkg_resources
import logging

from mkdocs.config.base import Config, ValidationError


log = logging.getLogger('mkdocs.plugins')


def get_plugins():
    """ Return a dict of all installed Plugins by name. """

    plugins = pkg_resources.iter_entry_points(group='mkdocs.plugins')

    return dict((plugin.name, plugin) for plugin in plugins)


class BasePlugin(object):
    """
    Plugin base class.

    All plugins should subclass this class.

    Accepts `options` as a dict of configuration options which are validated
    against the `config_scheme` defined on the class.
    """

    config_scheme = ()
    config = {}

    def __init__(self, options):
        self._load_config(options)

    def _load_config(self, options):
        """ Load config from a dict of options. """

        self.config = Config(schema=self.config_scheme)
        self.config.load_dict(options)

        errors, warnings = self.config.validate()

        # This is a nested config, so raise the errors to be caught by the parent config
        for config_name, warning in warnings:
            # TODO: perhaps do something different with warnings
            log.warning("Plugin value: '%s'. Warning: %s", config_name, warning)

        for config_name, error in errors:
            raise ValidationError("Plugin value: '%s'. Error: %s", config_name, error)


