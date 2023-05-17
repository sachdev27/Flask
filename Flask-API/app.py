from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init Server
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite') #IMP
# For Warning 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#Init DB
db = SQLAlchemy(app) # Intialized Database
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

# Product Schema
class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id','name','description','price','qty')

# Why do we need a schema?
# A schema is used to define how the data will be represented when it is returned as a response.
# For example, we can specify which fields we want to be returned, or if we want to add any additional fields.

# Init Schema
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)

# Add Product

@app.route('/product',methods=['POST'])
def add_product():
    name = request.json['name'] 
    description = request.json['description'] 
    price = request.json['price'] 
    qty = request.json['qty'] 
    
    new_product = Product(name,description,price,qty) 
    
    db.session.add(new_product) 
    db.session.commit() 
    
    return product_schema.jsonify(new_product) 

@app.route('/product',methods=['GET'])
def get_products():
    all_products = Product.query.all()
    result = products_schema.dump(all_products)
    return jsonify(result)

@app.route('/product/<id>',methods=['GET'])
def get_product(id):
    single_product = Product.query.get(id)
    return product_schema.jsonify(single_product)

#  Run Server
if __name__ == "__main__":
    app.run(debug=True)
    
# Create Database from Terminal
# >>> from app import app, db
# >>> app.app_context().push()
# >>> db.create_all()