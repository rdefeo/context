from bson import ObjectId
import tornado

__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode


class Root(RequestHandler):
    def initialize(self, contextualizer):
        self.contextualizer = contextualizer

    def on_finish(self):
        pass

    @asynchronous
    def get(self, *args, **kwargs):
        context_id = self.get_argument("context_id", None)
        self.set_status(200)
        hours = 600
        self.set_header('Cache-Control', 'public,max-age=%d' % int(3600*hours))
        self.finish(
            self.contextualizer.cache[context_id]
        )

    @asynchronous
    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        user_id = self.get_argument("user_id", None)
        session_id = self.get_argument("session_id", None)
        application_id = self.get_argument("application_id", None)
        locale = self.get_argument("locale", None)
        body = tornado.escape.json_decode(self.request.body)

        if application_id is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=application_id"
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
        elif locale is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=locale"
                    }
                )
            )
        else:
            detection_response = None
            if "detection_response" in body:
                detection_response = body["detection_response"]

            new_context_id = ObjectId()
            context = self.contextualizer.create(
                new_context_id,
                user_id,
                session_id,
                detection_response

            )

            self.add_header(
                "Location",
                "http://%s/%s" % (self.request.host, str(context["_id"]))
            )
            self.set_status(201)
            self.finish(context)

            if self.get_argument("skip_mongodb_log", None) is None:
                from context.data.context import Context
                context_data = Context()
                context_data.open_connection()
                context_data.insert(
                    context["entities"],
                    locale,
                    ObjectId(context["_id"]),
                    ObjectId(application_id),
                    ObjectId(session_id),
                    ObjectId(user_id) if user_id is not None else None,
                    ObjectId(detection_response["_id"]) if detection_response is not None else None
                )
                context_data.close_connection()