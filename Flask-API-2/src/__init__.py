from flask import Flask,jsonify,redirect
import os
from src.database import db,Bookmark
from src.auth import auth
from src.bookmarks import bookmarks
from flask_jwt_extended import JWTManager 
from src.constants.http_status_codes import *

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
        
    
    @app.get('/<short_url>')
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()
        
        if bookmark:
            bookmark.visits = bookmark.visits+1
            db.session.commit()

            return redirect(bookmark.url)
    
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(exception):
        return jsonify({
            'Error' : 'Not Found'
        }),HTTP_404_NOT_FOUND
        
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_404(exception):
        return jsonify({
            'Error' : 'Server Error. We are working on it.'
        }),HTTP_500_INTERNAL_SERVER_ERROR
        

        
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
    

