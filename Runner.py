# this file is just to run all the other files.
# It has also served as my personal outline and project management file throughout
# the course of this internship

# 1) Connect to database
#   1a) Identify schema
#   1b) Pull data in a format python can use
# 2) Data Pre-Processing
#   2a) Deal with nulls
#   2b) Identify Categorical
#   2c) Identify ID columns
#   2d) Conditional Parameter Aggregation
# 3) Data Processing
#   3a) Continuous
#       3ai) Find distributions of best fit
#       3aj) Find covariances between features
#   3b) Categorical
#       3bi)
# 4) Synthesize data
#   4a) Waaaay too far in advance


import PullDataPostgreSQL
import CleanData
import CreateSchema
import pandas as pd
import numpy as np
import ConditionalParameterAggregation as CPA
import datetime
import random
from collections import Counter
import FindDistribution
import FindCovariance


# connects to the database
dbname = 'dvdrental'
user = 'postgres'
host = 'localhost'
password = '@uckland1994'
cur, tableNames = PullDataPostgreSQL.ConnectToDatabase(dbname, user, host, password)


# creates a schema to be followed later. This schema needs to be organized starting
# at leaves and going up to higher level parents
schema = CreateSchema.CreateSchema(cur, tableNames)
schema = CreateSchema.OrganizeSchema(schema)


# This section needs to be iterated over every table in the database
for table in list(schema.keys()):

    # gets the data
    cur, tableNames = PullDataPostgreSQL.ConnectToDatabase(dbname, user, host, password)
    data, colnames = PullDataPostgreSQL.ReadTables(cur, table, save = 0)
    df = pd.DataFrame(data, columns = colnames)
    df.fillna(value=np.nan, inplace=True)
    # print(table, len(df))

    # because fuck that particular column
    if table == 'staff':
        df = df.drop('picture',1)

    # deals with datetime values in the data. uses the datetime module to convert all
    # datetime values to EPOCH
    df = CleanData.DatetimeToEPOCH(df)

    # now for the meat of the algorithm: Conditional Parameter Aggregation
    # go inside the file for more details
    df = CPA.ConditionalParameterAggregaation(df, schema[table])

    # deals with missing values in the data. Will fill any missing values with a
    # random point from the dataset. Also creates a new column to identify each
    # value as a either missing or not since this can be relevant data itself
    df = CleanData.MissingValues(df)

    # Deals with categorical features in the data. this is actually somewhat
    # complicated of a process. First to identify them as categorical, several
    # constraints have been set. they can be seen in depth inside the first function.
    # then to convert values ot continuous, the methodology in the SDV is followed
    # closely. it can be viewed clearly in the SDV paper itself
    # logicalCategorical = CleanData.IdentifyCategorical(df)

    # writes new extended data frame to a local text file
    df.to_csv('%s.csv' % table)


# that condludes the portion of our file surrounding making data.
# Now that we have all of the data in cleaned, organized CSVs,
# we can get values fom them
for table in list(schema.keys()):

    # gets extended table
    df = pd.DataFrame.from_csv('%s.csv' % table)

    # finds the best distribution , pvalues and parameters
    bestDistribution, param, pvalue = FindDistribution.FindDistribution(df)
