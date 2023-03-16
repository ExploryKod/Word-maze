from flask import render_template, session
fl_session = session
from app.main import bp


@bp.route('/')
def index():
    return render_template('index.html',fl_session=fl_session)

@bp.route('/board')
def play():
    return render_template('play/index.html',fl_session=fl_session)