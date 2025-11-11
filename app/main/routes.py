from flask import render_template, session
from datetime import datetime
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
    current_date = datetime.now().strftime('%d/%m/%Y')
    return render_template('legal/politique_confidentialite.html', fl_session=fl_session, current_date=current_date)

@bp.route('/cgu')
def cgu():
    return render_template('legal/cgu.html', fl_session=fl_session)