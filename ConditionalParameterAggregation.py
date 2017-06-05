import scipy

# Conditional Parameter Aggregation (CPA) is one of the most important parts
# of the entire SDV paper. It is what allows the user to synthesize an entire
# database instead of a single table. there are a couple steps that will be taken
# in this paper in accordance with the SDV paper. Keep in mind that the end result
# is to create a series of extended tables that include each original table's data
# and metrics from all the associated children tables

# 1) Start the extended table by saving all the data from the original table.
# 2) Iteratively go through each value in the original table's primary key
#   2a) Go iteratively through each child table
#       2ai) Find all primary key value instances in all children tables
#       2aj) Perform Gaussian Copula and find feature covariance
#       2ak) find alpha and beta values for distribution
#       2al) save all covariance and alpha beta values into the extended table


def ConditionalParameterAggregaation(df, children, cur):

    # df is the information from the original table. This includes missing value indices
    # and has all datetime values converted to EPOCH
    #
    # children is a list of all child tables
    #
    # cur is a database cursor object that will be used to pull data in the future



    return dfExtended