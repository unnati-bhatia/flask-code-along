from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db=SQLAlchemy(app)

class ToDo(db.Model):
    Sno= db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False) 
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.Sno} - {self.title}" 

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title =request.form['title']
        desc =request.form['desc']
        todo=ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    allTodo=ToDo.query.all()
    return render_template('index.html', allTodo=allTodo)
    #return 'Hello World!'
    
@app.route('/show')
def products():
    allTodo=ToDo.query.all()
    print(allTodo)
    return 'This is products page'



@app.route('/update/<int:Sno>', methods=['GET', 'POST'])
def update(Sno):
    if request.method=='POST':
        title =request.form['title']
        desc =request.form['desc']
        todo=ToDo.query.filter_by(Sno=Sno).first()
        todo.title=title
        todo.desc=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=ToDo.query.filter_by(Sno=Sno).first()
    return render_template('update.html', todo=todo)


@app.route('/delete/<int:Sno>')
def delete(Sno):
    
    Todo=ToDo.query.filter_by(Sno=Sno).first()
    db.session.delete(Todo)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True, port=8000)