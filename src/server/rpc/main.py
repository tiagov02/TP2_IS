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



    with SimpleXMLRPCServer(('0.0.0.0', PORT), requestHandler=RequestHandler) as server:
        server.register_introspection_functions()


        def signal_handler(signum, frame):
            print("received signal")
            server.server_close()

            # perform clean up, etc. here...

            print("exiting, gracefully")
            sys.exit(0)


        # TODO:XPATH AND XQUERY
        '''
        def orderByYear(year):
            nSuicides = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')

                cursor = connection.cursor()
                print(year)

                cursor.execute("SELECT MAX (id) from imported_documents")
                id = cursor.fetchone()[0]

                cursor.execute(
                    f"with suicides as\t"
                    f"(select unnest(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY/SUICIDE', xml))\t"
                    f"as suicide from imported_documents WHERE id={id})\t"
                    f"SELECT ((xpath('@sex', suicide))[1]::varchar) as sex,\t"
                    f"(sum((xpath('@suicides_no',suicide))[1]::varchar::numeric)) :: varchar\t"
                    f"FROM suicides GROUP BY (xpath('@sex', suicide))[1]::varchar")
                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()

                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select unnest(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY/SUICIDE[@minAge < 15]', xml)) "
                               f"as suicide from imported_documents WHERE id={id}) "
                               f"SELECT (sum((xpath('@suicides_no',suicide))[1]::varchar::numeric)) :: varchar "
                               f"FROM suicides")
                for c in cursor:
                    children.append(c)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select unnest(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY/SUICIDE[@maxAge =\"MAX\"]', xml)) "
                               f"as suicide "
                               f"from imported_documents WHERE id={id}) "
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
            return [nSuicides, children, olders]


        
        def orderByCountry(country):
            nSuicides = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')

                cursor = connection.cursor()

                cursor.execute("SELECT MAX (id) from imported_documents")
                id = cursor.fetchone()[0]


                cursor.execute(
                    f"with suicides as (select unnest"
                    f"(xpath('//SUICIDES/YEAR/COUNTRY[@name=\"{country}\"]/SUICIDE', xml)) "
                    f"as suicide from imported_documents WHERE id={id}) "
                    f"SELECT ((xpath('@sex', suicide))[1]::varchar) as sex, "
                    f"(sum((xpath('@suicides_no',suicide))[1]::varchar::numeric))::varchar "
                    f"FROM suicides GROUP BY (xpath('@sex', suicide))[1]::varchar")
                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()

                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select "
                               f"unnest"
                               f"(xpath('//SUICIDES/YEAR/COUNTRY[@name=\"{country}\"]/SUICIDE[@minAge < 15]', xml)) "
                               f"as suicide from imported_documents WHERE id={id}) "
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
                               f"from imported_documents WHERE id={id}) "
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
            return [nSuicides, children, olders]


        def orderByYarAndCountry(year, country):
            nSuicides = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')

                cursor = connection.cursor()

                cursor.execute("SELECT MAX (id) from imported_documents")
                id = cursor.fetchone()[0]

                cursor.execute(
                    f"with suicides as (select unnest"
                    f"(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY[@name=\"{country}\"]/SUICIDE', xml)) "
                    f"as suicide from imported_documents WHERE id={id}) "
                    f"SELECT ((xpath('@sex', suicide))[1]::varchar) as sex, "
                    f"(sum((xpath('@suicides_no',suicide))[1]::varchar::numeric)) :: varchar "
                    f"FROM suicides GROUP BY (xpath('@sex', suicide))[1]::varchar")

                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()

                cursor = connection.cursor()
                cursor.execute(f"with suicides as ("
                               f"select "
                               f"unnest"
                               f"(xpath('//SUICIDES/YEAR[@code=\"{year}\"]/COUNTRY[@name=\"{country}\"]/SUICIDE[@minAge < 15]', xml)) "
                               f"as suicide from imported_documents WHERE id={id}) "
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
                               f"from imported_documents WHERE id={id}) "
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
            return [nSuicides, children, olders]


        def suicidesInRichCountry():
            res = []
            try:
                connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')

                cursor = connection.cursor()

                cursor.execute("SELECT MAX (id) from imported_documents")
                id = cursor.fetchone()[0]

                cursor.execute(f"with suicides as "
                               f"(select unnest(xpath('//SUICIDES/YEAR/COUNTRY/SUICIDE[@gdp_per_capita>18577]', xml)) "
                               f"as suicide from imported_documents WHERE id={id}) "
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


        def CountryWithLessandMoreSuicides():
            res = []
            try:
                connection = psycopg2.connect(host='db-xml', database='is', user='is', password='is')

                cursor = connection.cursor()

                cursor.execute("SELECT MAX (id) from imported_documents")
                id = cursor.fetchone()[0]

                cursor.execute(
                    f"with countries as ( "
                    f"select unnest(xpath('//COUNTRY', xml)) as country "
                    f"from imported_documents WHERE id={id}"
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
        '''
        def orderByYear(year):
            nSuicides = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

                cursor = connection.cursor()
                print(year)

                cursor.execute(f"SELECT sex,SUM(suicides_no) from suicides "
                               f"WHERE year={year} "
                               f"group by sex; ")
                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()

                cursor = connection.cursor()
                cursor.execute(f"SELECT SUM(suicides_no) from suicides "
                               f"WHERE year={year} AND min_age < 15;")
                for c in cursor:
                    children.append(c)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"SELECT SUM(suicides_no) from suicides "
                               f"WHERE year={year} AND max_age = 0;")
                for o in cursor:
                    olders.append(o)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return [nSuicides, children, olders]


        def orderByCountry(country):
            nSuicides = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

                cursor = connection.cursor()

                cursor.execute(
                    f"SELECT s.sex , SUM(s.suicides_no) from suicides s, countries c "
                    f"WHERE s.id_country=c.id AND c.name like \'%{country}%\' "
                    f"Group by s.sex ")
                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()

                cursor = connection.cursor()
                cursor.execute(f"SELECT SUM(s.suicides_no) from suicides s, countries c "
                               f"WHERE s.id_country=c.id AND c.name like \'%{country}%\' AND s.min_age<15 ")
                for c in cursor:
                    children.append(c)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"SELECT SUM(s.suicides_no) from suicides s, countries c "
                               f"WHERE s.id_country=c.id AND c.name like \'%{country}%\' AND s.max_age=0 ")
                for o in cursor:
                    olders.append(o)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return [nSuicides, children, olders]

        def orderByYarAndCountry(year, country):
            nSuicides = []
            children = []
            olders = []
            try:
                connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

                cursor = connection.cursor()

                cursor.execute(
                    f"SELECT s.sex , SUM(s.suicides_no) from suicides s, countries c "
                    f"WHERE s.id_country=c.id AND c.name like \'%{country}%\' AND s.year={year}"
                    f"Group by s.sex ")
                for ns in cursor:
                    nSuicides.append(ns)
                cursor.close()

                cursor = connection.cursor()
                cursor.execute(f"SELECT SUM(s.suicides_no) from suicides s, countries c "
                               f"WHERE s.id_country=c.id AND c.name like \'%{country}%\' AND s.min_age<15 AND s.year={year}")
                for c in cursor:
                    children.append(c)
                cursor.close()
                cursor = connection.cursor()
                cursor.execute(f"SELECT SUM(s.suicides_no) from suicides s, countries c "
                               f"WHERE s.id_country=c.id AND c.name like \'%{country}%\' AND s.max_age=0 AND s.year={year}")
                for o in cursor:
                    olders.append(o)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return [nSuicides, children, olders]


        def suicidesInRichCountry():
            res = []
            try:
                connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

                cursor = connection.cursor()


                cursor.execute(f"SELECT sex , SUM(suicides_no) from suicides "
                               f"WHERE gdp_per_capita>18577 "
                               f"Group by sex ")
                for d in cursor:
                    res.append(d)
            except (Exception, psycopg2.Error) as error:
                print("Failed to fetch data", error)
            finally:
                if connection:
                    cursor.close()
                    connection.close()
            return res


        def CountryWithLessandMoreSuicides():
            res = []
            try:
                connection = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

                cursor = connection.cursor()

                cursor.execute("SELECT MAX (id) from imported_documents")
                id = cursor.fetchone()[0]

                cursor.execute(
                    f"WITH country_suicides as ( "
                    f"SELECT c.name as name, SUM(s.suicides_no) as suicides_no from suicides s, countries c "
                    f"WHERE s.id_country=c.id "
                    f"Group by c.name "
                    f") "
                    f",less_more as( "
                    f" SELECT MIN(suicides_no) min, "
                    f"MAX(suicides_no) max "
                    f"    FROM country_suicides"
                    f") "
                    f"SELECT DISTINCT name, suicides_no "
                    f"from country_suicides "
                    f"WHERE suicides_no IN (select min from less_more) OR "
                    f"suicides_no IN (select max from less_more) "
                    f"ORDER BY suicides_no "
                    f"limit 2 OFFSET 1 ")
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
        server.register_function(orderByYear)
        server.register_function(orderByCountry)
        server.register_function(orderByYarAndCountry)
        server.register_function(suicidesInRichCountry)
        server.register_function(CountryWithLessandMoreSuicides)

        # start the server
        print("Starting the RPC Server...")
        server.serve_forever()
