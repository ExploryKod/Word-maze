import os
from random import randint
from flask import Flask, request, redirect, abort, session, flash
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
# Import for Migrations
from words import chose_list, list_of_words
from letters import letter_blend

app = Flask(__name__)
app.debug = True

# adding configuration for using a sqlite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'game.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# Models
# May be a useless class 
class Letters(db.Model):
        # Id : Field which stores unique id for every row in
        # database table
        id = db.Column(db.Integer, primary_key=True)
        round_1 = db.Column(db.String(50), unique=False, nullable=True)
        round_2 = db.Column(db.String(50), unique=False, nullable=True)
        round_3 = db.Column(db.String(50), unique=False, nullable=True)
        secrets_id = db.relationship('Secrets', backref='letters', lazy='dynamic')
       
        def __repr__(self):
            return f"3 secrets words : {self.secret_1} {self.secret_2} {self.secret_3}"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), unique=False, nullable=True)
    guess = db.Column(db.String(150), unique=False, nullable=True)
    # Many answers and many scores for one user
    user_scores = db.relationship('Scores', backref='users', lazy='dynamic', cascade = "all, delete, delete-orphan")
    user_answers = db.relationship('Guess', backref='users', lazy='dynamic', cascade = "all, delete, delete-orphan")

class Secrets(db.Model):
        # Id : Field which stores unique id for every row in
        # database table
        id = db.Column(db.Integer, primary_key=True)
        secret_1 = db.Column(db.String(100), unique=False, nullable=False)
        secret_2 = db.Column(db.String(100), unique=False, nullable=False)
        secret_3 = db.Column(db.String(100), unique=False, nullable=False)
        # foreign key referring to the PK of a series of letters from the 3 words above
        letters_id = db.Column(db.Integer, db.ForeignKey('letters.id'))
        
        def __repr__(self):
            return f"Secrets : {self.secret_1} {self.secret_2} {self.secret_3}"

class Guess(db.Model):
    # Id : Field which stores unique id for every row in
    # database table
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(150), unique=False, nullable=False)
    # foreign key referring to the PK of Users (Many answers by user)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Answer : {self.word}"

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, unique=False, nullable=True)
    score_object = db.Column(db.String(150), unique=False, nullable=True)
    # foreign key referring to the PK of Users (Many scores by user) - FK is on the many side
    scores_id = db.Column(db.String, db.ForeignKey("users.id"))

with app.app_context():  # From SQLAlchemy 3.0 
    db.create_all()

# function to render index page
@app.route('/')
def index():
	# Query all data and then pass it to the template
    user_words = Guess.query.all()
    resp = Secrets.query.all()
    player = Users.query.all() 
    points = Scores.query.all()
    logout = False
    if not session.get('logged_in'):
        return render_template('index.html', user_words=user_words, resp=resp, player=player, points=points)
    else:
        return render_template('index.html', user_words=user_words, resp=resp, player=player, points=points)

@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    logout = True
    if not session.get('logged_in'):
        return render_template('login.html', logout=logout)
    else:
        logout = False
        return redirect('index.html')


@app.route('/login/checked', methods=['POST', 'GET'])
def check_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        session['logged_in'] = True
        return render_template('play.html', logout=logout)
    else:
        flash('wrong password!')
        return render_template('login.html', logout=logout)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@app.route('/add_data')
def add_data():
    is_a_turn = False
    round_num = randint(1,3)
    db.session.query(Secrets).delete()
    db.session.query(Guess).delete()
    db.session.query(Letters).delete()
    db.session.commit()
    base_list = chose_list(round_num)
    secret_words = list_of_words(base_list)
    
    if secret_words != '':
        letters = letter_blend(secret_words)
        blend_words = Letters(round_1=letters) 
        secret_1 = secret_words[0]
        secret_2 = secret_words[1]
        secret_3 = secret_words[2]
        first = Secrets(secret_1=secret_1, secret_2=secret_2,secret_3=secret_3)
        db.session.add(first)
        db.session.add(blend_words)
        db.session.commit()
            
    words_star = Secrets.query.all()

    return render_template('play.html', letters=letters, secret_words=secret_words, word_1=secret_1,word_2=secret_2,word_3=secret_3,first=first, words_star=words_star, is_a_turn = is_a_turn, blend_words=blend_words)

@app.route('/turn')
def turns():
    words_star = Secrets.query.all()
    blend_words = Letters.query.all()
    is_a_turn = True
    return render_template('play.html', words_star=words_star, is_a_turn = is_a_turn, blend_words=blend_words)

# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
	
    word = request.form.get("word")
    pseudo = request.form.get("pseudo")
    words_star = Secrets.query.all()
    if word == words_star[-1].secret_1 or word == words_star[-1].secret_2 or word == words_star[-1].secret_3:
        point = 1
    else:
        point = 0
    db.session.query(Guess).delete()
    db.session.commit()
	# create an object of the Guess class of models
	# and store data as a row in our datatable
    if word != '' and pseudo != '':
        answ = Guess(word=word, user_id=pseudo)
        you = Users(pseudo=pseudo, guess=word)
        # encore faudra t-il créer la relation (scores_id (FK) => PK de Users via users_scores rel)
        points = Scores(score=point,score_object=word, scores_id = pseudo)
        db.session.add(answ)
        db.session.add(you)
        db.session.add(points)
        db.session.commit()
        return redirect('/')
    elif word != words_star:
        return render_template('index.html', words_star=words_star, word=word)
    else:
	    return redirect('/')

@app.route('/delete/<int:id>')
def erase(id):
	# Deletes the data on the basis of unique id and
	# redirects to home page
	data = Guess.query.get(id)
	db.session.delete(data)
	db.session.commit()
	return redirect('/')

@app.route('/delete_all/<int:id>')
def delete_all(id):
    data = Secrets.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)


