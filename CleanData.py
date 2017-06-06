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
                df[column + '_EPOCH'] = [0]*len(df)
            except:
                pass

            for y in range(len(df[column])):
                df.loc[y, column + '_EPOCH'] = (df.loc[y, column] - datetime.datetime(1970, 1, 1)).total_seconds()
                y = y+1

            df = df.drop(column,1)

    return df



def IdentifyCategorical(df):
    # I talked with other Eric and Melissa. We determined stopgap measures for
    # determining categorical variables.
    #
    # 1) If it's anything but a number, it's categorical
    # 2) more than 50% of the variables are not unique
    # 3) the numbers are all integers
    # 4) any given number had more than 10% of the instances

    logicalCategorical = [0] * len(df.columns)
    x = 0

    for column in df:

        # checks for strings
        if isinstance(df[column][0], str):
            logicalCategorical[x] = 1
            x = x+1
            continue

        # applies mathematical constraints
        if len(df[column].unique()) < len(df[column])/2:
            logicalCategorical[x] = 1
        elif all(df[column] % 1 == 0):
            logicalCategorical[x] = 1
        elif Counter(df[column]).most_common()[0][1] > len(df[column])/10:
            logicalCategorical[x] = 1

        x = x+1

    return logicalCategorical


def CategoricalToContinuous(df, logicalCategorical):
    # The SDV paper had a very specific method for dealing with categorical variables.
    # Since it cannot be modeled with CPA as is, it needs to be converted into
    # continuous data in order to effectively run. This is done through a 4 step
    # process as outlined in SDV:
    #
    # 1) Identify all categories and sort them from most frequently occurring to least
    # frequently occurring
    # 2) Split the interval [0, 1] into sections based on the cumulative probability
    # for each category.
    # 3) find the interval [a, b] ∈ [0, 1] that corresponds to the category.
    # 4) Chose value between a and b by sampling from a truncated Gaussian distribution
    # with μ at the center of the interval, and σ = (b−a)/6.
    #
    # a graphical description can be viewed in Figure 6 of the SDV paper

    # random values for easy debugging
    df = [random.sample([1,2,3,4,5], 1) for _ in range(500)]
    df = pd.DataFrame([item[0] for item in df])


    x = 0
    for column in df:

        if logicalCategorical[x]:

            count = df[column].value_counts()
            count = count.to_frame()

            # finds the intervals for each individual categorical variable on an
            # interval between 0 and 1
            startpoint = [0]*len(count)
            endpoint = [0]*len(count)
            y = 0
            for index, row in count.iterrows():
                endpoint[y] = startpoint[y] + row[0]/len(df)

                # allows for the initial startpoint to be 0.
                # basically lets me ignore indexing
                try:
                    startpoint[y + 1] = startpoint[y] + row[0]/len(df)
                except:
                    pass
                y = y+1

            # for all pairs of start and end points, create normal data with
            # a mean in the middle of the points and a std of the maximum possible
            # range divided by 6. should also be the size of the number of counts
            data = [0]*len(count)
            for y in range(len(count)):
                start = float(startpoint[y])
                end = float(endpoint[y])
                mean = (start + end) / 2
                scale = (end - start) / 6
                size = round(scale*len(df)*6)
                data[y] = stats.norm.rvs(loc=mean, scale=scale, size=size)
                plt.hist(data[y], 50, normed=1, facecolor='green', alpha=0.5)

            data = np.concatenate(data)

    return df

