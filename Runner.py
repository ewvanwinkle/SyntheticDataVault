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


# connects to the database
dbname = 'dvdrental'
user = 'postgres'
host = 'localhost'
password = '@uckland1994'
cur, tableNames = PullDataPostgreSQL.ConnectToDatabase(dbname, user, host, password)

# creates a schema to be followed later
schema = CreateSchema(cur, tableNames)

# This section needs to be iteraated over every table in the database
for table in tableNames:

    # gets the data
    data, colnames = PullDataPostgreSQL.ReadAndWriteTables(cur, table, save = 0)

    # deals with missing values in the data













