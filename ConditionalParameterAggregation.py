from scipy import stats
import random
import numpy as np
import pandas as pd
from FindDistribution import FindDistribution
import CleanData

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

def MakeFakeData():
    # I'm making fake data to debug this with
    primaryKey = np.linspace(1,100, num=100)
    data1 = stats.norm.rvs(loc=10, scale=1, size=100)
    data2 = stats.norm.rvs(loc=20, scale=1, size=100)
    data3 = stats.norm.rvs(loc=5, scale=2, size=100)
    data4 = stats.norm.rvs(loc=100, scale=10, size=100)
    df = np.concatenate([primaryKey, data1, data2, data3, data4])
    df = df.reshape([5, 100])
    df = pd.DataFrame(df.T)
    df.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

    foreignKey = [random.sample(primaryKey.tolist(), 1) for _ in range(500)]
    foreignKey = np.array([item[0] for item in foreignKey])
    data1 = stats.norm.rvs(loc=60, scale=1.5, size=500)
    data2 = stats.norm.rvs(loc=30, scale=3, size=500)
    data3 = stats.norm.rvs(loc=5, scale=4, size=500)
    data4 = stats.norm.rvs(loc=100, scale=1, size=500)
    child1 = np.concatenate([foreignKey, data1, data2, data3, data4])
    child1 = child1.reshape([5, 500])
    child1 = pd.DataFrame(child1.T)
    child1.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

    foreignKey = [random.sample(primaryKey.tolist(), 1) for _ in range(500)]
    foreignKey = np.array([item[0] for item in foreignKey])
    data1 = stats.norm.rvs(loc=6, scale=5, size=500)
    data2 = stats.norm.rvs(loc=35, scale=3.5, size=500)
    data3 = stats.norm.rvs(loc=2, scale=.5, size=500)
    data4 = stats.norm.rvs(loc=10, scale=2, size=500)
    child2 = np.concatenate([foreignKey, data1, data2, data3, data4])
    child2 = child2.reshape([5, 500])
    child2 = pd.DataFrame(child2.T)
    child2.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

    return df, child1, child2



def ConditionalParameterAggregaation(df, children, cur):

    # df is the information from the original table. This includes missing value indices
    # and has all datetime values converted to EPOCH
    #
    # children is a list of all child tables
    #
    # cur is a database cursor object that will be used to pull data in the future

    # makes fake data so I dont have to clean just yet
    df, child1, child2 = MakeFakeData()
    children = ['child1', 'child2']


    # now that we have a parent table and two child tables all containing continuous data,
    # I can work on the CPA algorithm

    extendedTable = []
    y = 0
    for child in children:

        child = eval(child)
        # saves all data as categorical or not
        logicalCategorical = CleanData.IdentifyCategorical(child)

        # iterate over all IDs in the primary key
        for ID in df[df.columns[0]]:

            # pulls all data in the child table corresponding to the specific ID
            data = pd.DataFrame(child[child[df.columns[0]] == ID])

            x = 0
            for column in data.columns[1:]:

                # if the column is continuous
                if logicalCategorical[x+1] == 0:

                    # fit the data to a beta distribution and append it to the extended table
                    _, param, _ = FindDistribution(data[column], ['beta'])
                    extendedTable.extend(param)

                # if the column is categorical
                else:
                    pass

                x = x+1
            y = y+1

    return extendedTable

ConditionalParameterAggregaation(1,1,1)