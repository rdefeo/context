__author__ = 'robdefeo'
import sys

from flask import Flask

app = Flask(__name__)

from context.views.log import mod_log
app.register_blueprint(mod_log)

from context.views.interest import mod_interest
app.register_blueprint(mod_interest)

from context.views.root import mod_root
app.register_blueprint(mod_root)
