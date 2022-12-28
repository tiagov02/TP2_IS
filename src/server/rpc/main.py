import signal, sys

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

from functions.string_length import string_length
from functions.string_reverse import string_reverse
from lxml import etree
import psycopg2
PORT = int(sys.argv[1]) if len(sys.argv) >= 2 else 9000

if __name__ == "__main__":
    class RequestHandler(SimpleXMLRPCRequestHandler):
        rpc_paths = ('/RPC2',)


    with SimpleXMLRPCServer(('localhost', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()


        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...

            print("exiting, gracefully")
            sys.exit(0)


        def validateXSD(xml: str, xsd_path: str) -> bool:
            xmlschema_doc = etree.parse(xsd_path)
            xmlschema = etree.XMLSchema(xmlschema_doc)

            xml_doc = etree.fromstring(xml)
            result = xmlschema.validate(xml_doc)

            return result


        def receive_file(arg):
            if validateXSD(arg.data, "suicidesXSD.xsd"):
                with open("suicides.xml", "wb") as handle:
                    saveToDb(arg.data)
                    handle.write(arg.data)
                    return True
            else:
                return False


        def saveToDb(xml: str):
            try:
                xml_file = etree.fromstring(xml)
                s = etree.tostring(xml_file, encoding="utf8", method="xml").decode()
                connection = psycopg2.connect(user="is",
                                              password="is",
                                              host="localhost",
                                              port="5432",
                                              database="is")

                cursor = connection.cursor()
                cursor.execute("INSERT INTO imported_documents (file_name, xml) VALUES(%s, %s)", ("suicides2.xml", s))
                connection.commit()
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()


        # XPATH AND XQUERY
        def orderByYear(year):
            nSuicides = []
            data = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(user="is",
                                              password="is",
                                              host="localhost",
                                              port="5432",
                                              database="is")

                cursor = connection.cursor()
                print(year)

                cursor.execute(
                    f"with suicides as\t"
                    f"(select unnest(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY/SUICIDE', xml))\t"
                    f"as suicide from imported_documents where file_name = 'suicides2.xml')\t"
                    f"SELECT ((xpath('@sex', suicide))[1]::varchar) as sex,\t"
                    f"(sum((xpath('@suicides_no',suicide))[1]::varchar::numeric)) :: varchar\t"
                    f"FROM suicides GROUP BY (xpath('@sex', suicide))[1]::varchar")
                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"select unnest( "
                               f"xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY/SUICIDE',xml) "
                               f" ) as suicide "
                               f"from imported_documents where file_name='suicides2.xml'")
                for dt in cursor:
                    data.append(dt)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select unnest(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY/SUICIDE[@minAge < 15]', xml)) "
                               f"as suicide from imported_documents where file_name = 'suicides2.xml') "
                               f"SELECT (sum((xpath('@suicides_no',suicide))[1]::varchar::numeric)) :: varchar "
                               f"FROM suicides")
                for c in cursor:
                    children.append(c)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select unnest(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY/SUICIDE[@maxAge =\"MAX\"]', xml)) "
                               f"as suicide "
                               f"from imported_documents where file_name = 'suicides2.xml') "
                               f"SELECT (sum((xpath('@suicides_no',suicide))[1]::varchar::numeric))::varchar "
                               f"FROM suicides")
                for o in cursor:
                    olders.append(o)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return [nSuicides, data, children, olders]


        ##alterar
        def orderByCountry(country):
            nSuicides = []
            data = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(user="is",
                                              password="is",
                                              host="localhost",
                                              port="5432",
                                              database="is")

                cursor = connection.cursor()
                cursor.execute(
                    f"with suicides as (select unnest"
                    f"(xpath('//SUICIDES/YEAR/COUNTRY[@name=\"{country}\"]/SUICIDE', xml)) "
                    f"as suicide from imported_documents where file_name = 'suicides2.xml') "
                    f"SELECT ((xpath('@sex', suicide))[1]::varchar) as sex, "
                    f"(sum((xpath('@suicides_no',suicide))[1]::varchar::numeric))::varchar "
                    f"FROM suicides GROUP BY (xpath('@sex', suicide))[1]::varchar")
                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"select unnest( "
                               f"xpath('//SUICIDES/YEAR/COUNTRY[@name=\"{country}\"]/SUICIDE',xml) "
                               f" ) as suicide "
                               f"from imported_documents where file_name='suicides2.xml'")
                for dt in cursor:
                    data.append(dt)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select "
                               f"unnest"
                               f"(xpath('//SUICIDES/YEAR/COUNTRY[@name=\"{country}\"]/SUICIDE[@minAge < 15]', xml)) "
                               f"as suicide from imported_documents where file_name = 'suicides2.xml') "
                               f"SELECT (sum((xpath('@suicides_no',suicide))[1]::varchar::numeric))::varchar "
                               f"FROM suicides")
                for c in cursor:
                    children.append(c)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select "
                               f"unnest"
                               f"(xpath('//SUICIDES/YEAR/COUNTRY[@name=\"{country}\"]/SUICIDE[@maxAge =\"MAX\"]', xml)) "
                               f"as suicide "
                               f"from imported_documents where file_name = 'suicides2.xml') "
                               f"SELECT (sum((xpath('@suicides_no',suicide))[1]::varchar::numeric))::varchar "
                               f"FROM suicides")
                for o in cursor:
                    olders.append(o)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return [nSuicides, data, children, olders]


        def orderByYarAndCountry(year, country):
            nSuicides = []
            data = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(user="is",
                                              password="is",
                                              host="localhost",
                                              port="5432",
                                              database="is")

                cursor = connection.cursor()
                cursor.execute(
                    f"with suicides as (select unnest"
                    f"(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY[@name=\"{country}\"]/SUICIDE', xml)) "
                    f"as suicide from imported_documents where file_name = 'suicides2.xml') "
                    f"SELECT ((xpath('@sex', suicide))[1]::varchar) as sex, "
                    f"(sum((xpath('@suicides_no',suicide))[1]::varchar::numeric)) :: varchar "
                    f"FROM suicides GROUP BY (xpath('@sex', suicide))[1]::varchar")

                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"select unnest( "
                               f"xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY[@name=\"{country}\"]/SUICIDE',xml) "
                               f" ) as suicide "
                               f"from imported_documents where file_name='suicides2.xml'")
                for dt in cursor:
                    data.append(dt)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select "
                               f"unnest"
                               f"(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY[@name=\"{country}\"]/SUICIDE[@minAge < 15]', xml)) "
                               f"as suicide from imported_documents where file_name = 'suicides2.xml') "
                               f"SELECT (sum((xpath('@suicides_no',suicide))[1]::varchar::numeric))::varchar "
                               f"FROM suicides")
                for c in cursor:
                    children.append(c)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select "
                               f"unnest("
                               f"xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY[@name=\"{country}\"]/SUICIDE[@maxAge =\"MAX\"]', xml)) "
                               f"as suicide "
                               f"from imported_documents where file_name = 'suicides2.xml') "
                               f"SELECT (sum((xpath('@suicides_no',suicide))[1]::varchar::numeric))::varchar "
                               f"FROM suicides")
                for o in cursor:
                    olders.append(o)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return [nSuicides, data, children, olders]


        def suicidesInRichCountry():
            res = []
            try:
                connection = psycopg2.connect(user="is",
                                              password="is",
                                              host="localhost",
                                              port="5432",
                                              database="is")

                cursor = connection.cursor()
                cursor.execute(f"with suicides as "
                               f"(select unnest(xpath('//SUICIDES/YEAR/COUNTRY/SUICIDE[@gdp_per_capita>18577]', xml)) "
                               f"as suicide from imported_documents where file_name = 'suicides2.xml') "
                               f"SELECT ((xpath('@sex', suicide))[1]::varchar) as sex, "
                               f"(sum((xpath('@suicides_no',suicide))[1]::varchar::numeric))::varchar "
                               f"FROM suicides GROUP BY (xpath('@sex', suicide))[1]::varchar")
                for d in cursor:
                    res.append(d)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return res


        def yearWithLessandMoreSuicides():
            res = []
            try:
                connection = psycopg2.connect(user="is",
                                              password="is",
                                              host="localhost",
                                              port="5432",
                                              database="is")

                cursor = connection.cursor()
                cursor.execute(
                    f"with countries as ( "
                    f"select unnest(xpath('//COUNTRY', xml)) as country "
                    f"from imported_documents "
                    f"where file_name = 'suicides2.xml' "
                    f"), country_suicides as ( "
                    f"SELECT "
                    f"(xpath('@name', country))[1]::text as country_name, "
                    f"SUM((xpath('sum(./SUICIDE/@suicides_no)', country))[1]::text::decimal) as no_suicides "
                    f"FROM "
                    f"countries "
                    f"GROUP BY "
                    f"(xpath('@name', country))[1]::text "
                    f"),lessandmore_suicides as ( "
                    f"SELECT "
                    f"MIN(no_suicides) min, "
                    f"MAX(no_suicides) max "
                    f"FROM "
                    f"country_suicides"
                    f")"
                    f"SELECT country_name , (no_suicides) ::varchar "
                    f"FROM country_suicides "
                    f"WHERE "
                    f"no_suicides IN (SELECT max FROM lessandmore_suicides) OR "
                    f"no_suicides IN (SELECT min FROM lessandmore_suicides) ")
                for d in cursor:
                    res.append(d)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return res


        # signals

        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGHUP, signal_handler)
        signal.signal(signal.SIGINT, signal_handler)

        # register both functions
        server.register_function(string_reverse)
        server.register_function(string_length)
        server.register_function(receive_file)
        server.register_function(orderByYear)
        server.register_function(orderByCountry)
        server.register_function(orderByYarAndCountry)
        server.register_function(suicidesInRichCountry)
        server.register_function(yearWithLessandMoreSuicides)

        # start the server
        print("Starting the RPC Server...")
        server.serve_forever()
