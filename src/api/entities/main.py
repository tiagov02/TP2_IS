import sys

from flask import Flask, jsonify, request

from entities.suicide import Suicide

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access


app = Flask(__name__)
app.config["DEBUG"] = True

suicides=[
    Suicide(name="Nome1")
]


@app.route('/api/suicides/', methods=['GET'])
def get_suicides():
    return jsonify([suicide.__dict__ for suicide in suicides])


@app.route('/api/suicides/', methods=['POST'])
def create_suicides():
    data = request.get_json()
    suicide = Suicide(name=data['name'])
    suicides.append(suicide)
    return jsonify(suicide.__dict__), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
