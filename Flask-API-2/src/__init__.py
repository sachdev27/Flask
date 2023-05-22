from flask import Flask
import os

# Create the application factory function
def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__,instance_relative_config=True) 
    
    # instance_relative_config=True tells the app that configuration files are relative to the instance folder.
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = os.environ.get("SECRET_KEY")
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

    
    return app
    

