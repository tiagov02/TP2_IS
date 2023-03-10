import sys

from flask import Flask, jsonify, request,abort
from flask_cors import CORS
from entities.suicide import Suicide
from entities.country import Country
from entities.year import Year
import psycopg2

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

# set of all teams
# !TODO: replace by database access


app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

# SUICIDES

#Because our database have too many registries we limit the consult to faster acess

# conexão à base de dados
def connectToDB():
    return psycopg2.connect(user="is",password="is",host="db-rel",database="is")


#GET that return the year(distict for only repeat one year once)
@app.route('/api/years', methods=['GET'])
def get_years():

    ret = []
    connection = connectToDB()
    cursor = connection.cursor()

    cursor.execute(f"SELECT distinct year from suicides "
                   f"ORDER BY year asc; ")
    for res in cursor:
        ret.append(Year(year=res[0]))

    return jsonify([year.__dict__ for year in ret])



#GET that returns the suicides number for help in frontend to do the pagination
@app.route('/api/suicides/number', methods=['GET'])
def get_number_suicides():

    connection = connectToDB()
    cursor = connection.cursor()

    cursor.execute(f"SELECT COUNT(*) from suicides")
    result = cursor.fetchone()

    return [{
        "no_registries": result[0]
    }]


# GET that returns the suicides and respective countries, per page( bacause we have too many registries in the database)
@app.route('/api/suicides/per_page/<int:page>/<int:max_records>', methods=['GET'])
def get_suicides(page:int,max_records:int):
    suicides = []

    connection = connectToDB()

    cursor = connection.cursor()
    offset = max_records * (page-1)
    cursor.execute(f"SELECT s.*,c.* from suicides s, countries c WHERE s.id_country=c.id "
                   f"ORDER BY year LIMIT {max_records} OFFSET {offset} ")

    for result in cursor:
        c = Country(
            id=result[15],
            name=result[16],
            geom=result[17],
            created_on=result[18],
            updated_on=result[19]
        ).__dict__

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
            country= c,
            created_on = result[12],
            updated_on = result[13],
            sex = result[14]
        )
        suicides.append(s)

    return jsonify([suicide.__dict__ for suicide in suicides])


# GET that returns the suicide by Id
@app.route('/api/suicides/by_id/<string:id>', methods=['GET'])
def get_suicide(id:str):

    connection = connectToDB()
    cursor = connection.cursor()

    cursor.execute(f"SELECT s.*,c.* from suicides s, countries c WHERE id=\'{id}\' AND s.id_country=c.id ORDER by s.year and c.name")
    result = cursor.fetchone()

    c = Country(
        id=result[15],
        name=result[16],
        geom=result[17],
        created_on=result[18],
        updated_on=result[19]
    ).__dict__
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
        country=c,
        created_on = result[12],
        updated_on = result[13],
        sex = result[14]
        )

    return jsonify([suicide.__dict__])


# POST that create one suicide(receiving a JSON)
@app.route('/api/suicides/create', methods=['POST'])
def create_suicides():
    connection = connectToDB()

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

    cursor = connection.cursor()

    cursor.execute(f"insert into suicides (min_age, max_age, tax, population_no, suicides_no, generation, gdp_for_year, hdi_for_year, gdp_per_capita, year, id_country) "
                   f"values ({min_age}, {max_age}, {tax}, {population_no}, {suicides_no}, \'{generation}\', \'{gpd_for_year}\', {hdi_for_year}, {gdp_per_capita}, {year}, \'{id_country}\');")
    connection.commit()
    return jsonify(data), 201


# POST that update one suicide(receiving a JSON)
@app.route('/api/suicides/update', methods=['POST'])
def update_suicide():
    connection = connectToDB()

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
    sex = data['sex']

    cursor = connection.cursor()
    cursor.execute(f"UPDATE suicides SET min_age={min_age}, max_age={max_age}, tax={tax}, population_no={population_no}, suicides_no={suicides_no}, "
                   f"generation=\'{generation}\', gdp_for_year=\'{gpd_for_year}\', hdi_for_year={hdi_for_year}, gdp_per_capita={gdp_per_capita}, id_country=\'{id_country}\',  "
                   f"year={year} , sex=\'{sex}\' WHERE id=\'{id}\'")

    cursor.execute(f"SELECT s.*,c.* from suicides s, countries c WHERE id=\'{id}\'")
    result = cursor.fetchone()
    connection.commit()
    c = Country(
        id=result[15],
        name=result[16],
        geom=result[17],
        created_on=result[18],
        updated_on=result[19]
    ).__dict__
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
        updated_on=result[13],
        sex = result[14],
        country = c
    )

    return jsonify([suicide.__dict__]),201


'''
COUNTRIES
'''


# post That returns the countries that we have in the database order by name in alphabetic order
@app.route('/api/countries', methods=['GET'])
def get_countries():
    countries = []

    connection = connectToDB()
    cursor = connection.cursor()
    cursor.execute("SELECT * from countries order by name")
    for result in cursor:
        countries.append(Country(
            id=result[0],
            name=result[1],
            geom=result[2],
            created_on=result[3],
            updated_on=result[4]
        ))
    return jsonify([country.__dict__ for country in countries])


# GET that returns the country number for pagination
@app.route('/api/countries/number', methods=['GET'])
def get_number_countries():

    connection = connectToDB()
    cursor = connection.cursor()

    cursor.execute(f"SELECT COUNT(*) from countries")
    result = cursor.fetchone()

    return [{
        "no_registries": result[0]
    }]

#GET that returns the country and the number of suicides in each country
@app.route('/api/countries/with_suicides_no/<int:page>/<int:max_records>', methods=['GET'])
def get_countries_with_suicides_no(page:int,max_records:int):
    countries = []

    offset = max_records * (page - 1)
    connection = connectToDB()
    cursor = connection.cursor()
    cursor.execute(f"with cs as ( "
                   f"SELECT c.*, SUM(SC.suicides_no) "
                   f"from countries c, suicides sc "
                   f"where c.id = sc.id_country "
                   f"GROUP BY c.id "
                   f") "
                   f"select * from cs ORDER BY name "
                   f"LIMIT {max_records} OFFSET {offset}  ")
    for result in cursor:
        countries.append(Country(
            id=result[0],
            name=result[1],
            geom=result[2],
            created_on=result[3],
            updated_on=result[4],
            suicides_no=result[5]
        ))
    return jsonify([country.__dict__ for country in countries])

#GET that returns the countries without coordinates where have a limit defined by the task that updates them
@app.route('/api/countries/to_update/<int:limit>', methods=['GET'])
def get_countries_to_update(limit:int):
    countries = []

    connection = connectToDB()

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


#GET that returns a country by id
@app.route('/api/countries/<string:id>', methods=['GET'])
def get_country(id:str):
    connection = connectToDB()

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



# POST that create countries
@app.route('/api/countries/create',methods=['POST'])
def create_country():
    connection = connectToDB()

    data = request.get_json()
    name = data['name']

    cursor = connection.cursor()
    cursor.execute(f"insert into countries (name) values (\'{name}\') RETURNING id")
    new_id = cursor.fetchone()[0]
    connection.commit()
    if new_id is not None:
        return get_country(new_id)
    else:
        abort(500)


# POST that update countries
@app.route('/api/countries/update',methods=['POST'])
def update_country():
    connection = connectToDB()

    data = request.get_json()

    id = data['id']
    name = data['name']
    lat = data['lat']
    lon = data['lon']

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



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
