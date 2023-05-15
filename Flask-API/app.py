from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init Server
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite') #IMP
# For Warning 
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
#Init DB
db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.route('/',methods=['GET'])
def get():
    return jsonify({'msg':'Hello World!'})


# Product Class/Model
class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)
    
    def __init__(self,name,description,price,qty):
        self.name = name
        self.description = description
        self.price = price
        self.qty = qty

if __name__ == "__main__":
    app.run(debug=True)
    
