from __future__ import print_function
from flask import Flask, request

app = Flask(__name__)

@app.route("/authorize", methods=['GET', 'POST'])
def authorize():
    data = request.args
    print(data)

@app.route("/")
def home():
    return "Hello World"