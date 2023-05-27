from flask import Blueprint,request,jsonify
from werkzeug import generate_password_hash,check_password_hash
from src.constants.http_status_codes import *
import validators
from src.database import User,db

auth = Blueprint("auth",__name__,url_prefix="/api/v1/auth")


@auth.post("/register")
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']
    
    if len(password) < 6:
        return jsonify({
            'error' : 'Password is too short'
        }),HTTP_400_BAD_REQUEST
        
    if len(username) < 3:
        return jsonify({
            'error' : 'Username is too short'
        }),HTTP_400_BAD_REQUEST
        
    if not username.isalnum() or " " in username:
        return jsonify({
            'error' : 'Username should be alpha numeric and should not contain space'
        }),HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({
            'error' : 'Email is not valid.'
        }),HTTP_400_BAD_REQUEST  

    if User.query.filter_by(email=email).first() is not None:
         return jsonify({
            'error' : 'Email is taken.'
        }),HTTP_409_CONFLICT   
               
    if User.query.filter_by(username=username).first() is not None:
         return jsonify({
            'error' : 'Username is taken.'
        }),HTTP_409_CONFLICT    
         
         
    pwd_hash = generate_password_hash(password=password)
    
    # Creating a User oject of Database Model
    user = User(username=username,password=pwd_hash,email=email)
    
    # Adding the user to the database 
    db.session.add(user)
    # Saving the change in database
    db.commit()
    
    
    
    return jsonify({
        "message" : "User is created",
        "user" : {
           'username' : username,
           "email" : email
        }
    }), HTTP_201_CREATED
    
    
        



@auth.get("/me") 
def me():
    return {"user":"me"}