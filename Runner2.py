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
from CreateSchema import CreateSchema
import pandas as pd
import numpy as np
import ConditionalParameterAggregation as CPA
import FindCovariance
import FindDistribution



# connects to the database
dbname = 'dvdrental'
user = 'postgres'
host = 'localhost'
password = ''
cur, tableNames = PullDataPostgreSQL.ConnectToDatabase(dbname, user, host, password)



# creates a schema to be followed later
schema = CreateSchema(cur, tableNames)

covarianceMatrices = [0]*len(schema)
distributions = [0]*len(schema)
# This section needs to be iterated over every table in the database
for table in tableNames:

    # gets the data
    cur, _ = PullDataPostgreSQL.ConnectToDatabase(dbname, user, host, password)
    data, colnames = PullDataPostgreSQL.ReadTables(cur, table, save = 0)
    df = pd.DataFrame(data, columns = colnames)
    df.fillna(value=np.nan, inplace=True)

    # because fuck that particular column
    if table == 'staff':
        df = df.drop('picture',1)

    # now for the meat of the algorithm: Conditional Parameter Aggregation
    # go inside the file for more details
    df = CPA.ConditionalParameterAggregaation(df, schema[table], dbname, user, host, password)

    # deals with missing values in the data. Will fill any missing values with a
    # random point from the same column. Also creates a new column to identify each
    # value as a either missing or not since this can be relevant data itself
    df = CleanData.MissingValues(df)

    # deals with datetime values in the data. uses the datetime module to convert all
    # datetime values to EPOCH
    df = pd.concat([ df[df.columns[0]], df.loc[:, ~df.columns.str.contains('_id')] ], axis=1)
    df = CleanData.DatetimeToEPOCH(df)

    # saves the extended table to a .csv file. This line can be thought of as a major
    # checkpoint in the code. now all of the data is formatted correctly and saved locally.
    # From here out, the code should focus entirely on modeling and synthesizing. I should
    # no longer have ot worry about data cleaning or manipulation
    df.to_csv('~/PycharmProjects/practice/extended_%s.csv' % table)



    distributiontemp = FindDistribution.FindDistribution(df)


    dftemp= FindCovariance.GaussianCopula(df)









