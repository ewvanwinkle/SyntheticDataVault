from scipy import stats


def FindDistribution(column):

    distributionTypes = ['truncnorm', 'beta', 'expon', 'uniform']
    param = [0,0,0,0]
    pvalue = [0,0,0,0]

    for x in [0,1,2,3]:

        param[x] = eval('stats.%s.fit(column)' % distributionTypes[x])
        pvalue[x] = stats.kstest(column, distributionTypes[x], param[x])[1]

    bestDistribution = distributionTypes[pvalue.index(max(pvalue))]
    param = param[pvalue.index(max(pvalue))]

    return bestDistribution, param
