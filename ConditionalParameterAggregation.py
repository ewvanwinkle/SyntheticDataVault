import scipy
from CategoricalToContinuous import IdentifyCategorical

# Conditional Parameter Aggregation (CPA) is one of the most important parts
# of the entire SDV paper. It is what allows the user to synthesize an entire
# database instead of a single table. there are a couple steps that will be taken
# in this paper in accordance with the SDV paper. Keep in mind that the end result
# is to create a series of extended tables that include each original table's data
# and metrics from all the associated children tables

# 1) Start the extended table by saving all the data from the original table.
# 2) Iteratively go through each value in the original table's primary key
#   2a) Find all primary key value instances in all children tables
#   2b) Go iteratively through each child table
#       2bi) Perform Gaussian Copula and find feature covariance
#       2bj) find alpha and beta values for distribution
#       2bk) save all covariance and alpha beta values into the extended table


def ConditionalParameterAggregaation(extendedTable, children, table, data):

    extendedTable[table] = data
