import tornado
from tornado.web import url
from context.contextualizer import Contextualizer
import tornado.options
from context import handlers


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            # static_path = os.path.join(os.path.dirname(__file__), "static"),
            # template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug=tornado.options.options.debug,
        )
        tornado.web.Application.__init__(
            self,
            [
                url(r"/(.*)?    ", handlers.ContextHandler, dict(contextualizer=Contextualizer()), name="context"),
                url(r"/(.*)/messages", handlers.MessagesHandler, name="messages"),
                url(r"/(.*)/messages/", handlers.MessageHandler, name="message"),
                url(r"/feedback", handlers.FeedbackHandler, name="feedback"),
                url(r"/status", handlers.StatusHandler, name="status")
            ],
            **settings
        )