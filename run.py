import logging

import tornado
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
import tornado.options

from context.application import Application
from context.settings import PORT, LOGGING_LEVEL

tornado.options.define('port', type=int, default=PORT, help='server port number (default: 9000)')
tornado.options.define('debug', type=bool, default=False, help='run in debug mode with autoreload (default: False)')

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(tornado.options.options.port)
    IOLoop.instance().start()
