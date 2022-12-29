from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///website.db"
db = SQLAlchemy(app)

#db is an object that gives access to the db.Model class tot define models, and the db.session to execute queries. 

#defining models: subclass db.Model to define a model class.
class Work(db.Model):
    #Columns in the table
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(600), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"

#creating the table:
# in python console,
# with app.app_context():
#   db.create_all()



#routes

#note: witnin a Flask view or CLI command, we can use db.session to execute queries and modify model data.

#SQLAlchemy automatically defines an __init__ method for each model that assigns any keyword arguments to corresponding database columns and other attributes.

#workflow: session->(to stage to commit)->commit

#CRUD in Flask-SQLAlchemy:
# - db.session.add(obj) adds an object to the session, to be inserted
# - Modifying an object's attributes updates the object. 
# - db.session.delete(obj) deletes an object.

# remember to call db.session.commit() after modifying, adding, or deleting any data.

#db.session.execute(db.select(..)) constructs a query to select data from the database. 


@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method=='POST':
        title=request.form['title']
        desc = request.form['desc']
        work = Work(title=title, desc=desc)
        db.session.add(work)
        db.session.commit()
    allWorks = Work.query.all()
    return render_template('index.html', allWorks=allWorks)


@app.route('/delete/<int:sno>')
def delete(sno):
    work = Work.query.filter_by(sno=sno).first()
    db.session.delete(work)
    db.session.commit()
    
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    #important
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        work = Work.query.filter_by(sno=sno).first()
        work.title=title
        work.desc=desc
        db.session.add(work)
        db.session.commit()
        return redirect('/')
        
    work = Work.query.filter_by(sno=sno).first()
    return render_template('update.html', work=work)

@app.route('/contact')
def contact():
    return 'Contact me anytime'

if __name__ == "__main__":
    app.run(debug=True)