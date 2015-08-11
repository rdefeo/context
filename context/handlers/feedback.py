from bson import ObjectId
from bson.errors import InvalidId
from tornado.gen import engine
from tornado.web import RequestHandler, asynchronous, Finish, MissingArgumentError
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

        data = FeedbackData()
        data.open_connection()
        data.insert(
            self.param_user_id(),
            self.param_application_id(),
            self.param_session_id(),
            self.param_context_id(),
            self.param_product_id(),
            self.param_type(),
            self.body_meta_data()
        )
        data.close_connection()

        self.set_status(200)
        self.finish({})

    def body_meta_data(self) -> str:
        try:
            return self.body()["meta_data"] if "meta_data" in self.body() else None
        except:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "body [mete_data] direction,direction=%s"
                    }
                )
            )
            raise Finish()

    def body(self) -> dict:
        try:
            return json_decode(self.request.body)
        except:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid body,body=%s" % self.request.body
                    }
                )
            )
            raise Finish()


    def param_type(self):
        _type = self.get_argument("type", None)
        if _type is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=type"
                    }
                )
            )
            raise Finish()
        else:
            return _type

    def param_context_id(self):
        raw_context_id = self.get_argument("context_id", None)
        if not raw_context_id:
            self.set_status(412)
            self.finish(
                json_encode({
                    "status": "error",
                    "message": "missing param(s) context_id"
                }
                )
            )
            raise Finish()

        try:
            return ObjectId(raw_context_id)
        except InvalidId:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=context_id,context_id=%s" % raw_context_id
                    }
                )
            )
            raise Finish()

    def param_product_id(self):
        raw_product_id = self.get_argument("product_id", None)
        if not raw_product_id:
            self.set_status(412)
            self.finish(
                json_encode({
                    "status": "error",
                    "message": "missing param(s) product_id"
                }
                )
            )
            raise Finish()

        try:
            return ObjectId(raw_product_id)
        except InvalidId:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=product_id,product_id=%s" % raw_product_id
                    }
                )
            )
            raise Finish()

    def param_session_id(self):
        raw_session_id = self.get_argument("session_id", None)
        if not raw_session_id:
            self.set_status(412)
            self.finish(
                json_encode({
                    "status": "error",
                    "message": "missing param(s) session_id"
                }
                )
            )
            raise Finish()

        try:
            return ObjectId(raw_session_id)
        except InvalidId:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=session_id,session_id=%s" % raw_session_id
                    }
                )
            )
            raise Finish()

    def param_application_id(self):
        raw_application_id = self.get_argument("application_id", None)
        if raw_application_id is None:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param(s) application_id"
                    }
                )
            )
            raise Finish()

        try:
            return ObjectId(raw_application_id)
        except InvalidId:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=application_id,application_id=%s" % raw_application_id
                    }
                )
            )
            raise Finish()

    def param_user_id(self):
        raw_user_id = self.get_argument("user_id", None)
        try:
            return ObjectId(raw_user_id) if raw_user_id is not None else None
        except InvalidId:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=user_id,user_id=%s" % raw_user_id
                    }
                )
            )
            raise Finish()
