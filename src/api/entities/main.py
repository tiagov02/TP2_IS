import sys

from flask import Flask, jsonify, request,abort
from entities.suicide import Suicide
from entities.country import Country
import psycopg2

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access


app = Flask(__name__)
app.config["DEBUG"] = True

# SUICIDES

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

@app.route('/api/suicides/<string:id>', methods=['GET'])
def get_suicide(id:str):
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute(f"SELECT * from suicides WHERE id=\'{id}\'")
    result = cursor.fetchone()
    suicide = Suicide(
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

    return jsonify([suicide.__dict__])


@app.route('/api/suicides/create', methods=['POST'])
def create_suicides():
    data = request.get_json()
    print(data)
    #suicide = Suicide()
    #suicides.append()
    return jsonify(data), 201


@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = []
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute("SELECT * from countries")
    for result in cursor:
        countries.append(Country(
            id=result[0],
            name=result[1],
            geom=result[2],
            created_on=result[3],
            updated_on=result[4]
        ))
    return jsonify([country.__dict__ for country in countries])

@app.route('/api/countries/<string:id>', methods=['GET'])
def get_country(id:str):
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute(f"SELECT * from countries WHERE id=\'{id}\' ")
    first = cursor.fetchone()
    return jsonify(Country(
        id=first[0],
        name=first[1],
        geom=first[2],
        created_on=first[3],
        updated_on=first[4]
    ).__dict__),200

@app.route('/api/countries/to_update', methods=['GET'])
def get_100_countries_to_update():
    countries = []
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute("SELECT * from countries WHERE geom is null LIMIT 100")
    for result in cursor:
        countries.append(Country(
            id=result[0],
            name=result[1],
            geom=result[2],
            created_on=result[3],
            updated_on=result[4]
        ))
    return jsonify([country.__dict__ for country in countries])

@app.route('/api/countries/create',methods=['POST'])
def create_country():
    data = request.get_json()
    name = data['name']

    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute(f"insert into countries (name) values (\'{name}\') RETURNING id")
    new_id = cursor.fetchone()[0]
    if new_id is not None:
        return get_country(new_id)
    else:
        abort(500)

@app.route('/api/countries/update',methods=['POST'])
def update_country():
    data = request.get_json()
    id = data['id']
    name = data['name']
    lat = data['lat']
    lon = data['lon']

    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")
    cursor = connection.cursor()
    cursor.execute(f"UPDATE countries SET name=\'{name}\',geom = ST_MakePoint({lon}, {lat}) WHERE id=\'{id}\'")
    cursor.execute(f"SELECT * from countries WHERE id=\'{id}\' ")
    first = cursor.fetchone()
    return jsonify(Country(
        id=first[0],
        name=first[1],
        geom=first[2],
        created_on=first[3],
        updated_on=first[4]
    ).__dict__),201



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
