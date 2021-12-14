import statistics as stats

def get_stats(l):
    mean = stats.mean(l)
    min = min(l)
    max = max(l)
    std = stats.stdev(l)
    coefficient_of_variation = mean / std