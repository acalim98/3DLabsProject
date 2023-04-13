import os
import datetime
import time
from flask import Flask, render_template, request, url_for, redirect
from markupsafe import escape
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

# Flask app for web
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
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




class MyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route('/form', methods=['GET', 'POST'])
def form():
    form = MyForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            name = form.name.data
            message = form.message.data
            return redirect(url_for('success'))
    return render_template('form.html', form=form)

@app.route('/success')
def success():
    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)
