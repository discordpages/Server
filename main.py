from __future__ import print_function;
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World";
