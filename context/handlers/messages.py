from bson import ObjectId
from tornado.gen import engine
from tornado.web import RequestHandler, asynchronous

from context import data, __version__


class Messages(RequestHandler):
    def initialize(self):
        self.messages_data = data.MessageData()
        self.messages_data.open_connection()

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def get(self, context_id, *args, **kwargs):
        db_context_id = ObjectId(context_id)
        db_messages = self.messages_data.find(context_id=db_context_id)

        self.set_status(200)
        self.finish(
            {
                "messages": db_messages,
                "version": __version__
            }
        )

        # hours = 600
        # self.set_header('Cache-Control', 'public,max-age=%d' % int(3600*hours))
        # self.finish(
        #     self.contextualizer.cache[context_id]
        # )
