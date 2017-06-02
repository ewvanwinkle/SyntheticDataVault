import numpy
from collections import Counter
import datetime
from itertools import compress



# This specific group of functions is focused on cleaning the data so that
# it can be processed in the future. This includes things such as identifying
# and filling missing data, identifying categorical and datetime variables,
# and finally converting both of those into continuous data

def IdentifyMissingValues(data):

    # the point of this function is to deal with missing data points in a data set.
    # It creates a new column in the data identifying what points were missing.

    # Iterates by column


    logicalMissing = []
    return logicalMissing


def IdentifyCategorical(data):
    # I talked with other Eric and Melissa. We determined stopgap measures for
    # determining categorical variables.
    #
    # 1) If it's anything but a number, it's categorical
    # 2) more than 50% of the variables are not unique
    # 3) the numbers are all integers
    # 4) any given number had more than 10% of the instances

    logicalCategorical = []
    x = 0

    for column in data:

        # checks for strings
        if len([x for x in str(column) if x.isnumeric()]) == 0:
            logicalCategorical[x] = 1

        # applies mathematical constraints
        if len(numpy.unique(column)) < len(column)/2:
            logicalCategorical[x] = 1
        elif sum(column % 1) == 0:
            logicalCategorical[x] = 1
        elif Counter(column).most_common()[0][1] > len(column)/10:
            logicalCategorical[x] = 1

    return logicalCategorical


def IdentifyDatetime(data):
    # This function is a pretty basic for loop that determines whether or not a given
    # feature is a datetime

    x = 0
    column = data[0]
    logicalDatetime = [0]*len(column)

    for point in column:
        logicalDatetime[x] = isinstance(point, datetime.datetime)
        x = x+1

    return logicalDatetime





def FillMissingValues(data, logicalMissing):
    # once missing values have been identified, they can be filled with a number
    # from their respective distribution chosen at random

    x = 0
    for column in data:

        logicalMissingColumn = logicalMissing[x]
        data = list(compress(column, logicalMissingColumn))
        y = 0

        for logical in logicalMissingColumn:
            if logical:
                pass


    return data


def CategoricalToContinuous(data, logicalContinuous):
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

    return data

def DatetimeToContinuous(data, logicalDatetime):
    # All features identified as 'datetime features' will be converted to number
    # of seconds past EPOCH.

    return data
