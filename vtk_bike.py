import os

from flask import Flask
from flask.ext.pymongo import PyMongo
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.name = "VTK_BIKE"
app.config.from_object(os.environ['APP_SETTINGS'])
mongo = PyMongo(app)
Bootstrap(app)

from views import *

if __name__ == '__main__':
    utilities.start_thread()
    app.run(host='0.0.0.0')
