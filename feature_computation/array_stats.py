import statistics as stats
"""
File to control the computation and aggregation of statistics for arrays of values.
"""


def get_stats(l):
    mean = stats.mean(l)
    min_val = min(l)
    max_val = max(l)
    std = stats.stdev(l)
    coefficient_of_variation = calc_coefficient_of_variation(mean, std)

    return mean, coefficient_of_variation, min_val, max_val

"""
Find theoretical basis for entropy, reference here
For now, this will be based on the implementation from SATzilla
"""
def entropy_array(l):
    pass

"""
The coefficient of variation is a statistical measure of the relative dispersion of data points in a data series around the mean.
"""

def calc_coefficient_of_variation(mean, std):
    if std == 0:
        return 0
    else:
        return mean / std