# Flask SQLAlchemy

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
Output: [<User 'admin'>, <User 'guest'>]

User.query.first() # Return the first user
Output: <User 'admin'>

User.query.filter_by(username='admin').all() # Return all users with username 'admin'
Output: [<User 'admin'>]

User.query.filter_by(username='admin').first() # Return the first user with username 'admin'
Output: <User 'admin'>

User.query.order_by(User.username).all() # Return all users ordered by username
Output: [<User 'admin'>, <User 'guest'>]

User.query.limit(10).all() # Return the first 10 users
Output: [<User 'admin'>, <User 'guest'>]    

User.query.get(1) # Return the user with id 1
Output: <User 'admin'>

User.query.filter_by(username='admin').count() # Return the number of users with username 'admin'
Output: 1
```

```python

# Using filter
User.query.filter(User.username.like('%dmin%')).all() # Return all users with username containing 'dmin'
Output: [<User 'admin'>]

User.query.filter(User.username.like('Ad%')).all() # Return all users with username starting with 'Ad'
Output: [<User 'admin'>]

User.query.filter(User.username == 'admin').all() # Return all users with username 'admin'
Output: [<User 'admin'>]
```

```python
# Using or
from sqlalchemy import or_
User.query.filter(or_(User.username == 'admin', User.username == 'guest')).all() # Return all users with username 'admin' or 'guest'
Output: [<User 'admin'>, <User 'guest'>]    

# Using and
from sqlalchemy import and_
User.query.filter(and_(User.username == 'admin', User.email == 'test@example.com')).all() # Return all users with username 'admin' and email 'test@example'
Output: [<User 'admin'>]

# Using not
from sqlalchemy import not_
User.query.filter(not_(User.username == 'admin')).all() # Return all users with username not equal to 'admin'
Output: [<User 'guest'>]

# Using in
User.query.filter(User.username.in_(['admin', 'guest'])).all() # Return all users with username in the list ['admin', 'guest']
Output: [<User 'admin'>, <User 'guest'>]

```

```python

Data in database
id  username email date_joined
# 1	Sandesh Sachdev sandeshsachdev27@gmail.com	2023-06-09
# 2	Rahul Goel	rahulagoel1@gmail.com	2023-06-09
# 3	Yash Thakre	yashthakre@gmail.com	2022-02-14
# 4	Hevesh Lakhwani	hevesh001@gmail.com	2021-10-08
# 5	Henay Lakhwani	lakhwanih@gmail.com	2018-05-01

# Datetime 
from datetime import datetime
User.query.filter(User.date_joined.between('2016-01-01 00:00:00', '2021-01-31 23:59:59')).all() # Return all users with date_joined between 2016-01-01 and 2021-01-31
Output: [<5, Henay Lakhwani, lakhwanih@gmail.com, 2018-05-01>]

User.query.filter(User.date_joined > date(2020,1,1)).order_by(User.name.asc()).all() # Return all users with date_joined after 2020-01-01 ordered by name ascending
Output: [<4, Hevesh Lakhwani, hevesh001@gmail.com, 2021-10-08>, <2, Rahul Goel, rahulagoel1@gmail.com, 2023-06-09>, <1, Sandesh Sachdev, sandeshsachdev27@gmail.com, 2023-06-09>, <3, Yash Thakre, yashthakre@gmail.com, 2022-02-14>]

### Adding data into Varibale
user_joined = User.query.filter(User.date_joined > date(2020,1,1)).order_by(User.name.asc()).all()

For user in user_joined:
    print(user.name)

Output: Hevesh Lakhwani
        Rahul Goel
        Sandesh Sachdev
        Yash Thakre
```

## Checking Constraints

```python
# Checking Constraints in Model

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, check="username != 'admin'")
    email = db.Column(db.String(120), unique=True, nullable=False, db.CheckConstraint('email != "'))
    date_joined = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username


## One to Many Relationship

