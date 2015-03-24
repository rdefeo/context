import tornado

__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode
from context.contextualizer import Contextualizer


class Root(RequestHandler):
    def initialize(self, contextualizer):
        self.contextualizer = contextualizer

    def on_finish(self):
        pass

    @asynchronous
    def get(self, context_id):
        self.set_status(200)
        hours = 600
        self.set_header('Cache-Control', 'public,max-age=%d' % int(3600*hours))
        self.finish(
            self.contextualizer.cache[context_id]
        )

    @asynchronous
    def post(self, nothing):
        user_id = self.get_argument("user_id", None)
        session_id = self.get_argument("session_id", None)
        body = tornado.escape.json_decode(self.request.body)

        if user_id is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=user_id"
                    }
                )
            )

        elif session_id is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=session_id"
                    }
                )
            )
        else:
            detection_response = None
            if "detection_response" in body:
                detection_response = body["detection_response"]

            context = self.contextualizer.create(
                user_id,
                session_id,
                detection_response
            )

            self.add_header(
                "Location",
                "http://%s/%s" % (self.request.host, str(context["_id"]))
            )
            self.set_header('Content-Type', 'application/json')
            self.set_status(201)
            self.finish(
                context
            )

