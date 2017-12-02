from flask import Flask

app = Flask(__name__)

from .api_0_8 import api_0_8
app.register_blueprint(api_0_8, url_prefix='/api')

from detail import detail
app.register_blueprint(detail, url_prefix='/detail')





