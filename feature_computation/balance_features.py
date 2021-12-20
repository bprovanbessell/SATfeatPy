import statistics as stats


def compute_balance_features(clauses, c, v):
    # parse first the problem size features, and then do all of the clauses

    variables_count = [0] * v * 2
    variables_count_ratio = []
    # positive counts at variable -1, negative literal counts at v + literal -1

    pos_neg_clause_ratios = []
    pos_frac_in_clause = []
    num_horn_clauses = 0
    num_binary_clauses = 0
    num_ternary_clauses = 0

    for clause in clauses:
        # print("clause", clause)

        if len(clause) == 2:
            num_binary_clauses += 1
        if len(clause) == 3:
            num_ternary_clauses += 1

        pos = 0
        neg = 0

        for literal in clause:
            if literal < 0:
                neg += 1
                literal = abs(literal)

                variables_count[literal + v - 1] += 1

            else:
                pos += 1
                variables_count[literal - 1] += 1

        if neg == 0:
            ratio = 1
        else:
            ratio = pos/neg
        pos_neg_clause_ratios.append(ratio)

        pos_frac_in_clause.append(2.0 * abs(0.5 - (pos / (pos + neg))))

        for i in range(v):
            pos_instances = variables_count[i]
            neg_instances = variables_count[i + v]
            if neg_instances == 0:
                vi_ratio = 1
            else:
                vi_ratio = pos_instances/neg_instances

            variables_count_ratio.append(vi_ratio)

        # clause is a horn clause if it has at most 1 positive literal
        if pos <= 1:
            num_horn_clauses += 1

    print("Number of Horn clauses: ", num_horn_clauses)
    print("Positive/negative literals per clause ratios: ", pos_neg_clause_ratios)
    print("Positive/negative literals per clause ratios2: ", pos_frac_in_clause)


    pos_neg_ratios_mean = stats.mean(pos_neg_clause_ratios)
    print("pos fraction mean in clause: ", pos_neg_ratios_mean)
    pos_neg_ratios_std = stats.stdev(pos_neg_clause_ratios)
    pos_neg_ratios_coefficient_of_variation = pos_neg_ratios_mean/pos_neg_ratios_std

    pos_neg_ratio_all_mean = stats.mean(variables_count_ratio)
    pos_neg_ratio_all_std = stats.mean(variables_count_ratio)
    pos_neg_ratios_all_coefficient_of_variation = pos_neg_ratio_all_mean/pos_neg_ratio_all_std
    pos_neg_ratio_all_min = min(variables_count_ratio)
    pos_neg_ratio_all_min = max(variables_count_ratio)

    # entropy?

    print(pos_neg_ratios_coefficient_of_variation)

    # what is the entropy??

    print("binary clause fraction: ", num_binary_clauses/c)
    print("ternary clause fraction: ", num_ternary_clauses/c)

