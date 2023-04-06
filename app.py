import os
import datetime
import time
from flask import Flask, render_template, request, url_for, redirect
from markupsafe import escape

# Flask app for web
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

