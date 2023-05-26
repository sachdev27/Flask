from flask_sqlalchemy import SQLAlchemy
import string
import random
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(80),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.Text(),nullable=False)
    create_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
    bookmarks = db.relationship('Bookmark',backref="user")
    
    def __repr__(self) -> str:
        return f'USER >>> {self.username}'
    
class Bookmark(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    body = db.Column(db.Text,nullable=True)
    url = db.Column(db.Text,nullable=False)
    short_url = db.Column(db.String(3),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    visits = db.Column(db.Integer,default=0)
    create_at = db.Column(db.DateTime,default=datetime.now())
    updated_at = db.Column(db.DateTime,onupdate=datetime.now())
   
    def generate_short_url(self):
        characters = string.digits + string.ascii_letters
        picked_char = "".join(random.choices(characters,k=3))

        link = self.query.filter_by(short_url=picked_char).first()
        if link:
            return self.generate_short_url()
        else:
            return picked_char
        
        
        
        
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.short_url = generate_short_url()
        
    def __repr__(self) -> str:
        return f'Bookmark >>> {self.url}'   
 
    