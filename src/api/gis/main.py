import sys

import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

def connectToDB():
    return psycopg2.connect(user="is",password="is",host="db-rel",database="is")

#return coords lat/long north and south
@app.route('/api/tile/<string:swLng>/<string:swlAT>/<string:neLng>/<string:neLat>', methods=['GET'])
def get_countries(swLng,swlAT,neLng,neLat):

    connection = connectToDB()

    cursor = connection.cursor()
    cursor.execute(f"WITH suicide_country as( "
                   f"select SUM(s.suicides_no) as suicides_no, AVG(s.tax) as med_tax, c.name as country , c.geom as geom, c.id as id,  "
                   f"'https://cdn-icons-png.flaticon.com/512/6349/6349523.png' as imgUrl "
                   f" FROM countries c, suicides s "
                   f"WHERE s.id_country = c.id  "
                   f"GROUP BY s.id_country, c.name, c.geom, c.id "
                   f")"
                   f"SELECT jsonb_build_object(  "
                   f"'type', 'feature', "
                   f"'geometry', ST_AsGeoJSON(geom) ::json, "
                   f"'properties', to_jsonb(sc.*) -'geom' "
                   f") AS json  "
                   f"FROM suicide_country sc "
                   f"WHERE st_contains(st_makeenvelope({neLng},{swlAT},{swLng},{neLat}),sc.geom);"
                   )

    res = cursor.fetchall()
    return jsonify([country for country in res])

#This returns all
@app.route('/api/all', methods=['GET'])
def get_all():
    connection = connectToDB()

    cursor = connection.cursor()

    cursor.execute(f"WITH suicide_country as( "
                   f"select SUM(s.suicides_no) as suicides_no, AVG(s.tax) as med_tax, c.name as country , c.geom as geom, c.id as id,  "
                   f" 'https://cdn-icons-png.flaticon.com/512/6349/6349523.png' as imgUrl "
                   f" FROM countries c, suicides s "
                   f"WHERE s.id_country = c.id  "
                   f"GROUP BY s.id_country, c.name, c.geom,c.id "
                   f")"
                   f"SELECT jsonb_build_object(  "
                   f"'type', 'feature', "
                   f"'geometry', ST_AsGeoJSON(geom)::json, "
                   f"'properties', to_jsonb(sc.*) -'geom' "
                   f") AS json  "
                   f"FROM suicide_country sc; ")
    res = cursor.fetchall()
    return jsonify([country for country in res])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
