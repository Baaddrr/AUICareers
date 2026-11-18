from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .login_manager import login_manager  # Import the login_manager
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # Initialize the login manager with the Flask app
    login_manager.init_app(app)
    
    # Configure Flask-Login login_view to the login route
    login_manager.login_view = "main.login"  # You can change this to the correct login route if it's different

    # Register other blueprints if needed (e.g., main)
    from .routes import main
    app.register_blueprint(main)

    # Optionally, register the auth blueprint (if you've separated it into a separate blueprint)
    # from .auth.routes import auth
    # app.register_blueprint(auth)

    return app
