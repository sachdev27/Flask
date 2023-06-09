# Flask SQLAlchemy

## Description

Flask SQLAlchemy is a Flask extension that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

## Installation

```bash
pip install Flask
pip install Flask-SQLAlchemy
```

## Usage

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

```

## Table of Contents

- Insertion, Deletion and Update
- Querying
- Relationships
- Migrations
- Pagination
- Flask-Admin
- Flask-Login
- Flask-Uploads
- Flask-RESTful
- Flask-RESTPlus
- Flask-RESTless
- Flask-REST-JSONAPI

## Insertion, Deletion and Update

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Insertion
admin = User(username='admin',email='test@email.com')
db.session.add(admin)
db.session.commit()

# Deletion
db.session.delete(admin)
db.session.commit()

# Update
admin.username = 'new_admin'
db.session.commit()
```

## Querying

```python
# Querying
User.query.all() # Return all users in the database
User.query.first() # Return the first user
User.query.filter_by(username='admin').all() # Return all users with username 'admin'
User.query.filter_by(username='admin').first() # Return the first user with username 'admin'
User.query.order_by(User.username).all() # Return all users ordered by username
User.query.limit(10).all() # Return the first 10 users
User.query.get(1) # Return the user with id 1
User.query.filter_by(username='admin').count() # Return the number of users with username 'admin'
```


