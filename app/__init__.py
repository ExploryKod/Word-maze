from flask import Flask
from app.extensions import db
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
        db.create_all()

    return app