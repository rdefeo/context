from bson import ObjectId
from tornado.escape import json_decode, json_encode
from tornado.gen import engine
from tornado.web import RequestHandler, asynchronous
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
        try:
            db_context_id = ObjectId(context_id)
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
            return

        try:
            body = json_decode(self.request.body)
        except:
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid body,body=%s" % self.request.body
                    }
                )
            )
            return

        try:
            raw_direction = body["direction"] if "direction" in body else None
            direction = data.MessageDirection(int(raw_direction))
        except:

            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid direction,direction=%s" % raw_direction
                    }
                )
            )
            return

        try:
            detection_id = ObjectId(body["detection_id"]) if "detection_id" in body else None
        except:
            self.set_status(412)
            self.finish(
                json_encode(
                    {
                        "status": "error",
                        "message": "invalid param=detection_id,detection_id=%s" % body["detection_id"]
                    }
                )
            )
            return

        message_id = self.context_data.insert_message(
            db_context_id,
            direction,
            body["text"],
            detection_id=detection_id
        )
        self.set_status(201)
        self.set_header("Location", "/%s/messages/%s" % (context_id, message_id))
        self.finish()


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
        db_context_id = ObjectId(context_id)
        db_messages = self.context_data.find_messages(context_id=db_context_id)

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
