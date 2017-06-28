from scipy import stats
import numpy as np

def FindDistribution(df, *args):

    bestDistribution = [0] * len(df.columns)
    # allows the user to only text one singular distribution. for efficiency purposes
    try:
        distributionTypes = args[0]
    except:
        distributionTypes = ['truncnorm', 'beta', 'expon', 'uniform']


    bestDistribution = [0] * len(df.columns)
    param = [0] * len(df.columns)
    pvalue = [0] * len(df.columns)

    for x in range(len(df.columns)):

        # preallocation
        dataColumn = df[df.columns[x]]
        l = len(distributionTypes)
        param[x] = [0] * l
        pvalue[x] = [0] * l

        # try all distributions in distribution types
        for y in range(l):

            param[x][y] = eval('stats.%s.fit(dataColumn)' % distributionTypes[y])
            pvalue[x][y] = stats.kstest(dataColumn, distributionTypes[y], param[y])[1]

        bestDistribution[x] = distributionTypes[pvalue.index(max(pvalue))]
        param[x] = param[pvalue.index(max(pvalue))]


    return bestDistribution, param, pvalue

