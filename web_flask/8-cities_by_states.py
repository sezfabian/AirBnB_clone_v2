#!/usr/bin/python3
"""
Script that starts a Flask web application:

Web application must be listening on 0.0.0.0, port 5000
Routes:
/cities_by_states: display a HTML page: (inside the tag BODY)
    - H1 tag: “States”
    - UL tag: with the list of all State objects present sorted by name
    - LI tag: description of one State: <state.id>: <B><state.name></B>
+ UL tag: with the list of City objects linked to the State sorted by name
    - LI tag: description of one City: <city.id>: <B><city.name></B>
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def cities_by_states():
    states_list = storage.all(State)
    sorted_list = sorted(states_list.values(), key=lambda state: state.name)

    return render_template("8-cities_by_states.html", states=sorted_list)


@app.teardown_appcontext
def teardown(exc):
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
