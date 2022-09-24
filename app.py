from flask import Flask
from flask import render_template
from flask import url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('welcome.html')

@app.route("/game")
def game():
    return render_template('game.html')


