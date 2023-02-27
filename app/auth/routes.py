from flask import render_template, redirect, url_for
from app.auth import bp

@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/login/')
def login():
    return render_template('auth/login.html')

@bp.route('/login/')
def register():
    return render_template('auth/sign.html')

@bp.route('/')
def logout():
    redirect(url_for('index'))