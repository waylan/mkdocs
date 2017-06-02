import unittest
import os

from mkdocs.structure.pages import Page
from mkdocs.structure.files import File, Files
from mkdocs.tests.base import load_config, dedent

class PageTests(unittest.TestCase):
    
    def test_homepage(self):
        docs_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '../integration/subpages/docs'
        )
        cfg = load_config(docs_dir=docs_dir)
        fl = File(cfg['docs_dir'], 'index.md')
        pg = Page('Foo', fl, cfg)
        self.assertEqual(pg.abs_url, '')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertTrue(pg.is_homepage)
        self.assertTrue(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('## Test'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])
    
    def test_nested_index_page(self):
        docs_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '../integration/subpages/docs'
        )
        cfg = load_config(docs_dir=docs_dir)
        fl = File(cfg['docs_dir'], 'sub1/index.md')
        pg = Page('Foo', fl, cfg)
        pg.parent = 'foo'
        self.assertEqual(pg.abs_url, 'sub1/')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertTrue(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertFalse(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('# Test'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, 'foo')
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])
    
    def test_nested_nonindex_page(self):
        docs_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '../integration/subpages/docs'
        )
        cfg = load_config(docs_dir=docs_dir)
        fl = File(cfg['docs_dir'], 'sub1/non-index.md')
        pg = Page('Foo', fl, cfg)
        pg.parent = 'foo'
        self.assertEqual(pg.abs_url, 'sub1/non-index/')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertFalse(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('# Test'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, 'foo')
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])
    
    def test_page_defaults(self):
        cfg = load_config()
        fl = File(cfg['docs_dir'], 'testing.md')
        pg = Page('Foo', fl, cfg)
        self.assertRegexpMatches(pg.update_date, r'\d{4}-\d{2}-\d{2}')
        self.assertEqual(pg.abs_url, 'testing/')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('# Welcome to MkDocs\n'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])
    
    def test_page_no_directory_url(self):
        cfg = load_config(use_directory_urls=False)
        fl = File(cfg['docs_dir'], 'testing.md')
        pg = Page('Foo', fl, cfg)
        self.assertEqual(pg.abs_url, 'testing/index.html')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('# Welcome to MkDocs\n'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])
    
    def test_page_canonical_url(self):
        cfg = load_config(site_url='http://example.com')
        fl = File(cfg['docs_dir'], 'testing.md')
        pg = Page('Foo', fl, cfg)
        self.assertEqual(pg.abs_url, 'testing/')
        self.assertEqual(pg.canonical_url, 'http://example.com/testing/')
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('# Welcome to MkDocs\n'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Foo')
        self.assertEqual(pg.toc, [])
    
    def test_page_title_from_markdown(self):
        cfg = load_config()
        fl = File(cfg['docs_dir'], 'testing.md')
        pg = Page(None, fl, cfg)
        self.assertEqual(pg.abs_url, 'testing/')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('# Welcome to MkDocs\n'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Welcome to MkDocs')
        self.assertEqual(pg.toc, [])
    
    def test_page_title_from_meta(self):
        docs_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '../integration/subpages/docs'
        )
        cfg = load_config(docs_dir=docs_dir)
        fl = File(cfg['docs_dir'], 'metadata.md')
        pg = Page(None, fl, cfg)
        self.assertEqual(pg.abs_url, 'metadata/')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('# Welcome to MkDocs\n'))
        self.assertEqual(pg.meta, {'title': 'A Page Title'})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'A Page Title')
        self.assertEqual(pg.toc, [])
    
    def test_page_title_from_filename(self):
        docs_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '../integration/subpages/docs'
        )
        cfg = load_config(docs_dir=docs_dir)
        fl = File(cfg['docs_dir'], 'page-title.md')
        pg = Page(None, fl, cfg)
        self.assertEqual(pg.abs_url, 'page-title/')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('Page content.\n'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Page title')
        self.assertEqual(pg.toc, [])
    
    def test_page_title_from_capitalized_filename(self):
        docs_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '../integration/subpages/docs'
        )
        cfg = load_config(docs_dir=docs_dir)
        fl = File(cfg['docs_dir'], 'pageTitle.md')
        pg = Page(None, fl, cfg)
        self.assertEqual(pg.abs_url, 'pageTitle/')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertFalse(pg.is_homepage)
        self.assertFalse(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('Page content.\n'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'pageTitle')
        self.assertEqual(pg.toc, [])
    
    def test_page_title_from_homepage_filename(self):
        docs_dir = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), '../integration/subpages/docs'
        )
        cfg = load_config(docs_dir=docs_dir)
        fl = File(cfg['docs_dir'], 'index.md')
        pg = Page(None, fl, cfg)
        self.assertEqual(pg.abs_url, '')
        self.assertEqual(pg.canonical_url, None)
        self.assertEqual(pg.edit_url, None)
        self.assertEqual(pg.file, fl)
        self.assertEqual(pg.html, None)
        self.assertTrue(pg.is_homepage)
        self.assertTrue(pg.is_index)
        self.assertTrue(pg.is_page)
        self.assertFalse(pg.is_section)
        self.assertTrue(pg.is_top_level)
        self.assertTrue(pg.markdown.startswith('## Test'))
        self.assertEqual(pg.meta, {})
        self.assertEqual(pg.next, None)
        self.assertEqual(pg.parent, None)
        self.assertEqual(pg.previous, None)
        self.assertEqual(pg.title, 'Home')
        self.assertEqual(pg.toc, [])
    
    def test_page_edit_url(self):
        configs = [
            {
                'repo_url': 'http://github.com/mkdocs/mkdocs'
            },
            {
                'repo_url': 'https://github.com/mkdocs/mkdocs/'
            }, {
                'repo_url': 'http://example.com'
            }, {
                'repo_url': 'http://example.com',
                'edit_uri': 'edit/master'
            }, {
                'repo_url': 'http://example.com/foo/',
                'edit_uri': 'edit/master/'
            }, {
                'repo_url': 'http://example.com/foo/',
                'edit_uri': '/edit/master'
            }, {
                'repo_url': 'http://example.com',
                'edit_uri': '?query=edit/master'
            }, {
                'repo_url': 'http://example.com/',
                'edit_uri': '?query=edit/master/'
            }, {
                'repo_url': 'http://example.com',
                'edit_uri': '#edit/master'
            }, {
                'repo_url': 'http://example.com',
                'edit_uri': '#edit/master/'
            }
        ]
        
        expected = [
            'http://github.com/mkdocs/mkdocs/edit/master/docs/testing.md',
            'https://github.com/mkdocs/mkdocs/edit/master/docs/testing.md',
            'http://example.com/',
            'http://example.com/edit/master/testing.md',
            'http://example.com/foo/edit/master/testing.md',
            'http://example.com/edit/master/testing.md',
            'http://example.com/?query=edit/master/testing.md',
            'http://example.com/?query=edit/master/testing.md',
            'http://example.com/#edit/master/testing.md',
            'http://example.com/#edit/master/testing.md',
        ]
        
        for i, c in enumerate(configs):
            cfg = load_config(**c)
            fl = File(cfg['docs_dir'], 'testing.md')
            pg = Page('Foo', fl, cfg)
            self.assertEqual(pg.abs_url, 'testing/')
            self.assertEqual(pg.edit_url, expected[i])

    def test_page_render(self):
        cfg = load_config()
        fl = File(cfg['docs_dir'], 'testing.md')
        pg = Page('Foo', fl, cfg)
        self.assertEqual(pg.html, None)
        self.assertEqual(pg.toc, [])
        pg.render(cfg, [fl])
        self.assertTrue(pg.html.startswith(
            '<h1 id="welcome-to-mkdocs">Welcome to MkDocs</h1>\n'
        ))
        self.assertEqual(str(pg.toc).strip(), dedent("""
            Welcome to MkDocs - #welcome-to-mkdocs
                Commands - #commands
                Project layout - #project-layout
        """))
    
    def test_missing_page(self):
        cfg = load_config()
        fl = File(cfg['docs_dir'], 'missing.md')
        self.assertRaises(IOError, Page, 'Foo', fl, cfg)


class SourceDateEpochTests(unittest.TestCase):
    
    def setUp(self):
        self.default = os.environ.get('SOURCE_DATE_EPOCH', None)
        os.environ['SOURCE_DATE_EPOCH'] = '0'
    
    def test_source_date_epoch(self):
        cfg = load_config()
        fl = File(cfg['docs_dir'], 'testing.md')
        pg = Page('Foo', fl, cfg)
        self.assertEqual(pg.update_date, '1970-01-01')
    
    def tearDown(self):
        if self.default is not None:
            os.environ['SOURCE_DATE_EPOCH'] = self.default
        else:
            del os.environ['SOURCE_DATE_EPOCH']