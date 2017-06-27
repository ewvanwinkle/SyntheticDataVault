import numpy as np
from collections import Counter
import datetime
import pandas as pd
import random
from scipy import stats
import matplotlib.pyplot as plt



# This specific group of functions is focused on cleaning the data so that
# it can be processed in the future. This includes things such as identifying
# and filling missing data, identifying categorical and datetime variables,
# and finally converting both of those into continuous data

def MissingValues(df):

    # the point of this function is to deal with missing data points in a data set.
    # It creates a new column in the data identifying what points were missing.
    # It then fills the missing values with random values from the row

    x = 0
    for column in df:

        # if any values in the column are missing
        if pd.isnull(df[column]).any():

            # identifies missing values
            logicalMissing = pd.isnull(df[column])
            logicalFilled = [not i for i in logicalMissing]

            # and fills them from a random point in the data
            df[column].fillna(random.choice(df[column][logicalFilled] )
                              , inplace=True)

            # then fills in a new row indicating which values were missing
            x = x+1
            df.insert(x, column + '_MissingLogical', logicalMissing)

        x = x+1

    return df



def DatetimeToEPOCH(df):
    # This function is a pretty basic for loop that determines whether or not a given
    # feature is a datetime

    for column in df:

        # if the column contains datetimes
        if isinstance(df[column][0], datetime.datetime):

            # converts all datetimes to EPOCH
            y = 0
            try:
                df[column] = df[column].astype(np.int64) // 10**9
                df.rename(columns={column: column + '_EPOCH'}, inplace=True)
            except:
                pass


    return df



def IdentifyCategorical(df):
    # I talked with other James, Eric and Melissa. We determined stopgap measures for
    # determining categorical variables.
    #
    # 1) If it's anything but a number, it's categorical
    # 2) more than 50% of the variables are not unique
    # 3) the numbers are all integers
    # 4) any given number had more than 10% of the instances

    logicalCategorical = [0] * len(df.columns)

    for x in range(len(df.columns)):

        try:
            column = df.columns[x]

            # checks for strings and datetimes
            if isinstance(df[column][0], str):
                logicalCategorical[x] = 1
            elif column[-6:] == '_EPOCH':
                continue
            else:
                pass

            # applies mathematical constraints
            if len(df[column].unique()) < len(df[column])/2:
                logicalCategorical[x] = 1
            elif all(df[column] % 1 == 0):
                logicalCategorical[x] = 1
            elif Counter(df[column]).most_common()[0][1] > len(df[column])/10:
                logicalCategorical[x] = 1
        except:
            logicalCategorical[x] = 1



    return logicalCategorical


def RemoveUnimportant(df):

    # the point of this function is to return only columns with important data.
    # Things that will be taken out:
    # 1) anything with the string '_id' in it
    # 2) any value with absolutely no variation

    return df

