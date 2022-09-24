from flask import Flask
from flask import render_template
from flask import url_for
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<name>")
def hello(name):
    return f"Hello, {escape(name)}!"

@app.route('/hello/')
@app.route('/hello/<name>')
def say_hello(name=None):
    return render_template('hello.html', name=name)