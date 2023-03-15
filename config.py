import os

basedir = os.path.abspath(os.path.dirname(__file__))
# app.secret_key ="13883755267d736867381d1a1c2533855759fd8bff429b5a504378194f9df049"
# app.permanent_session_lifetime = timedelta(minutes=60)

class Config:
    DEBUG=True
    # adding configuration for using a sqlite database
    SECRET_KEY = os.environ.get('SECRET KEY')
    # app.config['SQLALCHEMY_DATABASE_URI'] =\
    #         'sqlite:///' + os.path.join(basedir, 'game.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'game.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Creating an SQLAlchemy instance
    # db = SQLAlchemy(app)