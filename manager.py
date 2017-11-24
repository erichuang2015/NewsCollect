# -*- coding: utf-8 -*-
from flask_script import Manager
from webapp import app
from flask_sqlalchemy import SQLAlchemy
import os

# app = create_app()
app.debug = True
db_path = os.path.abspath('.') + '\data.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
db = SQLAlchemy(app)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()