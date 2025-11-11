from flask import render_template, session
fl_session = session
from app.main import bp


@bp.route('/')
def index():
    return render_template('index.html',fl_session=fl_session)

@bp.route('/board')
def play():
    return render_template('play/index.html',fl_session=fl_session)

@bp.route('/mentions-legales')
def mentions_legales():
    return render_template('legal/mentions_legales.html', fl_session=fl_session)

@bp.route('/politique-confidentialite')
def politique_confidentialite():
    return render_template('legal/politique_confidentialite.html', fl_session=fl_session)

@bp.route('/cgu')
def cgu():
    return render_template('legal/cgu.html', fl_session=fl_session)