# coding: utf-8

from __future__ import unicode_literals

import os
import logging
from mkdocs import utils
from mkdocs.commands.build import build_template
from mkdocs.plugins import BasePlugin

from .search_index import SearchIndex

log = logging.getLogger(__name__)


class SearchPlugin(BasePlugin):
    """ Add a search feature to MkDocs. """

    def on_post_config(self, config, **kwargs):
        "Add plugin template dir to list of template dirs."
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
        # Insert after `theme` and before user's `theme_dir`
        config['theme_dir'].insert(1, path)
        return config

    def on_pre_build(self, env, config, site_navigation, **kwargs):
        "Save a reference to some variables for later use."
        self.env = env
        self.site_navigation = site_navigation
        self.search_index = SearchIndex()

    def on_pre_template(self, context, config, **kwargs):
        "Add page to search index."
        self.search_index.add_entry_from_context(context['page'])

    def on_post_build(self, config, **kwargs):
        "Build search index."

        if not build_template('search.html', self.env, config, self.site_navigation):
            log.debug("Search is enabled but the theme doesn't contain a "
                      "search.html file. Assuming the theme implements search "
                      "within a modal.")

        search_index = self.search_index.generate_search_index()
        json_output_path = os.path.join(config['site_dir'], 'search', 'search_index.json')
        utils.write_file(search_index.encode('utf-8'), json_output_path)
