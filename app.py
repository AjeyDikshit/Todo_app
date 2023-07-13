from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.app_context().push()

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow   )

    def __repr__(self):
        return f"{self.sno} -> {self.title}"
    

@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']    
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()

    return render_template("index.html", allTodo=allTodo)

@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']    
        row = Todo.query.filter_by(sno=sno).first()
        row.title = title
        row.desc = desc
        db.session.commit()
        return redirect("/")

    row = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", row=row)

@app.route('/success/<int:sno>')
def completed(sno):
    completed = Todo.query.filter_by(sno=sno).first()
    db.session.delete(completed)
    db.session.commit()
    return redirect("/")

@app.route('/about')
def about_page():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)