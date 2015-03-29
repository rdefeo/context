from bson import ObjectId
from tornado.gen import engine
from tornado.web import RequestHandler, asynchronous
from tornado.escape import json_encode, json_decode
from context.data.feedback import Feedback as FeedbackData


class Feedback(RequestHandler):
    def initialize(self):
        pass

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')
        user_id = self.get_argument("user_id", None)
        session_id = self.get_argument("session_id", None)
        context_id = self.get_argument("context_id", None)
        application_id = self.get_argument("application_id", None)
        product_id = self.get_argument("product_id", None)
        _type = self.get_argument("type", None)
        body = json_decode(self.request.body)

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
        elif product_id is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=product_id"
                    }
                )
            )
        elif _type is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=type"
                    }
                )
            )
        else:
            data = FeedbackData()
            data.open_connection()
            data.insert(
                ObjectId(user_id) if user_id is not None else None,
                ObjectId(application_id),
                ObjectId(session_id),
                ObjectId(context_id),
                ObjectId(product_id),
                _type,
                body["meta_data"] if "meta_data" in body else None
            )
            data.close_connection()

            self.set_status(200)
            self.finish({})