from flask import render_template, current_app
from app import app

@app.route('/detail/<unit>')
def show_detail(unit):
    current_app.logger.debug(current_app.template_folder)
    return render_template('test.html')

@app.route('/')
def index():
    return 'test'
