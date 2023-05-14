from flask import Flask,render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # Form input Name tag
        new_task = Todo(content = task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/") 
        except:
            return "Error creating new task."
        
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html',tasks = tasks) # IMP

if __name__ ==  '__main__':
    app.run(debug=True)
    
# From Shell
# from app import db,app
# app.app_context().push()
# db_create_all()    

    
