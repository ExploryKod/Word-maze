from flask import Blueprint, render_template
from auth.models import *

auth = Blueprint('auth', __name__,
    template_folder='templates',
    static_folder='static', static_url_path='assets')

# function to render index page (home)
@app.route('/')
def index():
	# Query all data and then pass it to the template
    user_words = Guess.query.all()
    resp = Secrets.query.all()
    player = Users.query.all() 
    points = Scores.query.all()
    return render_template('index.html', user_words=user_words, resp=resp, player=player, points=points, fl_session=fl_session)


@app.route('/register', methods=["GET"])
def register():
    return render_template('sign.html', fl_session=fl_session)

@app.route('/register/in', methods=["POST"])
def register_in():
    Session = sessionmaker(bind=engine)
    session = Session()

    username = request.form['username']
    password = request.form['password']
    # password = generate_password_hash(password)
    user = User(username,password)
    session.add(user)
    session.commit()
    return redirect(url_for('index'))


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html', fl_session=fl_session)

@app.route('/login/checked', methods=['POST'])
def check_login():
    if request.method == 'POST':
        POST_USERNAME = str(request.form['username'])
        POST_PASSWORD = str(request.form['password'])
    else:
        return redirect(url_for('index'))
    
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]))
    result = query.first()
    if result:
        flash('good password!')
        fl_session['username'] = request.form['username']
        return redirect(url_for('add_data'))
    else:
        flash('wrong password!')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    fl_session.pop('username', None)
    return redirect(url_for('index'))