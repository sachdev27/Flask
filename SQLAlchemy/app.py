from flask import Flask,g,render_template
from flask_sqlalchemy import SQLAlchemy,pagination
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_many_many.sqlite3"
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_pagination.sqlite3"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    # following = db.relationship('Channel',secondary=user_channel,backref='followers')
    
    def __repr__(self):
        return f"<User :  {self.name}>"
    
    

@app.route('/',methods=['GET'])
def index():
    return "HELLO WORLD"

@app.route("/user/<int:id>")
def user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        return f"User {id} Exists"
    
    else:
        return f"User {id} does not exist"
    
@app.get("/users/<int:page_num>")
def getusers(page_num):
    users = User.query.paginate(page=page_num,per_page=10)
    return render_template('page.html',users=users)
  

class Customer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    orders = db.relationship('Order',backref='customer',lazy=True) # Relationship with Order table ( one to many)
    
class Order(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    customer_id = db.Column(db.Integer,db.ForeignKey('customer.id'),nullable=False) # Relationship with Customer table ( many to one)
    price = db.Column(db.Integer)

if __name__ == "__main__":
    app.run(debug=True)
