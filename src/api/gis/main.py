import sys

import psycopg2
from flask import Flask, request, jsonify

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/tile', methods=['GET'])
def get_markers():
    args = request.args

    return [
        {
            "type": "feature",
            "geometry": {
                "type": "Point",
                "coordinates": [41.69462, -8.84679]
            },
            "properties": {
                "id": "7674fe6a-6c8d-47b3-9a1f-18637771e23b",
                "name": "Ronaldo",
                "country": "Portugal",
                "position": "Striker",
                "imgUrl": "https://cdn-icons-png.flaticon.com/512/805/805401.png",
                "number": 7
            }
        }
    ]
#This returns all
@app.route('/api/all', methods=['GET'])
def get_all():
    connection = psycopg2.connect(user="is",
                                  password="is",
                                  host="db-rel",
                                  database="is")

    cursor = connection.cursor()
    cursor.execute(f"WITH suicide_country as( "
                   f"select SUM(s.suicides_no) as suicides_no, AVG(s.tax) as med_tax, c.name as country , c.geom as geom "
                   f" FROM countries c, suicides s "
                   f"WHERE s.id_country = c.id AND st_makeenvelope(39.50,76.4,39.3,76.6) "
                   f"GROUP BY s.id_country, c.name, c.geom "
                   f")"
                   f"SELECT jsonb_build_object(  "
                   f"'type', 'feature', "
                   f"'geometry', ST_AsGeoJSON(geom), "
                   f"'proprieties', to_jsonb(sc.*) -'id' -'geom' "
                   f") AS json  "
                   f"FROM suicide_country sc; ")
    res = cursor.fetchall()
    return jsonify([country for country in res])

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
