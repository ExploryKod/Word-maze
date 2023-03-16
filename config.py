import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # adding configuration for using a sqlite database
    SECRET_KEY = os.environ.get('SECRET KEY')
    # app.config['SQLALCHEMY_DATABASE_URI'] =\
    #         'sqlite:///' + os.path.join(basedir, 'game.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')\
        or 'sqlite:///' + os.path.join(basedir, 'game.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Creating an SQLAlchemy instance
    # db = SQLAlchemy(app)