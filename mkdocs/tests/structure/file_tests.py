import unittest
import os
import tempfile
import shutil

from mkdocs.structure.files import Files, File, get_files, sort_files, _filter_paths

class TestFiles(unittest.TestCase):

    def test_sort_files(self):
        self.assertEqual(
            sort_files(['b.md', 'bb.md', 'a.md', 'index.md', 'aa.md']),
            ['index.md', 'a.md', 'aa.md', 'b.md', 'bb.md']
        )

        self.assertEqual(
            sort_files(['b.md', 'index.html', 'a.md', 'index.md']),
            ['index.html', 'index.md', 'a.md', 'b.md']
        )

        self.assertEqual(
            sort_files(['a.md', 'index.md', 'b.md', 'index.html']),
            ['index.md', 'index.html', 'a.md', 'b.md']
        )

        self.assertEqual(
            sort_files(['.md', '_.md', 'a.md', 'index.md', '1.md']),
            ['index.md', '.md', '1.md', '_.md', 'a.md']
        )

        self.assertEqual(
            sort_files(['a.md', 'b.md', 'a.md']),
            ['a.md', 'a.md', 'b.md']
        )

    def test_md_file(self):
        f = File('/path/to/docs', 'foo/bar.md', filename='bar.md')
        self.assertEqual(f.root, 'bar')
        self.assertEqual(f.extension, '.md')
        self.assertEqual(f.input_path, 'foo/bar.md')
        self.assertEqual(f.full_input_path, '/path/to/docs/foo/bar.md'.replace('/', os.sep))
        self.assertEqual(f.output_path, 'foo/bar/index.html'.replace('/', os.sep))
        self.assertTrue(f.is_documentation_page())
        self.assertFalse(f.is_static_page())
        self.assertFalse(f.is_media_file())
        self.assertFalse(f.is_javascript())
        self.assertFalse(f.is_css())

    def test_md_index_file(self):
        f = File('/path/to/docs', 'index.md', filename='index.md')
        self.assertEqual(f.root, 'index')
        self.assertEqual(f.extension, '.md')
        self.assertEqual(f.input_path, 'index.md')
        self.assertEqual(f.full_input_path, '/path/to/docs/index.md'.replace('/', os.sep))
        self.assertEqual(f.output_path, 'index.html'.replace('/', os.sep))
        self.assertTrue(f.is_documentation_page())
        self.assertFalse(f.is_static_page())
        self.assertFalse(f.is_media_file())
        self.assertFalse(f.is_javascript())
        self.assertFalse(f.is_css())

    def test_md_file_no_filename(self):
        f = File('/path/to/docs', 'foo/bar.md')
        self.assertEqual(f.root, 'bar')
        self.assertEqual(f.extension, '.md')
        self.assertEqual(f.input_path, 'foo/bar.md')
        self.assertEqual(f.full_input_path, '/path/to/docs/foo/bar.md'.replace('/', os.sep))
        self.assertEqual(f.output_path, 'foo/bar/index.html'.replace('/', os.sep))
        self.assertTrue(f.is_documentation_page())
        self.assertFalse(f.is_static_page())
        self.assertFalse(f.is_media_file())
        self.assertFalse(f.is_javascript())
        self.assertFalse(f.is_css())

    def test_static_file(self):
        f = File('/path/to/docs', 'foo/bar.html', filename='bar.html')
        self.assertEqual(f.root, 'bar')
        self.assertEqual(f.extension, '.html')
        self.assertEqual(f.input_path, 'foo/bar.html')
        self.assertEqual(f.full_input_path, '/path/to/docs/foo/bar.html'.replace('/', os.sep))
        self.assertEqual(f.output_path, 'foo/bar.html'.replace('/', os.sep))
        self.assertFalse(f.is_documentation_page())
        self.assertTrue(f.is_static_page())
        self.assertFalse(f.is_media_file())
        self.assertFalse(f.is_javascript())
        self.assertFalse(f.is_css())

    def test_media_file(self):
        f = File('/path/to/docs', 'foo/bar.jpg', filename='bar.jpg')
        self.assertEqual(f.root, 'bar')
        self.assertEqual(f.extension, '.jpg')
        self.assertEqual(f.input_path, 'foo/bar.jpg')
        self.assertEqual(f.full_input_path, '/path/to/docs/foo/bar.jpg'.replace('/', os.sep))
        self.assertEqual(f.output_path, 'foo/bar.jpg'.replace('/', os.sep))
        self.assertFalse(f.is_documentation_page())
        self.assertFalse(f.is_static_page())
        self.assertTrue(f.is_media_file())
        self.assertFalse(f.is_javascript())
        self.assertFalse(f.is_css())

    def test_javascript_file(self):
        f = File('/path/to/docs', 'foo/bar.js', filename='bar.js')
        self.assertEqual(f.root, 'bar')
        self.assertEqual(f.extension, '.js')
        self.assertEqual(f.input_path, 'foo/bar.js')
        self.assertEqual(f.full_input_path, '/path/to/docs/foo/bar.js'.replace('/', os.sep))
        self.assertEqual(f.output_path, 'foo/bar.js'.replace('/', os.sep))
        self.assertFalse(f.is_documentation_page())
        self.assertFalse(f.is_static_page())
        self.assertTrue(f.is_media_file())
        self.assertTrue(f.is_javascript())
        self.assertFalse(f.is_css())

    def test_css_file(self):
        f = File('/path/to/docs', 'foo/bar.css', filename='bar.css')
        self.assertEqual(f.root, 'bar')
        self.assertEqual(f.extension, '.css')
        self.assertEqual(f.input_path, 'foo/bar.css')
        self.assertEqual(f.full_input_path, '/path/to/docs/foo/bar.css'.replace('/', os.sep))
        self.assertEqual(f.output_path, 'foo/bar.css'.replace('/', os.sep))
        self.assertFalse(f.is_documentation_page())
        self.assertFalse(f.is_static_page())
        self.assertTrue(f.is_media_file())
        self.assertFalse(f.is_javascript())
        self.assertTrue(f.is_css())

    def test_files(self):
        fs = [
            File('/path/to/docs', 'index.md', filename='index.md'),
            File('/path/to/docs', 'foo/bar.md', filename='bar.md'),
            File('/path/to/docs', 'foo/bar.html', filename='bar.html'),
            File('/path/to/docs', 'foo/bar.jpg', filename='bar.jpg'),
            File('/path/to/docs', 'foo/bar.js', filename='bar.js'),
            File('/path/to/docs', 'foo/bar.css', filename='bar.css')
        ]
        files = Files(fs)
        self.assertEqual([f for f in files], fs)
        self.assertEqual(len(files), len(fs))
        self.assertEqual(files.input_paths, {f.input_path: f for f in fs})
        self.assertEqual(files.documentation_pages(), [fs[0], fs[1]])
        self.assertEqual(files.static_pages(), [fs[2]])
        self.assertEqual(files.media_files(), [fs[3], fs[4], fs[5]])
        self.assertEqual(files.javascript_files(), [fs[4]])
        self.assertEqual(files.css_files(), [fs[5]])

    def test_filter_paths(self):
        # Root levle file
        self.assertFalse(_filter_paths('foo.md', 'foo.md', False, ['bar.md']))
        self.assertTrue(_filter_paths('foo.md', 'foo.md', False, ['foo.md']))

        # Nested file
        self.assertFalse(_filter_paths('foo.md', 'baz/foo.md', False, ['bar.md']))
        self.assertTrue(_filter_paths('foo.md', 'baz/foo.md', False, ['foo.md']))

        # Wildcard
        self.assertFalse(_filter_paths('foo.md', 'foo.md', False, ['*.txt']))
        self.assertTrue(_filter_paths('foo.md', 'foo.md', False, ['*.md']))

        # Root level dir
        self.assertFalse(_filter_paths('bar', 'bar', True, ['/baz']))
        self.assertFalse(_filter_paths('bar', 'bar', True, ['/baz/']))
        self.assertTrue(_filter_paths('bar', 'bar', True, ['/bar']))
        self.assertTrue(_filter_paths('bar', 'bar', True, ['/bar/']))

        # Nested dir
        self.assertFalse(_filter_paths('bar', 'foo/bar', True, ['/bar']))
        self.assertFalse(_filter_paths('bar', 'foo/bar', True, ['/bar/']))
        self.assertTrue(_filter_paths('bar', 'foo/bar', True, ['bar/']))

        # Files that look like dirs (no extension). Note that `is_dir` is `False`.
        self.assertFalse(_filter_paths('bar', 'bar', False, ['bar/']))
        self.assertFalse(_filter_paths('bar', 'foo/bar', False, ['bar/']))


class TestGetFiles(unittest.TestCase):
    def setUp(self):
        """ Create some temp files to fetch. """
        self.tdir = tempfile.mkdtemp()
        self.filenames = [
            'index.md',
            'bar.css',
            'bar.html',
            'bar.jpg',
            'bar.js',
            'bar.md'
        ]

        # Create empty files
        for f in self.filenames:
            open(os.path.join(self.tdir, f), 'w').close()
        # Create ignored file
        open(os.path.join(self.tdir, '.dotfile'), 'w').close()
        # Create ignored dir & file
        os.mkdir(os.path.join(self.tdir, 'templates'))
        open(os.path.join(self.tdir, 'templates/foo.html'), 'w').close()

    def test_get_files(self):
        files = get_files(self.tdir)
        self.assertEqual(len(files), len(self.filenames))
        self.assertEqual([f.input_path for f in files], self.filenames)

    def tearDown(self):
        """ Clean up after test. """
        shutil.rmtree(self.tdir)
