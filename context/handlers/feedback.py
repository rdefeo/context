from bson import ObjectId
from bson.errors import InvalidId
from tornado.gen import engine
from tornado.web import RequestHandler, asynchronous, Finish, MissingArgumentError
from tornado.escape import json_encode, json_decode

from context.data.feedback import Feedback as FeedbackData
from context.handlers.extractors import ParamExtractor, BodyExtractor
from context.handlers.extractors import PathExtractor


class Feedback(RequestHandler):
    param_extractor = None
    path_extractor = None
    body_extractor = None

    def initialize(self):
        self.param_extractor = ParamExtractor(self)
        self.path_extractor = PathExtractor(self)
        self.body_extractor = BodyExtractor(self)

    def on_finish(self):
        pass

    @asynchronous
    @engine
    def post(self, *args, **kwargs):
        self.set_header('Content-Type', 'application/json')

        data = FeedbackData()
        data.open_connection()
        data.insert(
            self.param_extractor.user_id(),
            self.param_extractor.application_id(),
            self.param_extractor.session_id(),
            self.param_extractor.context_id(),
            self.param_extractor.product_id(),
            self.param_extractor.type(),
            self.body_extractor.meta_data()
        )
        data.close_connection()

        self.set_status(200)
        self.finish({})


