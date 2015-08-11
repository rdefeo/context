from bson import ObjectId
from bson.errors import InvalidId
from tornado.escape import json_decode, json_encode
from tornado.gen import engine
from tornado.web import RequestHandler, asynchronous, Finish
from bson.json_util import dumps, loads

from context import data, __version__


class Message(RequestHandler):
    context_data = None
    message_data = None

    def data_received(self, chunk):
        pass

    def initialize(self):
        from context.contextualizer import Contextualizer
        self.contextualizer = Contextualizer()
        self.context_data = data.ContextData()
        self.context_data.open_connection()
        self.message_data = data.MessageData()
        self.message_data.open_connection()

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def post(self, context_id, *args, **kwargs):
        # TODO get existing context here
        message = self.message_data.insert(
            self.path_context_id(context_id),
            self.body_direction(),
            self.body_text(),
            detection=self.body_detection()
        )

        # TODO expect ver to more efficiently get messages

        # TODO get messages

        # TODO calculate new context
        _ver = message["_id"]
        self.contextualizer.update(self.path_context_id(context_id), _ver, [message])

        self.set_status(201)
        self.set_header("Location", "/%s/messages/%s" % (context_id, message["_id"]))
        self.set_header("_id", str(message["_id"]))
        self.set_header("_rev", str(_ver))
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
            return loads(self.request.body.decode("utf-8"))
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

    def body_direction(self) -> data.MessageDirection:
        raw_direction = self.body()["direction"] if "direction" in self.body() else None
        try:
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

    def body_detection(self) -> dict:
        return self.body()["detection"] if "detection" in self.body() else None

    def body_text(self) -> str:
        if "text" in self.body():
            return self.body()["text"]
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
    message_data = None

    def data_received(self, chunk):
        pass

    def initialize(self):
        self.message_data = data.MessageData()
        self.message_data.open_connection()

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def get(self, context_id, *args, **kwargs):
        db_messages = self.message_data.find(context_id=self.path_context_id(context_id))

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
