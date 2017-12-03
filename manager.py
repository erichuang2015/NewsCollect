# -*- coding: utf-8 -*-
from flask_script import Manager
from webapp import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

app = create_app()
app.debug = True
bootstrap = Bootstrap(app)
db_path = os.path.abspath('.') + '\data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)
manager = Manager(app)


if __name__ == '__main__':
    manager.run()