```python

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    posts = db.relationship('Post',backref='author')
    
    def __repr__(self):
        return f"<User :  {self.name}>"

class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f"<Post :  {self.title}>"

Output
>>> user1 = User(name='Sandesh')
>>> user2 = User(name='Rahul')
>>> user3 = User(name='Yash')
>>> user4 = User(name='Hevesh')
>>> user5 = User(name='Henay')
>>> post1 = Post(title='Python',content='Python is a programming language',author=user1)
>>> post2 = Post(title='Flask',content='Flask is a web framework',author=user1)
>>> post3 = Post(title='SQLAlchemy',content='SQLAlchemy is a ORM',author=user1)
>>> post4 = Post(title='Django',content='Django is a web framework',author=user1)
>>> post5 = Post(title='FastAPI',content='FastAPI is a web framework',author=user1)
>>> post6 = Post(title='PyTorch',content='PyTorch is a deep learning framework',author=user1)


>>> db.session.add([user1,user2,user3,user4,user5])
>>> db.session.commit()

>>> user1.posts
[<Post :  Python>, <Post :  Flask>, <Post :  SQLAlchemy>, <Post :  Django>, <Post :  FastAPI>, <Post :  PyTorch>]

>>> user2.posts
[]

>>> user3.posts
[]

>>> user4.posts
[]
```

## Many to Many Relationship

```python
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


Output
>>> user1 = User(name='Sandesh')
>>> user2 = User(name='Rahul')
>>> user3 = User(name='Yash')
>>> user4 = User(name='Hevesh')
>>> user5 = User(name='Henay')
>>> channel1 = Channel(name='Python')
>>> channel2 = Channel(name='Flask')
>>> channel3 = Channel(name='SQLAlchemy')
>>> channel4 = Channel(name='Django')
>>> channel5 = Channel(name='FastAPI')
>>> channel6 = Channel(name='PyTorch')
>>> channel7 = Channel(name='Tensorflow')
>>> channel8 = Channel(name='Keras')

>>> user1.following.append(channel1)
>>> user1.following.append(channel2)
>>> user1.following.append(channel3)
>>> user1.following.append(channel4)

>>> user2.following.append(channel1)
>>> user2.following.append(channel2)

>>> user3.following.append(channel1)
>>> user3.following.append(channel2)
>>> user3.following.append(channel3)

>>> user4.following.append(channel1)
>>> user4.following.append(channel2)
>>> user4.following.append(channel3)
>>> user4.following.append(channel4)

>>> user5.following.append(channel1)

>>> db.session.add([user1,user2,user3,user4,user5])
>>> db.session.commit()

>>> user1.following
[<Channel :  Python>, <Channel :  Flask>, <Channel :  SQLAlchemy>, <Channel :  Django>]

>>> channel1.followers
[<User :  Sandesh>, <User :  Rahul>, <User :  Yash>, <User :  Hevesh>, <User :  Henay>]

>>> channel2.followers
[<User :  Sandesh>, <User :  Rahul>, <User :  Yash>, <User :  Hevesh>]

>>> channel3.followers
[<User :  Sandesh>, <User :  Yash>, <User :  Hevesh>]

>>> channel4.followers
[<User :  Sandesh>, <User :  Hevesh>]

>>> channel5.followers
[]

>>> channel6.followers
[]

>>> channel7.followers
[]


# Removing data from Many to Many Relationship

>>> user1.following.remove(channel1)
>>> user1.following.remove(channel2)


>>> user1.following
[<Channel :  SQLAlchemy>, <Channel :  Django>]


```

## Executing Custom SQL Queries

```python

# Executing Custom SQL Queries
db.session.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)')
db.session.execute('INSERT INTO users (name) VALUES (:name)', {'name': 'admin'})

# Executing Custom SQL Queries with Result
result = db.session.execute('SELECT * FROM users')
for row in result:
    print(row)

```

## Using Different Schemas

```Python
class User(db.Model):
    __tablename__ = 'users' 
    __table_args__ = {'schema': 'test'} 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()
```

## Using Multiple Databases

```python
app = Flask(__name__)

app.config['SQLALCHEMY_BINDS'] = {
    'users':        'sqlite:///users.sqlite3',
    'appmeta':      'sqlite:///appmeta.sqlite3'
}

db = SQLAlchemy(app)

class User(db.Model):
    __bind_key__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class AppMeta(db.Model):
    __bind_key__ = 'appmeta'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    value = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<AppMeta %r>' % self.name

db.create_all()

```

