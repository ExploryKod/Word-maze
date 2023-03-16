from flask import Flask
from app.extensions import db
from datetime import datetime, timedelta
from config import Config

# factory function
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
 
    # Initialize Flask extensions here
    db.init_app(app)
    
    # Register blueprints here
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.play import bp as play_bp
    app.register_blueprint(play_bp, url_prefix='/play')

    with app.app_context():
        app.secret_key ="13883755267d736867381d1a1c2533855759fd8bff429b5a504378194f9df049"
        app.permanent_session_lifetime = timedelta(minutes=60)
        app.debug = True
        db.create_all()

    return app