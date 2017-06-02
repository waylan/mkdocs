from __future__ import unicode_literals

from mkdocs.structure.toc import get_toc
from mkdocs.structure.urls import get_relative_url
from mkdocs.utils import meta, urlparse, urlunparse, urljoin, get_markdown_title

from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import AMP_SUBSTITUTE
import markdown
import datetime
import logging
import io
import os


log = logging.getLogger(__name__)


@meta.transformer()
def default(value):
    """ By default, return all meta values as strings. """
    return ' '.join(value)


class Page(object):
    def __init__(self, title, file, config):
        self.file = file

        # Navigation attributes
        self.parent = None
        self.previous = None
        self.next = None

        self.is_section = False
        self.is_page = True
        # self.active = False

        # Support SOURCE_DATE_EPOCH environment variable for "reproducible" builds.
        # See https://reproducible-builds.org/specs/source-date-epoch/
        if 'SOURCE_DATE_EPOCH' in os.environ:
            self.update_date = datetime.datetime.utcfromtimestamp(
                int(os.environ['SOURCE_DATE_EPOCH'])
            ).strftime("%Y-%m-%d")
        else:
            self.update_date = datetime.datetime.now().strftime("%Y-%m-%d")

        self._set_abs_url(config.get('use_directory_urls', None))
        self._set_canonical_url(config.get('site_url', None))
        self._set_edit_url(config.get('repo_url', None), config.get('edit_uri', None))
        self._load_markdown()
        self._set_title(title)

        # Placeholders to be filled in later in the build process.
        self.html = None
        self.toc = []

    @property
    def is_index(self):
        return self.file.root == 'index'

    @property
    def is_top_level(self):
        return self.parent is None

    @property
    def is_homepage(self):
        return self.is_top_level and self.is_index

    def _set_abs_url(self, use_directory_urls):
        url = self.file.output_path.replace('\\', '/')
        if use_directory_urls:
            self.abs_url = url[:-len('index.html')]
        else:
            self.abs_url = url

    def _set_canonical_url(self, base):
        if base:
            if not base.endswith('/'):
                base += '/'
            self.canonical_url = urljoin(base, self.abs_url.lstrip('/'))
        else:
            self.canonical_url = None

    def _set_edit_url(self, repo_url, edit_uri):
        if repo_url:
            if not repo_url.endswith('/'):
                repo_url += '/'
            if not edit_uri:
                self.edit_url = repo_url
            else:
                input_path_url = self.file.input_path.replace('\\', '/')
                if not edit_uri.endswith('/'):
                    edit_uri += '/'
                self.edit_url = urljoin(repo_url, edit_uri + input_path_url)
        else:
            self.edit_url = None

    def _load_markdown(self):
        try:
            input_content = io.open(self.file.full_input_path, 'r', encoding='utf-8').read()
        except IOError:
            log.error('file not found: %s', self.file.full_input_path)
            raise

        self.markdown, self.meta = meta.get_data(input_content)

    def _set_title(self, title):
        """
        Set the title for a Markdown document.

        Check these in order and use the first that returns a valid title:
        - value provided on init (passed in from config)
        - value of metadata 'title'
        - content of the first H1 in Markdown content
        - convert filename to title
        """
        if title is not None:
            self.title = title
            return

        if 'title' in self.meta:
            self.title = self.meta['title']
            return

        title = get_markdown_title(self.markdown)

        if title is None:
            if self.is_homepage:
                title = 'Home'
            else:
                title = self.file.root.replace('-', ' ').replace('_', ' ')
                # Capitalize if the filename was all lowercase, otherwise leave it as-is.
                if title.lower() == title:
                    title = title.capitalize()

        self.title = title

    def render(self, config, files):
        """
        Convert the Markdown source file to HTML as per the config.
        """

        extensions = [
            _RelativePathExtension(self.file, files, config['strict'])
        ] + config['markdown_extensions']

        md = markdown.Markdown(
            extensions=extensions,
            extension_configs=config['mdx_configs'] or {}
        )
        self.html = md.convert(self.markdown)
        self.toc = get_toc(getattr(md, 'toc', ''))


def build_pages(files):
    pages = []
    for file in files.documentation_pages():
        md = markdown.Markdown(
            extensions=[
                _RelativePathExtension(file, files, strict=False),
                'meta', 'toc', 'tables', 'fenced_code'
            ],
        )
        file.page.build(md)
    return pages


def _path_to_url(url, file, files, strict):
    scheme, netloc, path, params, query, fragment = urlparse(url)

    if scheme or netloc or not path or AMP_SUBSTITUTE in url:
        # Ignore URLs unless they are a relative link to a source file.
        # AMP_SUBSTITUTE is used internally by Markdown only for email.
        return url

    # Determine the filepath of the target.
    target_path = os.path.join(os.path.dirname(file.input_path), path)
    target_path = os.path.normpath(target_path).lstrip('/')

    # Validate that the target exists.
    if target_path not in files.input_paths:
        # TODO: This should be a warning.
        # TODO: We could rephrase this for img links:
        #       'contains an image link'
        # TODO: We could rephrase this for non-markdown targets:
        #       'does not exist in either the docs or theme directories'
        print (
            "Documentation file '%s' contains a link to '%s' which "
            "does not exist in the docs directory."
            % (file.input_path, target_path)
        )

    path = get_relative_url(to_path=target_path, from_path=file.input_path)
    components = (scheme, netloc, path, params, query, fragment)
    return urlunparse(components)


class _RelativePathTreeprocessor(Treeprocessor):
    def __init__(self, file, files, strict):
        self.file = file
        self.files = files
        self.strict = strict

    def run(self, root):
        """
        Update urls on anchors and images to make them relative

        Iterates through the full document tree looking for specific
        tags and then makes them relative based on the site navigation
        """
        for element in root.iter():
            if element.tag == 'a':
                key = 'href'
            elif element.tag == 'img':
                key = 'src'
            else:
                continue

            url = element.get(key)
            new_url = _path_to_url(url, self.file, self.files, self.strict)
            element.set(key, new_url)

        return root


class _RelativePathExtension(Extension):
    """
    The Extension class is what we pass to markdown, it then
    registers the Treeprocessor.
    """

    def __init__(self, file, files, strict):
        self.file = file
        self.files = files
        self.strict = strict

    def extendMarkdown(self, md, md_globals):
        relpath = _RelativePathTreeprocessor(self.file, self.files, self.strict)
        md.treeprocessors.add("relpath", relpath, "_end")
