#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

import unittest
import mock

from mkdocs import plugins
from mkdocs import utils
from mkdocs import config


class DummyPlugin(plugins.BasePlugin):
    config_scheme = (
        ('foo', config.config_options.Type(utils.string_types, default='default foo')),
        ('bar', config.config_options.Type(int, default=0))
    )


class TestPluginClass(unittest.TestCase):

    def test_valid_plugin_options(self):

        options = {
            'foo': 'some value'
        }

        expected = {
            'foo': 'some value',
            'bar': 0
        }

        plugin = DummyPlugin(options)
        self.assertEqual(plugin.config, expected)

    def test_invalid_plugin_options(self):

        self.assertRaises(config.base.ValidationError, DummyPlugin, {'foo': 42})
        self.assertRaises(config.base.ValidationError, DummyPlugin, {'bar': 'a string'})
        # TODO: fix this... The error in the nested config is not being properly passed up
        #self.assertRaises(config.base.ValidationError, DummyPlugin, {'invalid_key': 'value'})


MockEntryPoint = mock.Mock()
MockEntryPoint.configure_mock(**{'name': 'sample', 'load.return_value': DummyPlugin})


@mock.patch('pkg_resources.iter_entry_points', return_value=[MockEntryPoint])
class TestPluginConfig(unittest.TestCase):

    def test_plugin_config_without_options(self, mock_class):

        cfg = {'plugins': ['sample']}
        option = config.config_options.Plugins()
        cfg['plugins'] = option.validate(cfg['plugins'])

        self.assertIn('sample', cfg['plugins'])
        self.assertIsInstance(cfg['plugins']['sample'], plugins.BasePlugin)
        expected = {
            'foo': 'default foo',
            'bar': 0
        }
        self.assertEqual(cfg['plugins']['sample'].config, expected)

    def test_plugin_config_with_options(self, mock_class):

        cfg = {
            'plugins': [{
                'sample': {
                    'foo': 'foo value',
                    'bar': 42
                }
            }]
        }
        option = config.config_options.Plugins()
        cfg['plugins'] = option.validate(cfg['plugins'])

        self.assertIn('sample', cfg['plugins'])
        self.assertIsInstance(cfg['plugins']['sample'], plugins.BasePlugin)
        expected = {
            'foo': 'foo value',
            'bar': 42
        }
        self.assertEqual(cfg['plugins']['sample'].config, expected)

    def test_plugin_config_uninstalled(self, mock_class):

        cfg = {'plugins': ['uninstalled']}
        option = config.config_options.Plugins()
        self.assertRaises(config.base.ValidationError, option.validate, cfg['plugins'])

    def test_plugin_config_not_list(self, mock_class):

        cfg = {'plugins': 'sample'}  # should be a list
        option = config.config_options.Plugins()
        self.assertRaises(config.base.ValidationError, option.validate, cfg['plugins'])

    def test_plugin_config_multivalue_dict(self, mock_class):

        cfg = {
            'plugins': [{
                'sample': {
                    'foo': 'foo value',
                    'bar': 42
                },
                'extra_key': 'baz'
            }]
        }
        option = config.config_options.Plugins()
        self.assertRaises(config.base.ValidationError, option.validate, cfg['plugins'])

    def test_plugin_config_not_string_or_dict(self, mock_class):

        cfg = {
            'plugins': [('not a string or dict',)]
        }
        option = config.config_options.Plugins()
        self.assertRaises(config.base.ValidationError, option.validate, cfg['plugins'])

    def test_plugin_config_options_not_dict(self, mock_class):

        cfg = {
            'plugins': [{
                'sample': 'not a dict'
            }]
        }
        option = config.config_options.Plugins()
        self.assertRaises(config.base.ValidationError, option.validate, cfg['plugins'])
