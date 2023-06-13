from flask import render_template
from app.writer import bp


@bp.route('/', methods=('GET', 'POST'))
def index():
    return render_template('writer/index.html')