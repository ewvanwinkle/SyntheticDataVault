import psycopg2
import sys
import csv
import numpy


# basically a runner function for pulling data
def PullDataPostgreSQL(dbname, user, host, password):

    cur, tableNames = ConnectToDatabase(dbname, user, host, password)
    schema = CreateSchema(cur, tableNames)



def ConnectToDatabase(dbname, user, host, password):

    # allows for parameters to be blank. basically for lazy code creation
    try:
        dbname
    except:
        dbname = 'dvdrental'
    try:
        user
    except:
        user = 'postgres'
    try:
        host
    except:
        host = 'localhost'
    try:
        password
    except:
        password = ''

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



def CreateSchema(cur, tableNames):

    colnames = dict()
    IDs = dict()

    # Finds all the variable names in the tables
    for table in tableNames:

        cur.execute('SELECT * FROM %s' % table)
        colnames[table] = [desc[0] for desc in cur.description]

        # takes only the columns being used as IDs
        IDs[table] = [str for str in colnames[table] if str[-3:]=="_id"]

    # takes all of the IDs in each table and identifies child tables
    schema = {}
    for table in tableNames:

        # makes sure that all IDs are actually table names. Then removes the "_id' tag
        schema[table] = [x for x in IDs[table][1:] if x[:-3] in tableNames]
        schema[table] = [x[:-3] for x in schema[table]]
        count = 0

        # iterates over all options in the specific tables list
        while count < len(schema[table]):

            # finds the children of the 'count'eth table
            children = IDs[schema[table][count]][1:]
            children = [x[:-3] for x in children]

            # keeps duplicates out. Also makes sure that all IDs are tables
            for x in children:
                if x in schema[table]:
                    continue
                else:
                    if x in tableNames:
                        schema[table].extend([x])

            count = count + 1

    return schema







def WriteTablesToTXT(cur, tablenames):

    # saves all the different tables as txt files
    for table in tableNames:

        cur.execute('SELECT * FROM %s' % table)
        data = cur.fetchall()
        colnames = [desc[0] for desc in cur.description]

        with open('%s.txt' % table, "w") as the_file:
            csv.register_dialect("custom", delimiter=" ", skipinitialspace=True)
            writer = csv.writer(the_file, dialect="custom")
            writer.writerow(colnames)
            for tup in data:
                writer.writerow(tup)