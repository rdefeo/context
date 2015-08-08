import tornado
from tornado.web import url
from context.handlers.feedback import Feedback
from context.handlers.root import Root
from context.handlers.status import Status
from context.contextualizer import Contextualizer
import tornado.options
from context import handlers


class Application(tornado.web.Application):
    def __init__(self):
        application_handlers = [
            url(r"/", Root, dict(contextualizer=Contextualizer()), name="root"),
            url(r"/(.*)/messages", handlers.MessagesHandler, name="messages"),
            url(r"/(.*)/messages/", handlers.MessageHandler, name="message"),
            url(r"/feedback", handlers.FeedbackHandler, name="feedback"),
            url(r"/status", handlers.StatusHandler, name="status")
        ]

        settings = dict(
            # static_path = os.path.join(os.path.dirname(__file__), "static"),
            # template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug=tornado.options.options.debug,
        )
        tornado.web.Application.__init__(self, application_handlers, **settings)