import statistics as stats
import math
"""
File to control the computation and aggregation of statistics for arrays of values.
"""


def get_stats(l):
    """
    Gets the four basic stats used for most features
    :param l: List to generate statistics from.
    :return: mean, co-efficient of variation, minimum and maximum.
    """
    mean = stats.mean(l)
    min_val = min(l)
    max_val = max(l)
    std = stats.stdev(l)
    coefficient_of_variation = calc_coefficient_of_variation(mean, std)

    return mean, coefficient_of_variation, min_val, max_val


def get_stdev(l):
    return stats.stdev(l)


def calc_coefficient_of_variation(mean, std):
    """
    The coefficient of variation is a statistical measure of the relative dispersion of data points in a data series
    around the mean. https://en.wikipedia.org/wiki/Coefficient_of_variation
    :param mean:
    :param std:
    :return: Coefficient of variation
    """
    if std == 0:
        return 0
    else:
        return std / mean


def entropy_float_array(l, num, vals, maxval):
    # afaik num could be len(l)...
    """
    Find theoretical basis for entropy, reference here
    For now, this will be based on the implementation from SATzilla

    (posneg-ratio-clause-entropy)
    What is int num -> number of clauses/variables -> length of input array
    What is int vals?

    100, 1

    array_entropy(horny_var+1,numActiveVars,numActiveClauses+1)


    writeFeature("POSNEG-RATIO-CLAUSE-entropy",array_entropy(pos_frac_in_clause,numClauses,100,1));
    https://en.wikipedia.org/wiki/Entropy_(information_theory)
    """

    p = [0] * vals

    res = 0
    entropy = 0

    # make the distribution
    for t in range(num):
        # if l[t] == reserved_value ?:
        #   res ++
        #     continue

        index = math.floor(l[t] / (maxval/vals))

        if index > vals:
            index = vals
        if index < 0:
            index = 0

        p[index] += 1

    for t in range(vals):
        if p[t] != 0:
            pval = p[t]/(num-res)
            entropy += pval * math.log(pval)

    return -1 * entropy


def entropy_int_array(l, num, vals):
    """

    :return:

    vcg clause entropy = array_entropy(clause_array,numClauses,numActiveVars+1))
    """

    p = [0] * vals
    res = 0
    entropy = 0

    for t in range(num):
        p[l[t]] += 1

    for t in range(vals):
        if p[t] != 0:
            pval = p[t]/(num - res)
            entropy += pval * math.log(pval)

    return -1 * entropy

