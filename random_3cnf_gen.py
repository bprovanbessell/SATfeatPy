import cnfgen
import math
import csv
import numpy as np
import random
from pysat.solvers import Glucose4
from pysat.formula import CNF
# CLAUSE to VARIABLE ratio
# Create range of 3 cnf gen, with clause to variable ratio in a range centered around 4.2, so from 2.2 to 6.2 perhaps

# Also need to get whether the formula is satisfiable or not

k = 3

# to generate a single problem

# n is number of variables
# m is number of clauses
# we want to control this such that the c/v ratio is specific...
# so create some sort of grid search function
# random_formula = cnfgen.RandomKCNF(k=k,)

# minimum n has to be 3 for 3 cnf
# then control m to scale with n??


def gen_n_m_pairs(cv_ratio, upper_n=105):
    # for each number of variables, we need a specific number of clauses,
    pairs = []
    # to get number of clauses there should be, multiply by the cv ratio,
    # naturally some rounding will be necessary, ratio will not be exactly
    for n in range(3, upper_n+1):
        c = math.ceil(n * cv_ratio)
        pairs.append((n, c))

    # perhaps better to do a sampling of these afterwards
    return pairs


def gen_pair_formulas(pairs, save_dir="rand_3cnf/"):
    # generate the cnf formula
    # then get whether it is satisfiable or not (can  we use cnfgen for that too?)
    labels_file_names = []
    csv_fn = save_dir + "rand_labels.csv"
    with open(csv_fn, 'w') as csvfile:
        rand_writer = csv.writer(csvfile, delimiter=',')
        rand_writer.writerow(["file_name", "label"])

        for v, c in pairs:
            random_formula = cnfgen.RandomKCNF(k=k, n=v, m=c)

            fn_base = "rand_3cnf_" + str(v) + "_" + str(c) + ".cnf"
            saved_cnf = save_dir + fn_base
            with open(saved_cnf, 'w') as f:
                f.write(random_formula.dimacs())

            formula = CNF(from_file=saved_cnf)

            with Glucose4(bootstrap_with=formula.clauses) as g:
                label = g.solve()
                # print(g.solve())

            # label = random_formula.is_satisfiable(cmd='glucose -pre')

            # save the dimacs
            # create file_name
            # fn_base = "_rand_3cnf_" + str(v) + "_" + str(c) + ".cnf"
            if label:
                label_str = "sat"
            else:
                label_str = "unsat"
            # fn = save_dir + label_str + fn_base
            # with open(fn, 'w') as f:
            #     f.write(random_formula.dimacs())

            #     rename the file here with the label?? Not really necessary

            rand_writer.writerow([saved_cnf, label_str])

        # save a csv too with the label and filename? will make it easier later


# use solver from pysat, so transfer the cnf to a pysat one to solve the instance
'''
4 clauses, 1 variable

min would be 12 clauses 3 variables for c/v ratio of 4
'''


if __name__ == "__main__":
    ratio = 4.2

    cv_list = gen_n_m_pairs(ratio, upper_n=100)

    # print(cv_list)
    print(len(cv_list))
    # sample = np.random.choice(cv_list, 50, replace=False)
    sample = random.sample(cv_list, 2)
    print(sample)

    gen_pair_formulas(sample)

    # what ranges of ratios do we want to generate samples for
    ratios = [2.2, 3.2, 4.2, 5.2, 6.2]

    for ratio in ratios:
        # depending on how many we want
        cv_list = gen_n_m_pairs(ratio, upper_n=100)
        sample = random.sample(cv_list, 30)
        gen_pair_formulas(sample)
