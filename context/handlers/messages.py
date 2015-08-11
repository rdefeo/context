from bson import ObjectId
from bson.errors import InvalidId
from tornado.escape import json_decode, json_encode
from tornado.gen import engine
from tornado.web import RequestHandler, asynchronous, Finish
from bson.json_util import dumps

from context import data, __version__


class Message(RequestHandler):
    context_data = None

    def data_received(self, chunk):
        pass

    def initialize(self):
        self.context_data = data.ContextData()
        self.context_data.open_connection()

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def post(self, context_id, *args, **kwargs):
        message_id = self.context_data.insert_message(
            self.path_context_id(context_id),
            self.body_direction(),
            self.body_text(),
            detection_id=self.param_detection_id()
        )
        self.set_status(201)
        self.set_header("Location", "/%s/messages/%s" % (context_id, message_id))
        self.finish()

    def path_context_id(self, context_id) -> ObjectId:
        try:
            return ObjectId(context_id)
        except InvalidId:
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

    def param_detection_id(self):
        raw_detection_id = self.get_argument("detection_id", None)
        try:
            return ObjectId(raw_detection_id) if raw_detection_id is not None else None
        except InvalidId:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=detection_id,detection_id=%s" % raw_detection_id
                    }
                )
            )
            return

    def body_direction(self) -> data.MessageDirection:
        try:
            raw_direction = self.body()["direction"] if "direction" in self.body() else None
            return data.MessageDirection(int(raw_direction))
        except:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid direction,direction=%s" % raw_direction
                    }
                )
            )
            raise Finish()

    def body_text(self) -> str:
        if "text" in self.body():
            return self.body()["body"]
        else:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "missing [text]"
                    }
                )
            )
            raise Finish()


class Messages(RequestHandler):
    context_data = None

    def data_received(self, chunk):
        pass

    def initialize(self):
        self.context_data = data.ContextData()
        self.context_data.open_connection()

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def get(self, context_id, *args, **kwargs):

        db_messages = self.context_data.find_messages(context_id=self.path_context_id(context_id))

        self.set_status(200)
        self.set_header("Content-Type", "application/json")
        self.finish(
            dumps(
                {
                    "messages": db_messages,
                    "version": __version__
                }
            )
        )

        # hours = 600
        # self.set_header('Cache-Control', 'public,max-age=%d' % int(3600*hours))
        # self.finish(
        #     self.contextualizer.cache[context_id]
        # )

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
