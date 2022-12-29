from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///website.db"
db = SQLAlchemy(app)


class Work(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(600), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self)->str:
        return f"{self.sno} - {self.title}"

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