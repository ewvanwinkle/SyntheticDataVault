import psycopg2
import sys
import csv
import numpy
from collections import Counter


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

def OrganizeSchema(schema):

    # The point of this function lies in the way that a database is laid out.
    # Although a child table will always contain the primary key from it's parent,
    # a second level child (child of a child table) will not necessarily contain said ID
    # It is therefore important to make sure that we always start at the leaf tables
    # and work our way upwards to more complicated tables.

    # identifies all leaf tables and moves them to the front of the new schema
    schema1 = {}
    keys = list(schema.keys())
    for t in keys:

        if len(schema[t]) == 0:
            schema1[t] = schema[t]

    # finds all tables that only use the tables already present. appends them to
    # the table
    y = 0
    while len(schema) != len(schema1):

        key = keys[y % len(schema)]
        keysTemp = list(schema1.keys())
        if key in keysTemp:
            y = y + 1
            continue

        c = Counter(schema[key])
        d = Counter(keysTemp)
        c.subtract(d)
        if all(v <= 0 for k, v in c.items()):
            schema1[key] = schema[key]

        y = y + 1

    return schema1

