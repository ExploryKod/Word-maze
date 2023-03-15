from flask import Blueprint

bp = Blueprint('play', __name__)


from app.play import routes