# -*- coding: utf-8 -*-
from . import main
from flask import current_app


@main.route('/')
def index():
    current_app.logger.debug(main)
    return main.send_static_file('index.html')
