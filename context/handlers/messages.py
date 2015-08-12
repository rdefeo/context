from tornado.gen import engine
from tornado.web import RequestHandler, asynchronous

from bson.json_util import dumps

from context import data, __version__
from context.handlers.extractors import ParamExtractor, BodyExtractor, PathExtractor


class Message(RequestHandler):
    context_data = None
    message_data = None
    contextualizer = None
    param_extractor = None
    path_extractor = None
    body_extractor = None

    def data_received(self, chunk):
        pass

    def initialize(self):
        self.param_extractor = ParamExtractor(self)
        self.path_extractor = PathExtractor(self)
        self.body_extractor = BodyExtractor(self)

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
            self.path_extractor.context_id(context_id),
            self.body_extractor.direction(),
            self.body_extractor.text(),
            detection=self.body_extractor.detection()
        )

        # TODO expect ver to more efficiently get messages

        # TODO get messages

        # TODO calculate new context
        _ver = message["_id"]
        self.contextualizer.update(self.path_extractor.context_id(context_id), _ver, [message])

        self.set_status(201)
        self.set_header("Location", "/%s/messages/%s" % (context_id, message["_id"]))
        self.set_header("_id", str(message["_id"]))
        self.set_header("_rev", str(_ver))
        self.finish()


class Messages(RequestHandler):
    message_data = None
    param_extractor = None
    path_extractor = None
    body_extractor = None

    def data_received(self, chunk):
        pass

    def initialize(self):
        self.message_data = data.MessageData()
        self.message_data.open_connection()

        self.param_extractor = ParamExtractor(self)
        self.path_extractor = PathExtractor(self)
        self.body_extractor = BodyExtractor(self)

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def get(self, context_id, *args, **kwargs):
        db_messages = self.message_data.find(context_id=self.path_extractor.context_id(context_id))

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
