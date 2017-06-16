import numpy as np
from collections import Counter
import datetime
import pandas as pd
import random
from scipy import stats
import matplotlib.pyplot as plt


def SynthesizeCategorical(df, logicalCategorical):
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


    for x in range(1,len(df)):

        column = df[df.columns[x]]

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
                # basically lets me ignore proper indexing
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

            data = pd.DataFrame(np.concatenate(data))

            # converts the random data back into the original categories
            changedData = [0]*len(data)
            for x in range(len(data)):

                point = data.loc[x]

                logical1 = [i < point for i in startpoint]
                changedData[x] = count.index[max(np.where(logical1)[0])]


            df[column] = pd.DataFrame(changedData).sample(frac=1).reset_index(drop=True)

    return df
