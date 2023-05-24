#!/usr/bin/python3
"""
Script that starts a Flask web application:
Web application must be listening on 0.0.0.0, port 5000
Routes:
/states_list: display a HTML page: (inside the tag BODY)
       - H1 tag: “States”
       - UL tag: with the list of all State objects sorted by name
       - LI tag: description of one State: <state.id>: <B><state.name></B>
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    states_list = storage.all(State)
    sorted_list = sorted(states_list.values(), key=lambda state: state.name)

    return render_template("7-states_list.html", states=sorted_list)


@app.teardown_appcontext
def teardown(td):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
