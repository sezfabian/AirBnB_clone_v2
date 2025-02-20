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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
