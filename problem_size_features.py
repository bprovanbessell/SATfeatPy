import cnfgen
import statistics as stats
with open("cnf_examples/basic.cnf") as f:
    pos_neg_clause_ratios = []
    num_horn_clauses = 0

    clauses_list = []

    c = None
    v = None
    cv_ratio = None

    for line in f:
        if line[0] == 'c':
            continue
        if line[0] == 'p':
            sizes = line.split(" ")
            variables = int(sizes[2])
            clauses = int(sizes[3])
            ratio = clauses / variables

            print("c: ", clauses)
            print("v: ", variables)
            print("ratio: ", ratio)

            c = clauses
            v = variables
            cv_ratio = ratio

        else:
            clauses_list.append([int(x) for x in line.split(" ")[:-1]])

        # parse first the problem size features, and then do all of the clauses

    variables_count = {}

    for clause in clauses_list:
        # print("clause", clause)

        # all following lines should represent a clause, so literals separated by spaces, with a 0 at the end,
        # denoting the end of the line.
        pos = 0
        neg = 0

        for literal in clause:
            if literal < 0:
                neg += 1
                literal = abs(literal)

            else:
                pos += 1


        if neg == 0:
            ratio = 1
        else:
            ratio = pos/neg
        pos_neg_clause_ratios.append(ratio)

        # clause is a horn clause if it has at most 1 positive literal
        if pos <= 1:
            num_horn_clauses += 1



    print("Number of Horn clauses: ", num_horn_clauses)
    print("Positive/negative literals per clause ratios: ", pos_neg_clause_ratios)

    pos_neg_ratios_mean = stats.mean(pos_neg_clause_ratios)
    pos_neg_ratios_std = stats.stdev(pos_neg_clause_ratios)
    pos_neg_ratios_coefficient_of_variation = pos_neg_ratios_mean/pos_neg_ratios_std

    print(pos_neg_ratios_coefficient_of_variation)

    # what is the entropy??

