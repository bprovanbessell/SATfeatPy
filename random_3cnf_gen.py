import cnfgen
import math
import csv
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


def gen_n_m_pairs(cv_ratio, upper_n=105, step=5):
    # for each number of variables, we need a specific number of clauses,
    pairs = []
    # to get number of clauses there should be, multiply by the cv ratio,
    # naturally some rounding will be necessary, ratio will not be exactly
    for n in range(3, upper_n+1):
        c = math.ceil(n * cv_ratio)
        pairs.append((n, c))

    return pairs


def gen_pair_formulas(pairs):
    # generate the cnf formula
    # then get whether it is satisfiable or not (can  we use cnfgen for that too?)
    labels_file_names = []
    with open("rand_labels.csv", 'w') as csvfile:
        rand_writer = csv.writer(csvfile, delimiter=',')
        rand_writer.writerow(["file_name", "label"])

        for v, c in pairs:
            random_formula = cnfgen.RandomKCNF(k=k, n=v, m=c)
            label = random_formula.is_satisfiable()

            # save the dimacs
            # create file_name
            fn_base = "_rand_3cnf_" + str(v) + "_" + str(c) + ".cnf"
            if label:
                label_str = "sat"
            else:
                label_str = "unsat"
            fn = label_str + fn_base
            with open(fn, 'w') as f:
                f.write(random_formula.dimacs())

            rand_writer.writerow([fn, label_str])


        # save a csv too with the label and filename? will make it easier later

'''
4 clauses, 1 variable

min would be 12 clauses 3 variables for c/v ratio of 4
'''
