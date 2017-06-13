from scipy import stats
import numpy as np

def FindDistribution(dataColumn, *args):

    # allopws the user to only text one singular distribution. for efficiency purposes
    try:
        distributionTypes = args[0]
    except:
        distributionTypes = ['truncnorm', 'beta', 'expon', 'uniform']

    #
    l = len(distributionTypes)
    param = [0]*l
    pvalue = [0]*l
    for x in range(l):

        param[x] = eval('stats.%s.fit(dataColumn)' % distributionTypes[x])
        pvalue[x] = stats.kstest(dataColumn, distributionTypes[x], param[x])[1]

    bestDistribution = distributionTypes[pvalue.index(max(pvalue))]
    param = param[pvalue.index(max(pvalue))]

    return bestDistribution, param, pvalue

