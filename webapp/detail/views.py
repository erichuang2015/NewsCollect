from flask import render_template
from . import detail

@detail.route('/<unit>')
def show_detail(unit):
    return render_template('detail.html')
