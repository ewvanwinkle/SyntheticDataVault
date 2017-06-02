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
        IDs[table] = [string for string in colnames[table] if string[-3:]=="_id"]

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

