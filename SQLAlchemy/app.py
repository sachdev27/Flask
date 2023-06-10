from flask import Flask,g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database_many_many.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/',methods=['GET'])
def index():
    return "HELLO WORLD"


# class User(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(50))
#     email = db.Column(db.String(100),unique=True)
#     date_joined = db.Column(db.Date,default=datetime.utcnow)
    
#     def __repr__(self):
#         return f"<{self.id}, {self.name}, {self.email}, {self.date_joined}>"

user_channel = db.Table('user_channel',
            db.Column('user_id',db.Integer,db.ForeignKey('user.id')),            
            db.Column('channel_id',db.Integer,db.ForeignKey('channel.id')),            
            )

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    following = db.relationship('Channel',secondary=user_channel,backref='followers')
    
    def __repr__(self):
        return f"<User :  {self.name}>"
    
class Channel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    
    def __repr__(self):
        return f"<User :  {self.name}>"

if __name__ == "__main__":
    app.run(debug=True)