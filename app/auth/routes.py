from flask import render_template, redirect, url_for, session, request, flash
from app.auth import bp
fl_session = session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.authentication_check import *
from app.models.game_tables import *

@bp.route('/')
def index():
    return render_template('auth/index.html', fl_session=fl_session)

@bp.route('/register', methods=["GET"])
def register():
    return render_template('auth/sign.html', fl_session=fl_session)

@bp.route('/sign-in', methods=["POST"])
def register_in():
#     Session = sessionmaker(bind=engine)
#     session = Session()

    username = request.form['username']
    password = request.form['password']
    auth = Auth(username=username)
    auth.set_password(password)
    db.session.add(auth)
    db.session.commit()
    return render_template('auth/index.html', fl_session=fl_session)


@bp.route('/login', methods=['GET'])
def login():
    return render_template('auth/login.html', fl_session=fl_session)

@bp.route('/login/checked', methods=['POST'])
def check_login():
    if request.method == 'POST':
          username = str(request.form['username'])
          password = str(request.form['password'])
    else:
        return redirect(url_for('auth.index'))

    auth_data = Auth.query.all()
    user_pass = Auth.query.filter_by(username=username).first()
    print(user_pass)
    is_password_check = True
    if is_password_check :
        fl_session['username'] = request.form['username']
        return render_template('auth/index.html', user_pass=user_pass, auth_data=auth_data, username=username, fl_session=fl_session)
    else:
        return render_template('auth/login.html', auth_data=auth_data, username=username, fl_session=fl_session)

@bp.route('/logout')
def logout():
    # remove the username from the session if it's there
    fl_session.pop('username', None)
    return redirect(url_for('main.index'))