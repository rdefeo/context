__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode
from context import __version__

class Status(RequestHandler):
    def initialize(self):
        pass

    def on_finish(self):
        pass

    @asynchronous
    def get(self):
        self.set_header('Content-Type', 'application/json')
        self.set_status(200)
        self.finish({
            "status": "OK",
            "version": __version__
        })

