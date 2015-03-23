import tornado

__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode
from context.contextualizer import Contextualizer


class Root(RequestHandler):
    def initialize(self):
        pass

    def on_finish(self):
        pass

    @asynchronous
    def post(self):
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
            contextualizer = Contextualizer()
            context = contextualizer.contextualize(
                user_id,
                session_id,
                body["detection_result"] if "detection_result" in body else None
            )

            self.set_header('Content-Type', 'application/json')
            self.set_status(200)
            self.finish({
                "context": context,
                "version": "0.0.1"
            })

