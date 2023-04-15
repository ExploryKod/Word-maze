from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

engine = create_engine('sqlite:///auth.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)

    def __init__(self, username, password):
        self.username = username
        self.password = password

# Vérifie si la table existe déjà dans la base de données
inspector = inspect(engine)
if not inspector.has_table('users'):
    # Crée la table si elle n'existe pas
    Base.metadata.create_all(engine)

