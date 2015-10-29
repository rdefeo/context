import tornado
from tornado.web import url
import tornado.options

from context.contextualizer import Contextualizer
from context import handlers
from context.data import ContextData


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            # static_path = os.path.join(os.path.dirname(__file__), "static"),
            # template_path = os.path.join(os.path.dirname(__file__), "templates"),
            debug=tornado.options.options.debug,
        )
        context_data = ContextData()
        context_data.open_connection()

        tornado.web.Application.__init__(
            self,
            [
                url(
                    r"/([0-9a-fA-F]+)?",
                    handlers.ContextHandler,
                    dict(contextualizer=Contextualizer(context_data)),
                    name="context"
                ),
                url(r"/([0-9a-fA-F]+)/messages", handlers.MessagesHandler, name="messages"),
                url(r"/([0-9a-fA-F]+)/messages/", handlers.MessageHandler, name="message"),
                url(r"/([0-9a-fA-F]+)/feedback/", handlers.FeedbackHandler, name="feedback"),
                url(r"/status", handlers.StatusHandler, name="status")
            ],
            **settings
        )
