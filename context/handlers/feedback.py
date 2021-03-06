from tornado.gen import engine

from tornado.web import RequestHandler, asynchronous

from context.data.feedback import Feedback as FeedbackData
from context.handlers.extractors import ParamExtractor, BodyExtractor
from context.handlers.extractors import PathExtractor
from context import data, __version__


class Feedback(RequestHandler):
    context_data = None
    feedback_data = None

    _param_extractor = None
    _path_extractor = None
    _body_extractor = None

    def data_received(self, chunk):
        pass

    def initialize(self):
        self._param_extractor = ParamExtractor(self)
        self._path_extractor = PathExtractor(self)
        self._body_extractor = BodyExtractor(self)

        self.context_data = data.ContextData()
        self.context_data.open_connection()
        self.feedback_data = data.FeedbackData()
        self.feedback_data.open_connection()

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def post(self, context_id, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')

        inserted_feedback = self.feedback_data.insert(
            self._param_extractor.user_id(),
            self._param_extractor.application_id(),
            self._param_extractor.session_id(),
            self._path_extractor.context_id(context_id),
            self._param_extractor.product_id(),
            self._param_extractor.type(),
            self._body_extractor.meta_data()
        )

        _rev = inserted_feedback["_id"]

        self.set_status(201)
        self.set_header("Location", "/%s/feedback/%s" % (context_id, inserted_feedback["_id"]))
        self.set_header("_id", str(inserted_feedback["_id"]))
        self.set_header("_rev", str(_rev))
        self.finish()
