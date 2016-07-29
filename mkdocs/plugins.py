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
    """

    config_scheme = ()
    config = {}

    def load_config(self, options):
        """ Load config from a dict of options. Returns a tuple of (errors, warnings)."""

        self.config = Config(schema=self.config_scheme)
        self.config.load_dict(options)

        return self.config.validate()
