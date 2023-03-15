from flask import render_template
from app.main import bp


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/board')
def play():
    return render_template('play/index.html')