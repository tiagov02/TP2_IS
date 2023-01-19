import sys
import xmlrpc.client
from flask import Flask,abort
from flask_cors import CORS

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True



@app.route('/api/suicides_per_year/<int:year>', methods=['GET'])
def get_suicides_per_year(year:int):
    server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
    res = server.orderByYear(year)
    if not len(res) == 0:
        return [{
            "per_sex": [{
                "sex": res[0][0][0],
                "suicides_no": res[0][0][1]
            },
                {
                    "sex": res[0][1][0],
                    "suicides_no": res[0][1][1]
                }],
            "children": res[1][0][0],
            "olders": res[2][0][0]

        }], 200
    else:
        abort(404)

@app.route('/api/suicides_per_country/<string:country>', methods=['GET'])
def get_suicides_per_country(country):
    try:
        server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
        res = server.orderByCountry(country)
        if not len(res) == 0:
            return [{
                "per_sex": [{
                    "sex": res[0][0][0],
                    "suicides_no": res[0][0][1]
                },
                    {
                        "sex": res[0][1][0],
                        "suicides_no": res[0][1][1]
                    }],
                "children": res[1][0][0],
                "olders": res[2][0][0]
            }], 200
        else:
            abort(404)
    except xmlrpc.client.Fault:
        abort(404)


@app.route('/api/suicides_per_year_country/<int:year>/<string:country>', methods =['GET'])
def get_suicides_per_year_country(year,country):
    try:
        server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
        res = server.orderByYarAndCountry(year, country)
        if not len(res) == 0:
            return [{
                "per_sex": [{
                    "sex": res[0][0][0],
                    "suicides_no": res[0][0][1]
                },
                    {
                        "sex": res[0][1][0],
                        "suicides_no": res[0][1][1]
                    }],
                "children": res[1][0][0],
                "olders": res[2][0][0]
            }], 200
        else:
            abort(404)
    except xmlrpc.client.Fault:
        abort(404)

@app.route('/api/suicides_in_rich_countries', methods=['GET'])
def get_suicides_in_rich_countries():
    try:
        server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
        res = server.suicidesInRichCountry()
        if not len(res) == 0:
            return [{
                "sex": res[0][0],
                "suicides_no": res[0][1]
            },
                       {
                           "sex": res[0][0],
                           "suicides_no": res[0][1]
                       }], 200
        else:
            abort(404)
    except xmlrpc.client.Fault:
        abort(404)

@app.route('/api/country_less_more_suicides', methods=['GET'])
def get_countries_less_more_suicides():
    try:
        server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
        res = server.CountryWithLessandMoreSuicides()
        if not len(res) == 0:
            return [{
                "less": {
                    "country": res[1][0],
                    "suicides_no": res[1][1]
                },
                "more": {
                    "country": res[0][0],
                    "suicides_no": res[0][1]
                }
            }], 200
        else:
            abort(404)
    except xmlrpc.client.Fault:
        abort(404)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
