# Flask SQLAlchemy

## Description

Flask SQLAlchemy is a Flask extension that adds support for SQLAlchemy to your application. It aims to simplify using SQLAlchemy with Flask by providing useful defaults and extra helpers that make it easier to accomplish common tasks.

## References

- [Flask SQLAlchemy by PrettyPrinted](https://www.youtube.com/@prettyprinted)

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

# Using filter
User.query.filter(User.username.like('%dmin%')).all() # Return all users with username containing 'dmin'
User.query.filter(User.username.like('Ad%')).all() # Return all users with username starting with 'Ad'
User.query.filter(User.username == 'admin').all() # Return all users with username 'admin'

# Using or
from sqlalchemy import or_
User.query.filter(or_(User.username == 'admin', User.username == 'guest')).all() # Return all users with username 'admin' or 'guest'

# Using and
from sqlalchemy import and_
User.query.filter(and_(User.username == 'admin', User.email == 'test@example.com')).all() # Return all users with username 'admin' and email 'test@example'

# Using not
from sqlalchemy import not_
User.query.filter(not_(User.username == 'admin')).all() # Return all users with username not equal to 'admin'

# Using in
User.query.filter(User.username.in_(['admin', 'guest'])).all() # Return all users with username in the list ['admin', 'guest']

# Datetime 
from datetime import datetime
User.query.filter(User.last_seen.between('2016-01-01 00:00:00', '2016-01-31 23:59:59')).all() # Return all users with last_seen between 2016-01-01 and 2016-01-31

User.query.filter(User.last_seen.between(datetime(2016, 1, 1), datetime(2016, 1, 31))).all() # Return all users with last_seen between 2016-01-01 and 2016-01-31

User.query.filter(User.date_joined > date(2020,1,1)).order_by(User.name.asc()).all() # Return all users with date_joined after 2020-01-01 ordered by name ascending

### Adding data into Varibale
user_joined = User.query.filter(User.date_joined > date(2020,1,1)).order_by(User.name.asc()).all()

For user in user_joined:
    print(user.name)
```

