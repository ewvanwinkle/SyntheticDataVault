import psycopg2
import sys
import csv
import numpy


def ConnectToDatabase(dbname, user, host, password):


    # attempts to connect ot the database
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s'"
                                % (dbname, user, host, password))
        cur = conn.cursor()
    except:
        print("I am unable to connect to the database")

    # reads the table names of the database into python
    try:
        cur.execute("SELECT relname FROM pg_class WHERE relkind='r' and "
                    "relname !~ '^(pg_|sql_)';")
        tableNames = cur.fetchall()
    except psycopg2.Error as e:
        pass

    # gets table names out of list of tuples and into list
    tableNames = [name[0] for name in tableNames]

    return cur, tableNames



def ReadTables(cur, table, save):

    # pull all data, also puulll column names
    cur.execute('SELECT * FROM %s' % table)
    data = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]

    # if desired, save table to an external TXT file
    if save == 1:
        with open('%s.txt' % table, "w") as the_file:
            csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
            writer = csv.writer(the_file, dialect="custom")
            writer.writerow(colnames)
            for tup in data:
                writer.writerow(tup)

    return data, colnames

