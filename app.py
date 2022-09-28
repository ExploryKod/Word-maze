from random import randint
from flask import Flask, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import delete
# Import for Migrations

from words import chose_list, list_of_words
from letters import letter_blend

app = Flask(__name__)
app.debug = True

# adding configuration for using a sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'

# Creating an SQLAlchemy instance
db = SQLAlchemy(app)


# Models
class Guess(db.Model):
	# Id : Field which stores unique id for every row in
	# database table
	id = db.Column(db.Integer, primary_key=True)
	word = db.Column(db.String(50), unique=False, nullable=False)

	# repr method represents how one object of this datatable
	# will look like
	def __repr__(self):
		return f"Word : {self.word}"

class Secrets(db.Model):
        # Id : Field which stores unique id for every row in
        # database table
        id = db.Column(db.Integer, primary_key=True)
        secret_1 = db.Column(db.String(50), unique=False, nullable=False)
        secret_2 = db.Column(db.String(50), unique=False, nullable=False)
        secret_3 = db.Column(db.String(50), unique=False, nullable=False)

        # repr method represents how one object of this datatable
        # will look like
        def __repr__(self):
            return f"Secrets : {self.secret_1} {self.secret_2} {self.secret_3}"

class Letters(db.Model):
        # Id : Field which stores unique id for every row in
        # database table
        id = db.Column(db.Integer, primary_key=True)
        round_1 = db.Column(db.String(50), unique=False, nullable=False)
        round_2 = db.Column(db.String(50), unique=False, nullable=False)
        round_3 = db.Column(db.String(50), unique=False, nullable=False)

        # repr method represents how one object of this datatable
        # will look like
        def __repr__(self):
            return f"Word : {self.secret_1} {self.secret_2} {self.secret_3}"

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pseudo = db.Column(db.String(50), unique=True, nullable=True)

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.String(50), unique=True, nullable=True)

class Rounds(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.String(50), unique=True, nullable=True)

# function to render index page
@app.route('/')
def index():
	# Query all data and then pass it to the template
    user_words = Guess.query.all()
    resp = Secrets.query.all()
    return render_template('index.html', user_words=user_words, resp=resp)

@app.route('/add_data')
def add_data():
    is_a_turn = False
    round_num = randint(1,3)
    db.session.query(Secrets).delete()
    db.session.query(Guess).delete()
    db.session.commit()
    base_list = chose_list(round_num)
    secret_words = list_of_words(base_list)  
    if secret_words != '':
        secret_1 = secret_words[0]
        secret_2 = secret_words[1]
        secret_3 = secret_words[2]
        first = Secrets(secret_1=secret_1, secret_2=secret_2,secret_3=secret_3)
        db.session.add(first)
        db.session.commit()
            
      
        letters = letter_blend(secret_words)
    words_star = Secrets.query.all()

    return render_template('play.html', letters=letters, secret_words=secret_words, word_1=secret_1,word_2=secret_2,word_3=secret_3,first=first, words_star=words_star, is_a_turn = is_a_turn)


@app.route('/turn')
def turns():
    words_star = Secrets.query.all()
    is_a_turn = True
    return render_template('play.html', words_star=words_star, is_a_turn = is_a_turn)

# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
	
	# In this function we will input data from the
	# form page and store it in our database.
	# Remember that inside the get the name should
	# exactly be the same as that in the html
	# input fields
    word = request.form.get("word")
    words_star = Secrets.query.all()

	# create an object of the Guess class of models
	# and store data as a row in our datatable
    if word != '':
        p = Guess(word=word)
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    elif word != words_star:
        return render_template('index.html', words_star=words_star)
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
	app.run()


