import psycopg2
import sys
import csv
import numpy


def CreateSchema(cur, tableNames):

    colnames = dict()
    IDs = dict()

    # Finds all the variable names in the tables
    for table in tableNames:

        cur.execute('SELECT * FROM %s' % table)
        colnames[table] = [desc[0] for desc in cur.description]

        # takes only the columns being used as IDs
        IDs[table] = [i for i in colnames[table] if i[-3:]=="_id"]

    # takes all of the IDs in each table and identifies child tables
    schema = dict()
    for table in tableNames:

        # makes sure that all IDs are actually table names. Then removes the "_id' tag
        schema[table] = [i for i in IDs[table][1:] if i[:-3] in tableNames]
        schema[table] = [i[:-3] for i in schema[table]]

        # iterates over all options in the specific tables list
        count = 0
        while count < len(schema[table]):

            # finds the children of the 'count'eth table
            children = IDs[schema[table][count]][1:]
            children = [i[:-3] for i in children]

            # keeps duplicates out. Also makes sure that all IDs are tables
            for x in children:
                if x in schema[table]:
                    continue
                else:
                    if x in tableNames:
                        schema[table].extend([x])

            count = count + 1

    return schema

