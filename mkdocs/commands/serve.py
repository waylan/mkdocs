from __future__ import unicode_literals
import logging
import shutil
import tempfile

from mkdocs.commands.build import build
from mkdocs.config import load_config

log = logging.getLogger(__name__)


def _get_error_handler():
    """
    Return an ErrorHandler which returns user provided error pages.
    
    Thanks to @jehiah for the code: https://gist.github.com/jehiah/398252
    
    """
    
    # Importing here to seperate the code paths from static_server and livereload
    from tornado.web import RequestHandler

    class ErrorHandler(RequestHandler):
        """ Generates an error response with status_code for all requests. """

        def __init__(self, application, request, status_code):
            tornado.web.RequestHandler.__init__(self, application, request)
            self.set_status(status_code)
        
        def get_error_html(self, status_code, **kwargs):
            self.require_setting("static_path")
            if status_code in [404, 500, 503, 403]:
                filename = os.path.join(self.settings['static_path'], '%d.html' % status_code)
                if os.path.exists(filename):
                    f = open(filename, 'r')
                    data = f.read()
                    f.close()
                    return data
            return "<html><title>%(code)d: %(message)s</title>" \
                    "<body class='bodyErrorPage'>%(code)d: %(message)s</body></html>" % {
                "code": status_code,
                "message": httplib.responses[status_code],
            }
        
        def prepare(self):
            raise tornado.web.HTTPError(self._status_code)

    return ErrorHandler


def _livereload(host, port, config, builder, site_dir):

    # We are importing here for anyone that has issues with livereload. Even if
    # this fails, the --no-livereload alternative should still work.

    # Monkey patch tornado ErrorHandler as LiveReload offers no way to override.
    from tornado import web
    web.ErrorHandler = _get_error_handler()
    
    from livereload import Server

    server = Server()

    # Watch the documentation files, the config file and the theme files.
    server.watch(config['docs_dir'], builder)
    server.watch(config['config_file_path'], builder)

    for d in config['theme_dir']:
        server.watch(d, builder)

    server.serve(root=site_dir, host=host, port=int(port), restart_delay=0)


def _static_server(host, port, site_dir):

    # Importing here to seperate the code paths from the --livereload
    # alternative.
    from tornado import ioloop
    from tornado import web
    
    settings = {
        'default_handler_class': _get_error_handler(),
        'static_path': site_dir
    }

    application = web.Application([
        (r"/(.*)", web.StaticFileHandler, {
            "path": site_dir,
            "default_filename": "index.html"
        }),
    ], settings=settings)
    application.listen(port=int(port), address=host)

    log.info('Running at: http://%s:%s/', host, port)
    log.info('Hold ctrl+c to quit.')
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        log.info('Stopping server...')


def serve(config_file=None, dev_addr=None, strict=None, theme=None,
          theme_dir=None, livereload='livereload'):
    """
    Start the MkDocs development server

    By default it will serve the documentation on http://localhost:8000/ and
    it will rebuild the documentation and refresh the page automatically
    whenever a file is edited.
    """

    # Create a temporary build directory, and set some options to serve it
    tempdir = tempfile.mkdtemp()

    def builder():
        log.info("Building documentation...")
        config = load_config(
            config_file=config_file,
            dev_addr=dev_addr,
            strict=strict,
            theme=theme,
            theme_dir=theme_dir
        )
        config['site_dir'] = tempdir
        live_server = livereload in ['dirty', 'livereload']
        dirty = livereload == 'dirtyreload'
        build(config, live_server=live_server, dirty=dirty)
        return config

    # Perform the initial build
    config = builder()

    host, port = config['dev_addr'].split(':', 1)

    try:
        if livereload in ['livereload', 'dirtyreload']:
            _livereload(host, port, config, builder, tempdir)
        else:
            _static_server(host, port, tempdir)
    finally:
        shutil.rmtree(tempdir)
