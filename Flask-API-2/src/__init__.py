from flask import Flask
import os
from src.database import db
from src.auth import auth
from src.bookmarks import bookmarks
from flask_jwt_extended import JWTManager 

# Create the application factory function
def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__,instance_relative_config=True) 
    
    # instance_relative_config=True tells the app that configuration files are relative to the instance folder.
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI"),
            JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
        )
    else:
        app.config.from_mapping(test_config)
        # Load the instance config, if it exists, when not testing
        
    @app.route("/")
    def index():
        return "Hello World"


    @app.route("/home")
    def home():
        return {"message":"Hello World!"}

    
    # Initialize the database
    db.app = app
    db.init_app(app)
    
    
    # JWT Manager
    # JWTManager is used to handle the creation and verification of JSON Web Tokens.
    JWTManager(app)
    
    # What are Blue print ?
    # Blueprints are a way to organize related routes in a Flask application.
    # Blueprints are registered with the Flask application object.
    # Blueprints are created with a name and import name.
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)
    
    return app
    

