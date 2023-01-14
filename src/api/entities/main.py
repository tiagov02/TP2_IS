import sys

from flask import Flask, jsonify, request
from entities.suicide import Suicide
import psycopg2

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access


app = Flask(__name__)
app.config["DEBUG"] = True



@app.route('/api/suicides/', methods=['GET'])
def get_suicides():
    suicides = []
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute("SELECT * from suicides")
    for result in cursor:
        s = Suicide(result[0],result[1],result[2],result[3],result[4],result[5],result[6],result[7],result[8],result [9],result[10],result[11])
        suicides.append(s)

    return jsonify([suicide for suicide in suicides])


@app.route('/api/suicides/create', methods=['POST'])
def create_suicides():
    data = request.get_json()
    print(data)
    suicide = Suicide()
    #suicides.append()
    return jsonify(data), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
