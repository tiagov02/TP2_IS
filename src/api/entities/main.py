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

#Because our database have too many registries we limit the consult to faster acess
@app.route('/api/suicides/<int:page>/<int:max_records>', methods=['GET'])
def get_suicides(page:int,max_records:int):
    suicides = []
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    offset = max_records * (page-1)
    cursor.execute(f"SELECT * from suicides ORDER year LIMIT {max_records} OFFSET {offset}")
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
    min_age = data['min_age']
    max_age = data['max_age']
    tax = data['tax']
    population_no = data['population_no']
    suicides_no = data['suicides_no']
    generation = data['generation']
    gpd_for_year = data['gdp_for_year']
    hdi_for_year = data['hdi_for_year']
    gdp_per_capita = data['gpd_per_capita']
    id_country = data['id_country']
    year = data['year']

    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()

    cursor.execute(f"insert into suicides (min_age, max_age, tax, population_no, suicides_no, generation, gdp_for_year, hdi_for_year, gdp_per_capita, year, id_country) "
                   f"values ({min_age}, {max_age}, {tax}, {population_no}, {suicides_no}, \'{generation}\', \'{gpd_for_year}\', {hdi_for_year}, {gdp_per_capita}, {year}, \'{id_country}\');")
    connection.commit()
    return jsonify(data), 201

@app.route('/api/suicides/update', methods=['POST'])
def update_suicide():
    data = request.get_json()
    id = data['id']
    min_age = data['min_age']
    max_age = data['max_age']
    tax = data['tax']
    population_no = data['population_no']
    suicides_no = data['suicides_no']
    generation = data['generation']
    gpd_for_year = data['gdp_for_year']
    hdi_for_year = data['hdi_for_year']
    gdp_per_capita = data['gpd_per_capita']
    id_country = data['id_country']
    year = data['year']

    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute(f"UPDATE suicides SET min_age={min_age}, max_age={max_age}, tax={tax}, population_no={population_no}, suicides_no={suicides_no}, "
                   f"generation=\'{generation}\', gdp_for_year=\'{gpd_for_year}\', hdi_for_year={hdi_for_year}, gdp_per_capita={gdp_per_capita}, id_country=\'{id_country}\',  "
                   f"year={year} WHERE id=\'{id}\'")

    cursor.execute(f"SELECT * from suicides WHERE id=\'{id}\'")
    result = cursor.fetchone()
    connection.commit()
    suicide = Suicide(
        id=result[0],
        min_age=result[1],
        max_age=result[2],
        tax=result[3],
        population_no=result[4],
        suicides_no=result[5],
        generation=result[6],
        gdp_for_year=result[7],
        hdi_for_year=result[8],
        gdp_per_capita=result[9],
        year=result[10],
        id_country=result[11],
        created_on=result[12],
        updated_on=result[13]
    )

    return jsonify([suicide.__dict__]),201


'''
COUNTRIES
'''

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

@app.route('/api/countries/to_update/<int:limit>', methods=['GET'])
def get_100_countries_to_update(limit:int):
    countries = []
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute(f"SELECT * from countries WHERE geom is null LIMIT {limit}")
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
    connection.commit()
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
    cursor.execute(f"UPDATE countries SET name=\'{name}\',geom = ST_MakePoint({lon}, {lat}),updated_on=now() WHERE id=\'{id}\'")
    cursor.execute(f"SELECT * from countries WHERE id=\'{id}\' ")
    first = cursor.fetchone()
    connection.commit()
    return jsonify(Country(
        id=first[0],
        name=first[1],
        geom=first[2],
        created_on=first[3],
        updated_on=first[4]
    ).__dict__),201


@app.route('/api/suicides/delete/<int:id>', methods=['GET'])
def delete_suicide(id:str):
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")
    cursor = connection.cursor()
    cursor.execute(f"DELETE FROM suicides WHERE id = {id}")
    connection.commit()
    return jsonify({'message': 'Suicide record deleted'}), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
