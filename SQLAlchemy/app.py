from flask import Flask,g
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/',methods=['GET'])
def index():
    return "HELLO WORLD"


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100),unique=True)
    date_joined = db.Column(db.Date,default=datetime.utcnow)
    
    def __repr__(self):
        return f"<{self.id}, {self.name}, {self.email}, {self.date_joined}>"

if __name__ == "__main__":
    app.run(debug=True)