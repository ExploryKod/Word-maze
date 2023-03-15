from flask import render_template, redirect, url_for, session, request, flash
from app.auth import bp
fl_session = session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.authentication_check import *
from app.models.authentication_tables import User

@bp.route('/')
def index():
    return render_template('auth/index.html')

@bp.route('/register', methods=["GET"])
def register():
    return render_template('auth/sign.html', fl_session=fl_session)

@bp.route('/sign-in', methods=["POST"])
def register_in():
    Session = sessionmaker(bind=engine)
    session = Session()

    username = request.form['username']
    password = request.form['password']
    # password = generate_password_hash(password)
    user = User(username,password)
    session.add(user)
    session.commit()
    return redirect(url_for('auth.index'))


@bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html', fl_session=fl_session)

@bp.route('/login/checked', methods=['POST'])
def check_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
    else:
        return redirect(url_for('auth.index'))
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        flash('good password!')
        fl_session['username'] = request.form['username']
        return redirect(url_for('auth.index'))
    else:
        flash('wrong password!')
        return redirect(url_for('login'))

@bp.route('/logout')
def logout():
    # remove the username from the session if it's there
    fl_session.pop('username', None)
    return redirect(url_for('main.index'))