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

        # makes sure that tables without any children are still present in the schema
        try:
            schema[table]
        except:
            schema[table] = []

        # appends all of the places a child exists. creates a space for the
        # schema if it doesnt exist yet
        children = [i[:-3] for i in IDs[table]]
        for child in children:
            try:
                schema[child]
            except:
                schema[child] = []

            if child != table:
                schema[child].append(table)


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

