import os
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import task_utils

db = SQLAlchemy()
# Flask app for web
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

# create instance of database object
db = SQLAlchemy(app)
#db.init_app(app)

# create Todo table in database
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    new = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f'<Todo {self.id}>'

    def add_random_todos():
        for _ in range(10):
            new_todo = Todo(content=f'Task with ID')
            db.session.add(new_todo)

    db.session.commit()

@app.route('/addtodo', methods=['GET', 'POST'])
def addtodo():
    new_todo = Todo(content=f'Task with ID')
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for('todos'))


@app.route("/add_random_todos")
def add_random_todos_route():
    add_random_todos()
    return "Added 10 random todos."

@app.route("/create_db")
def create_db():
    with app.app_context():
        db.create_all()

    return "Database created."

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/base")
def base():
    return render_template('base.html')

@app.route("/example")
def example():
    text = 'Hello, World! This is an example page!'
    return render_template('example.html', text=text)

@app.route("/link")
def my_link():
    my_link_text = "This is a link!"
    return render_template('example_link.html', text=my_link_text)

@app.route('/todos', methods=['GET', 'POST'])
def todos():
    todos = Todo.query.all()
    return render_template('todos.html', todos=todos)

@app.route('/todos/edit/<int:todo_id>', methods=['GET', 'POST'])
def edit_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    if request.method == 'POST':
        todo.content = request.form['content']
        db.session.commit()
        return redirect(url_for('todos'))
    return render_template('edit_todo.html', todo=todo)

@app.route('/todos/delete/<int:todo_id>')
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('todos'))