import sys
import time

import psycopg2
from psycopg2 import OperationalError

POLLING_FREQ = int(sys.argv[1]) if len(sys.argv) >= 2 else 60


def print_psycopg2_exception(ex):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()

    # get the line number when exception occured
    line_num = traceback.tb_lineno

    # print the connect() error
    print("\npsycopg2 ERROR:", ex, "on line number:", line_num)
    print("psycopg2 traceback:", traceback, "-- type:", err_type)

    # psycopg2 extensions.Diagnostics object attribute
    print("\nextensions.Diagnostics:", ex.diag)

    # print the pgcode and pgerror exceptions
    print("pgerror:", ex.pgerror)
    print("pgcode:", ex.pgcode, "\n")


if __name__ == "__main__":

    db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
    db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')

    while True:

        # Connect to both databases
        db_org = None
        db_dst = None

        try:
            db_org = psycopg2.connect(host='db-xml', database='is', user='is', password='is')
            db_dst = psycopg2.connect(host='db-rel', database='is', user='is', password='is')
        except OperationalError as err:
            print_psycopg2_exception(err)

        if db_dst is None or db_org is None:
            continue

        print("Checking updates...")
        # !TODO: 1- Execute a SELECT query to check for any changes on the table
        # !TODO: 2- Execute a SELECT queries with xpath to retrieve the data we want to store in the relational db
        # !TODO: 3- Execute INSERT queries in the destination db
        # !TODO: 4- Make sure we store somehow in the origin database that certain records were already migrated.
        #          Change the db structure if needed.

        db_org_cur = db_org.cursor()
        db_dst_cur = db_dst.cursor()

        db_org_cur.execute("select COUNT(*) from imported_documents WHERE estado='imported';")
        regs = db_org_cur.fetchone()[0]

        if regs >0 :
            print("Have files in imported_documents. Starting the migration!")
            db_org_cur.execute("select id from imported_documents WHERE estado='imported';")
            ids = db_org_cur.fetchall()

            for id in ids:
                db_org_cur.execute(f"WITH data AS (  "
                                   f"SELECT unnest(xpath('/SUICIDES/YEAR/@code', xml))::text AS year "
                                   f"FROM imported_documents WHERE id={id[0]} "
                                   f")"
                                   f"SELECT DISTINCT year FROM data ORDER BY year;")
                for year in db_org_cur.fetchall():
                    db_org_cur.execute(f"WITH data AS ( "
                                       f"SELECT unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY/@name', xml))::text AS country "
                                       f"FROM imported_documents ) "
                                       f"SELECT DISTINCT country FROM data ORDER BY country;")
                    for country in db_org_cur.fetchall():
                        found = False
                        new_id = None

                        db_dst_cur.execute(f"SELECT id from countries WHERE name=\'{country[0]}\'")
                        a = db_dst_cur.fetchall()
                        if len(a) == 0:
                            db_dst_cur.execute(f"insert into countries (name) values (\'{country[0]}\')")
                            db_dst.commit()
                        db_org_cur.execute(f"WITH data AS ( "
                                           f"SELECT "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@sex', xml)))::text AS sex, "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@minAge', xml)))::text AS min_age, "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@maxAge', xml)))::text AS max_age, "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@tax', xml)))::text AS tax, "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@population_no', xml)))::text AS population_no, "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@suicides_no', xml)))::text AS suicides_no, "
                                           f" (unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@generation', xml)))::text AS generation, "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@gdp_for_year', xml)))::text AS gdp_for_year, "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@hdi_for_year', xml)))::text AS hdi_for_year, "
                                           f"(unnest(xpath('/SUICIDES/YEAR[@code={year[0]}]/COUNTRY[@name=\"{country[0]}\"]/SUICIDE/@gdp_per_capita', xml)))::text AS gdp_per_capita "
                                           f"FROM imported_documents WHERE id={id[0]}"
                                           f")"
                                           f"SELECT * FROM data;")
                        for row in db_org_cur.fetchall():
                            db_dst_cur.execute(f"SELECT id from countries WHERE name=\'{country[0]}\'")
                            new_id = db_dst_cur.fetchone()[0]
                            sex = row[0]
                            min_age = row[1]
                            max_age = row[2] if row[2] != "MAX" else 0
                            tax = row[3]
                            population_no = row[4]
                            suicides_no = row[5]
                            generation = row[6]
                            gdp_for_year = row[7]
                            hdi_for_year = 0 if row[8] == 'nan' else row[8]
                            gdp_per_capita = row[9]
                            db_dst_cur.execute(
                                f"insert into suicides (min_age, max_age, tax, population_no, suicides_no, generation, gdp_for_year, hdi_for_year, gdp_per_capita, year, id_country,sex) "
                                f"values ({min_age}, {max_age}, {tax}, {population_no}, {suicides_no}, \'{generation}\', \'{gdp_for_year}\', {hdi_for_year}, {gdp_per_capita}, {year[0]}, \'{new_id}\', {sex});")
                            db_dst.commit()

                print(f"Finished the conversion for file with id: {id[0]}")
                db_org_cur.execute(
                    f"UPDATE imported_documents SET estado='migrated', updated_on=now() WHERE id={id[0]}")
                db_org.commit()
        db_org.close()
        db_dst.close()

        time.sleep(POLLING_FREQ)
