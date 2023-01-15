import sys
import xmlrpc.client
from flask import Flask,abort

PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

app = Flask(__name__)
app.config["DEBUG"] = True

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://rpc-server:9000')
print("Connected!")

@app.route('/api/suicides_per_year/<int:year>', methods=['GET'])
def get_suicides_per_year(year:int):
    res = server.orderByYear(year)
    return [{
        "per_sex":[{
            "sex" : res[0][0][0],
            "suicides_no" : res[0][0][1]
        },
        {
            "sex" : res[0][1][0],
            "suicides_no" : res[0][1][1]
        }],
        "children" : res[1][0][0],
        "olders" : res[3][0][0]
    }],200

@app.route('/api/suicides_per_country/<string:country>', methods=['GET'])
def get_suicides_per_country(country):
    res= server.orderByCountry(country)
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
        "olders": res[3][0][0]
    }], 200

@app.route('/api/suicides_per_year_country/<int:year>/<int:country>', methods =['GET'])
def get_suicides_per_year_country(year,country):
    res = server.orderByYarAndCountry(year, country)
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
        "olders": res[3][0][0]
    }], 200

@app.route('/api/suicides_in_rich_countries', methods=['GET'])
def get_suicides_in_rich_countries():
    res = server.suicidesInRichCountry()
    if not len(res) == 0:
        return [{
            "sex": res[0][0],
            "suicides_no": res[0][1]
        },
        {
            "sex": res[0][0],
            "suicides_no": res[0][1]
        }],200
    else:
        abort(500)

@app.route('/api/country_less_more_suicides', methods=['GET'])
def get_countries_less_more_suicides():
    res = server.CountryWithLessandMoreSuicides()
    if not len(res) == 0:
        return [{
            "less":{
                "country": res[1][0],
                "suicides_no" : res[1][1]
            },
            "more":{
                "country" : res[0][0],
                "suicides_no": res[0][1]
            }
        }],200

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=PORT)
