#!/usr/bin/python3
"""
script that starts a Flask web application:
application must be listening on 0.0.0.0, port 5000
"""
from flask import Flask
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/')
def hello():
    "Returns hello HBNB"
    return 'Hello HBNB'


@app.route('/hbnb')
def hbnb():
    "Returns HBNB"
    return 'HBNB'


@app.route('/c/<text>')
def c(text):
    "Returns C ” followed by the value of the text"
    return 'C {}'.format(text.replace('_', ' '))


@app.route("/python/", defaults={"text": "is_cool"})
@app.route('/python/<text>')
def python(text):
    "Returns Python ” followed by the value of the text"
    return 'Python {}'.format(text.replace('_', ' '))


@app.route("/number/<int:n>")
def number(n):
    "Returns n only if its an integer else route not found"
    return "{:d} is a number".format(n)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
