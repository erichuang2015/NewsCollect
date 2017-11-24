from flask import Flask

app = Flask(__name__, static_folder='')


from .api_0_8 import api_0_8
app.register_blueprint(api_0_8, url_prefix='/api')

from index import main
app.register_blueprint(main)





