import unittest
import os

from mkdocs.structure.urls import get_output_path, get_output_url, get_relative_url

class TestURLs(unittest.TestCase):
    def test_get_ouput_path(self):
        paths = [
            ('index.md',        'index.html'),
            ('README.md',       'index.html'),
            ('foo.md',          'foo/index.html'),
            ('foo/bar.md',      'foo/bar/index.html'),
            ('foo/bar/baz.md',  'foo/bar/baz/index.html'),
            ('foo.jpg',         'foo.jpg'),
            ('foo/bar.jpg',     'foo/bar.jpg'),
            ('foo/bar/baz.jpg', 'foo/bar/baz.jpg'),
        ]
        
        for src, expected in paths:
            self.assertEqual(get_output_path(src.replace('/', os.sep)), expected.replace('/', os.sep))

    def test_get_output_url(self):
        paths = [
            ('index.html',              '/'),
            ('foo/index.html',          '/foo/'),
            ('foo/bar/index.html',      '/foo/bar/'),
            ('foo/bar/baz/index.html',  '/foo/bar/baz/'),
            ('foo.html',                '/foo.html'),
            ('foo.jpg',                 '/foo.jpg'),
            ('foo/bar.jpg',             '/foo/bar.jpg'),
            ('foo/bar/baz.jpg',         '/foo/bar/baz.jpg'),
        ]
        
        for src, expected in paths:
            # Posix paths
            self.assertEqual(get_output_url(src), expected)
            # Windows paths
            self.assertEqual(get_output_url(src.replace('/', '\\')), expected)
    
    def test_get_output_url_no_directory_urls(self):
        paths = [
            ('index.html',              '/index.html'),
            ('foo/index.html',          '/foo/index.html'),
            ('foo/bar/index.html',      '/foo/bar/index.html'),
            ('foo/bar/baz/index.html',  '/foo/bar/baz/index.html'),
            ('foo.html',                '/foo.html'),
            ('foo.jpg',                 '/foo.jpg'),
            ('foo/bar.jpg',             '/foo/bar.jpg'),
            ('foo/bar/baz.jpg',         '/foo/bar/baz.jpg'),
        ]
        
        for src, expected in paths:
            # Posix paths
            self.assertEqual(get_output_url(src, False), expected)
            # Windows paths
            self.assertEqual(get_output_url(src.replace('/', '\\'), False), expected)

    def test_get_relative_url(self):
        from_paths = [
            'index.md',
            'foo/index.md',
            'foo/bar/index.md',
            'foo/bar/baz/index.md',
            'foo.md',
            'foo/bar.md',
            'foo/bar/baz.md',
        ]
        
        to_path = 'img.jpg'
        expected = [
            'img.jpg',
            '../img.jpg',
            '../../img.jpg',
            '../../../img.jpg',
            '../img.jpg',
            '../../img.jpg',
            '../../../img.jpg'
        ]
        
        for i, from_path in enumerate(from_paths):
            self.assertEqual(get_relative_url(to_path, from_path), expected[i])
            
        
        to_path = 'foo/img.jpg'
        expected = [
            'foo/img.jpg',
            'img.jpg',
            '../img.jpg',
            '../../img.jpg',
            'img.jpg',
            '../img.jpg',
            '../../img.jpg'
        ]
        
        for i, from_path in enumerate(from_paths):
            self.assertEqual(get_relative_url(to_path, from_path), expected[i])
        
        to_path = '../img.jpg'
        expected = [
            'img.jpg',
            '../img.jpg',
            '../../img.jpg',
            '../../../img.jpg',
            '../img.jpg',
            '../../img.jpg',
            '../../../img.jpg'
        ]
        
        for i, from_path in enumerate(from_paths):
            self.assertEqual(get_relative_url(to_path, from_path), expected[i])

    def test_get_relative_url_no_directory_urls(self):
        from_paths = [
            'index.md',
            'foo/index.md',
            'foo/bar/index.md',
            'foo/bar/baz/index.md',
            'foo.md',
            'foo/bar.md',
            'foo/bar/baz.md',
        ]
        
        to_path = 'img.jpg'
        expected = [
            '../img.jpg',
            '../../img.jpg',
            '../../../img.jpg',
            '../../../../img.jpg',
            '../../img.jpg',
            '../../../img.jpg',
            '../../../../img.jpg'
        ]
        
        for i, from_path in enumerate(from_paths):
            self.assertEqual(get_relative_url(to_path, from_path, False), expected[i])
        
        to_path = 'foo/img.jpg'
        expected = [
            '../foo/img.jpg',
            '../img.jpg',
            '../../img.jpg',
            '../../../img.jpg',
            '../img.jpg',
            '../../img.jpg',
            '../../../img.jpg'
        ]
        
        for i, from_path in enumerate(from_paths):
            self.assertEqual(get_relative_url(to_path, from_path, False), expected[i])
        
        to_path = '../img.jpg'
        expected = [
            '../img.jpg',
            '../../img.jpg',
            '../../../img.jpg',
            '../../../../img.jpg',
            '../../img.jpg',
            '../../../img.jpg',
            '../../../../img.jpg'
        ]
        
        for i, from_path in enumerate(from_paths):
            self.assertEqual(get_relative_url(to_path, from_path, False), expected[i])
