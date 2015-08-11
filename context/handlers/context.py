from bson import ObjectId
from bson.errors import InvalidId
from bson.json_util import dumps

__author__ = 'robdefeo'
from tornado.web import RequestHandler, asynchronous, Finish
from tornado.escape import json_encode, json_decode


class Context(RequestHandler):
    context_data = None

    def initialize(self, contextualizer):
        self.contextualizer = contextualizer
        from context.data.context import Context
        self.context_data = Context()
        self.context_data.open_connection()

    def on_finish(self):
        pass

    @asynchronous
    def get(self, context_id, *args, **kwargs):
        self.set_status(200)
        self.set_header('Content-Type', 'application/json')
        
        # hours = 600
        # self.set_header('Cache-Control', 'public,max-age=%d' % int(3600*hours))
        self.finish(
            dumps(
                self.context_data.get(self.path_context_id(context_id), self.param_ver())
            )
        )

    @asynchronous
    def post(self, *args, **kwargs):
        new_context_id = ObjectId()
        context = self.contextualizer.create(new_context_id, self.param_user_id(), self.param_session_id())

        self.set_header('Content-Type', 'application/json')
        self.add_header("Location", "/%s" % str(context["_id"]))
        self.add_header("_id", str(context["_id"]))
        self.add_header("_ver", str(context["_id"]))
        self.set_status(202)
        self.finish()

        self.context_data.insert(
            context["entities"],
            self.param_locale(),
            context["_id"],
            self.param_application_id(),
            self.param_session_id(),
            self.param_user_id()
        )
        self.context_data.close_connection()

    def param_ver(self):
        return self.get_argument("_ver", None)

    def param_locale(self):
        locale = self.get_argument("locale", None)
        if locale is None:
            self.set_status(428)
            self.finish(
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

    def param_application_id(self):
        raw_application_id = self.get_argument("application_id", None)
        if raw_application_id is None:
            self.set_status(428)
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

    def param_session_id(self):
        raw_session_id = self.get_argument("session_id", None)
        if not raw_session_id:
            self.set_status(428)
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

    def path_context_id(self, context_id) -> ObjectId:
        try:
            return ObjectId(context_id)
        except:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=context_id,context_id=%s" % context_id
                    }
                )
            )
            raise Finish()
