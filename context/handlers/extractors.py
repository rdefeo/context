from bson import ObjectId
from bson.errors import InvalidId
from bson.json_util import loads
from tornado.escape import json_encode, json_decode
from tornado.web import RequestHandler, Finish
from context.data import MessageDirection


class PathExtractor:
    def __init__(self, handler: RequestHandler):
        self.handler = handler

    def context_id(self, context_id) -> ObjectId:
        try:
            return ObjectId(context_id)
        except:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=context_id,context_id=%s" % context_id
                    }
                )
            )
            raise Finish()


class BodyExtractor:
    def __init__(self, handler: RequestHandler):
        self.handler = handler

    def body(self) -> dict:
        try:
            return loads(self.handler.request.body.decode("utf-8"))
        except:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid body,body=%s" % self.handler.request.body
                    }
                )
            )
            raise Finish()

    def meta_data(self) -> str:
        try:
            return self.body()["meta_data"] if "meta_data" in self.body() else None
        except:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "body [mete_data] direction"
                    }
                )
            )
            raise Finish()

    def direction(self) -> MessageDirection:
        raw_direction = self.body()["direction"] if "direction" in self.body() else None
        try:
            return MessageDirection(int(raw_direction))
        except:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid direction,direction=%s" % raw_direction
                    }
                )
            )
            raise Finish()

    def detection(self) -> dict:
        return self.body()["detection"] if "detection" in self.body() else None

    def text(self) -> str:
        if "text" in self.body():
            return self.body()["text"]
        else:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing [text]"
                    }
                )
            )
            raise Finish()


class ParamExtractor:
    def __init__(self, handler: RequestHandler):
        self.handler = handler
        pass

    def session_id(self) -> ObjectId:
        raw_session_id = self.handler.get_argument("session_id", None)
        if raw_session_id is None:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param(s) session_id"
                    }
                )
            )
            raise Finish()

        try:
            return ObjectId(raw_session_id)
        except InvalidId:
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=session_id,session_id=%s" % raw_session_id
                    }
                )
            )
            raise Finish()

    def application_id(self) -> ObjectId:
        raw_application_id = self.handler.get_argument("application_id", None)
        if raw_application_id is None:
            self.handler.set_status(428)
            self.handler.finish(
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
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=application_id,application_id=%s" %
                                   raw_application_id
                    }
                )
            )
            raise Finish()

    def product_id(self) -> ObjectId:
        raw_product_id = self.handler.get_argument("product_id", None)
        if not raw_product_id:
            self.handler.set_status(428)
            self.handler.finish(
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
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=product_id,product_id=%s" % raw_product_id
                    }
                )
            )
            raise Finish()

    def context_id(self):
        raw_context_id = self.handler.get_argument("context_id", None)
        if not raw_context_id:
            self.handler.set_status(428)
            self.handler.finish(
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
            self.handler.set_status(412)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=context_id,context_id=%s" % raw_context_id
                    }
                )
            )
            raise Finish()

    def user_id(self) -> ObjectId:
        raw_user_id = self.handler.get_argument("user_id", None)
        try:
            return ObjectId(raw_user_id) if raw_user_id is not None else None
        except InvalidId:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=user_id,user_id=%s" % raw_user_id
                    }
                )
            )
            raise Finish()

    def rev(self):
        raw_rev = self.handler.get_argument("_rev", None)
        try:
            return ObjectId(raw_rev) if raw_rev is not None else None
        except InvalidId:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=_rev,_rev=%s" % raw_rev
                    }
                )
            )
            raise Finish()

    def locale(self):
        locale = self.handler.get_argument("locale", None)
        if locale is None:
            self.handler.set_status(428)
            self.handler.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing param=locale"
                    }
                )
            )
            raise Finish()
        else:
            return locale

    def type(self):
        _type = self.handler.get_argument("type", None)
        if _type is None:
            self.handler.set_status(428)
            self.handler.finish(
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
