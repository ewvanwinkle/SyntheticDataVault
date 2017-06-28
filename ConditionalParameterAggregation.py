from scipy import stats
import random
import numpy as np
import pandas as pd
import CleanData
import timeit
import PullDataPostgreSQL

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


def ConditionalParameterAggregaation(df, children):
    # df is the information from the original table. This includes missing value indices
    # and has all datetime values converted to EPOCH
    #
    # children is a list of all child tables
    #
    # cur is a database cursor object that will be used to pull data in the future


    for childstr in children:
        print(childstr)

        child = pd.DataFrame.from_csv('%s.csv' % childstr)
        child.fillna(value=np.nan, inplace=True)

        # saves all data as categorical or not. ignores the primary key
        logicalCategorical = CleanData.IdentifyCategorical(child)

        # preallocates memory for points to be appended to in the future
        df = MakeBlankDataFrame(df, child, childstr, logicalCategorical)


        # iterate over all IDs in the primary key with the intent of finding and
        # inputting data
        for c in range(len(df[df.columns[0]])):
            print(c)

            ID = df[df.columns[0]][c]

            # pulls all data in the child table corresponding to the specific ID
            data = pd.DataFrame(child[child[df.columns[0]] == ID])

            # iterates over every column in the dataset
            for y in range(1, len(child.columns)):

                column = child.columns[y]

                # if the column is Categorical
                if logicalCategorical[y]:

                    uniqueCategories = sorted(child[child.columns[y]].unique().tolist())
                    # finds the percentage of each variable in the column of the temporary
                    # dataset. then saves that
                    if len(data) == 0:

                        for z in range(len(uniqueCategories)):
                            cat = uniqueCategories[z]
                            colname = 'Categ_%s_%s_%s' % (cat, column, childstr)
                            df.loc[c, colname] = None

                    else:

                        count = CalculateCategoricalPercentage(data, uniqueCategories, column)

                        # adds the points to the correct column
                        for z in range(len(uniqueCategories)):
                            cat = uniqueCategories[z]
                            colname = 'Categ_%s_%s_%s' % (cat, column, childstr)
                            df.loc[c, colname] = count.loc[0,cat]

                # if the column is continuous
                else:

                    points = ['alpha', 'beta', 'loc', 'scale']
                    # fit the data to a beta distribution and append it to the extended table
                    # initial dataframe to make sure that numbers aren't left out
                    if len(data) == 0:
                        for z in range(3):
                            colname = 'Cont_%s_%s_%s' % (points[z], column, childstr)
                            df.loc[c, colname] = None
                    else:
                        statistics = list(stats.beta.fit(data[column]))
                        for z in range(4):
                            colname = 'Cont_%s_%s_%s' % (points[z], column, childstr)
                            df.loc[c, colname] = statistics[z]

    return df


def CalculateCategoricalPercentage(data, uniqueCategories, column):

    # initial dataframe to make sure that numbers aren't left out
    d1 = pd.DataFrame([0] * len(uniqueCategories)).T
    d1.columns = uniqueCategories

    # finds the percentages to be added to the df
    count = data[column].value_counts()
    count = (count + d1) / sum(count)
    count[count.isnull()] = 0
    count = count

    return count


def MakeBlankDataFrame(df, child, childstr, logicalCategorical):

    # The point of this function is to create a blank dataframe to enter points into int he future
    # It uses column names as metadata storage.
    #
    # df is the original dataframe getting appended to.
    # child is the child dataframe being appended
    # childstr is the specific name of the child dataframe
    # logicalCategorical is a logical list indicating whether each column is categorical or continuous


    # ignores the primary key
    for y in range(1, len(child.columns)):

        column = child.columns[y]

        # For categorical variables, we must create a column for each category.
        if logicalCategorical[y]:

            uniqueCategories = child[child.columns[y]].unique().tolist()
            for z in range(len(uniqueCategories)):
                cat = uniqueCategories[z]
                colname = 'Categ_%s_%s_%s' % (cat, column, childstr)
                df = pd.concat([df, pd.DataFrame(np.zeros([len(df)]), columns=[colname])], axis=1)

        # For continuous, we must create 4 columns for beta distribution values
        else:
            points = ['alpha', 'beta', 'loc', 'scale']
            for z in range(4):
                colname = 'Cont_%s_%s_%s' % (points[z], column, childstr)
                df = pd.concat([df, pd.DataFrame(np.zeros([len(df)]), columns=[colname])], axis=1)

    return df



def MakeFakeData(Continuous):
    # I'm making fake data to debug this with. It's a temporary funcution

    if Continuous == 1:
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
    else:

        primaryKey = np.linspace(1,100, num=100)
        data1 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(100)]]
        data2 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(100)]]
        data3 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(100)]]
        data4 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(100)]]
        df = np.concatenate([primaryKey, data1, data2, data3, data4])
        df = df.reshape([5, 100])
        df = pd.DataFrame(df.T)
        df.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

        foreignKey = [random.sample(primaryKey.tolist(), 1) for _ in range(500)]
        foreignKey = np.array([item[0] for item in foreignKey])
        data1 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(500)]]
        data2 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(500)]]
        data3 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(500)]]
        data4 = [i[0] for i in [random.sample([1, 2, 3, 4, 5], 1) for _ in range(500)]]
        child1 = np.concatenate([foreignKey, data1, data2, data3, data4])
        child1 = child1.reshape([5, 500])
        child1 = pd.DataFrame(child1.T)
        child1.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

        foreignKey = [random.sample(primaryKey.tolist(), 1) for _ in range(500)]
        foreignKey = np.array([item[0] for item in foreignKey])
        data1 = [i[0] for i in [random.sample([10, 20, 30, 40, 50], 1) for _ in range(500)]]
        data2 = [i[0] for i in [random.sample([10, 20, 30, 40, 50], 1) for _ in range(500)]]
        data3 = [i[0] for i in [random.sample([10, 20, 30, 40, 50], 1) for _ in range(500)]]
        data4 = [i[0] for i in [random.sample([10, 20, 30, 40, 50], 1) for _ in range(500)]]
        child2 = np.concatenate([foreignKey, data1, data2, data3, data4])
        child2 = child2.reshape([5, 500])
        child2 = pd.DataFrame(child2.T)
        child2.columns = ['df_id', 'data1', 'data2', 'data3', 'data4']

    return df, child1, child2
