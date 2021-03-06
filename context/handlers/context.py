from bson import ObjectId
from bson.json_util import dumps
from tornado.web import RequestHandler, asynchronous

from context.contextualizer import Contextualizer
from context.handlers.extractors import ParamExtractor, PathExtractor


class Context(RequestHandler):
    context_data = None
    contextualizer = None
    param_extractor = None
    path_extractor = None

    def initialize(self, contextualizer: Contextualizer):
        self.contextualizer = contextualizer
        from context.data.context import Context
        self.context_data = Context()
        self.context_data.open_connection()
        self.param_extractor = ParamExtractor(self)
        self.path_extractor = PathExtractor(self)

    def data_received(self, chunk):
        pass

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
                self.context_data.get(self.path_extractor.context_id(context_id), self.param_extractor.rev())
            )
        )

    @asynchronous
    def post(self, *args, **kwargs):
        new_context_id = ObjectId()
        self.contextualizer.create(
            new_context_id,
            self.param_extractor.user_id(),
            self.param_extractor.application_id(),
            self.param_extractor.session_id(),
            self.param_extractor.locale()
        )

        self.set_header('Content-Type', 'application/json')
        self.add_header("Location", "/%s" % str(new_context_id))
        self.add_header("_id", str(new_context_id))
        self.add_header("_rev", str(new_context_id))
        self.set_status(201)
        self.finish()
