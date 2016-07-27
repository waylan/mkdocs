# coding: utf-8

"""
Implements the plugin API for MkDocs.

"""

from __future__ import unicode_literals

import pkg_resources
from mkdocs inport exceptions
from mkdocs.config import Config


def get_plugins():
    """ Return a dict of all installed Plugins by name. """

    plugins = pkg_resources.iter_entry_points(group='mkdocs.plugins')

    return dict((plugin.name, plugin) for plugin in plugins)


def get_plugin_names():
    """ Return an iterable of all installed plugin names. """

    return get_plugins().keys()


def get_plugin(name):
    """ Return a Plugin class of the given name. """

    # TODO: perhaps add some error handling here for pretty error messages
    return get_plugins()[name].load()


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

    def _load_config(options):
        """ Load config from a dict of options. """

        self.config = Config(schema=self.config_scheme)
        self.config.load_dict(options)

        errors, warnings = self.config.validate()

        for config_name, warning in warnings:
            log.warning("Config value: '%s'. Warning: %s", config_name, warning)

        for config_name, error in errors:
            log.error("Config value: '%s'. Error: %s", config_name, error)

        if len(errors) > 0:
            raise exceptions.ConfigurationError(
                "Aborted with {0} Configuration Errors!".format(len(errors))
            )
