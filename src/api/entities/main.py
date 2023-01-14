import sys

from flask import Flask, jsonify, request
from entities.suicide import Suicide
from entities.country import Country
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
        s = Suicide(
            id=result[0],
            min_age=result[1],
            max_age=result[2],
            tax = result[3],
            population_no = result[4],
            suicides_no = result[5],
            generation = result[6],
            gdp_for_year = result[7],
            hdi_for_year = result[8],
            gdp_per_capita = result[9],
            year = result[10],
            id_country = result[11],
            created_on = result[12],
            updated_on = result[13]
        )
        suicides.append(s)

    return jsonify([suicide.__dict__ for suicide in suicides])


@app.route('/api/suicides/create', methods=['POST'])
def create_suicides():
    data = request.get_json()
    print(data)
    suicide = Suicide()
    #suicides.append()
    return jsonify(data), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
