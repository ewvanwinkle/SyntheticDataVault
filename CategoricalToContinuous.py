import numpy
from collections import Counter

def CategoricalToContinuousRunner(data):
    # data should be a list of arrays. each array in the list should represent
    # a feature

    isCategorical = [0]*length(data)

    # for loop to iterate through every feature.
    x = 0
    for column in data:

        # first we determine if the variable is categorical.
        # This probably needs some improvement
        isCategorical[x] = IdentifyCategorical(column, isCategorical[x])

        # if the variable is categorical, go through the if statement
        if isCategorical[x] == 1:

            column = CategoricalToContinuous(column)


def IdentifyCategorical(column, logical):
    # I tal;ked with other Eric and we determined a stopgap measure for
    # determining categorical variables.
    #
    # 1) If it's anything but a number, it's categorical
    # 2) more than 50% of the variables are not unique
    # 3) the numbers are all integers
    # 4) any given number had more than 10% of the instances

    # checks for strings
    if len([x for x in str(column) if x.isnumeric()]) == 0:
        logical = 1

    # applies mathematical constraints
    if len(numpy.unique(column)) < len(column)/2:
        logical = 1
    elif sum(column % 1) == 0:
        logical = 1
    elif Counter(column).most_common()[0][1] > len(column)/10:
        logical = 1

    return logical




def CategoricalToContinuous():



def DatetimeToContinuous():
    # This variable is different for all different types of datetime configurations.
