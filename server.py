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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)