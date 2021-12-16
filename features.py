from feature_computation import parse_cnf, balance_features, graph_features, array_stats

'''
Main file to control extraction of features

'''


def compute_features_from_file(cnf_path="cnf_examples/basic.cnf"):
    # parse cnf, and get problem size features

    features_dict = {}

    clauses, c, v = parse_cnf.parse_cnf(cnf_path)
    cv_ratio = c/v
    # 1-3.
    print("c: ", c)
    print("v: ", v)
    print("ratio: ", cv_ratio)
    features_dict["c"] = c
    features_dict["v"] = v
    features_dict["ratio"] = cv_ratio

    # Variable Clause Graph features
    # 4-8
    vcg_v_node_degrees, vcg_c_node_degrees = graph_features.create_vcg(clauses, c, v)

    vcg_v_mean, vcg_v_coeff, vcg_v_min, vcg_v_max = array_stats.get_stats(vcg_v_node_degrees)

    print("Variable-Clause Graph features")
    print("Variable nodes degree statistics")
    print("mean: ", vcg_v_mean)
    print("coefficient of variation: ", vcg_v_coeff)
    print("min: ", vcg_v_min)
    print("max: ", vcg_v_max)

    vg_node_degrees = graph_features.create_vg(clauses)

    balance_features.compute_balance_features(clauses, c, v)

    return features_dict


if __name__ == "__main__":
    cnf_path = "cnf_examples/basic.cnf"
    # compute_features_from_file(cnf_path)

    test_labels = ["nvarsOrig","nclausesOrig","nvars","nclauses","reducedVars","reducedClauses","Pre-featuretime","vars-clauses-ratio","POSNEG-RATIO-CLAUSE-mean",
                   "POSNEG-RATIO-CLAUSE-coeff-variation","POSNEG-RATIO-CLAUSE-min","POSNEG-RATIO-CLAUSE-max","POSNEG-RATIO-CLAUSE-entropy","VCG-CLAUSE-mean",
                   "VCG-CLAUSE-coeff-variation","VCG-CLAUSE-min","VCG-CLAUSE-max","VCG-CLAUSE-entropy","UNARY","BINARY+","TRINARY+","Basic-featuretime","VCG-VAR-mean","VCG-VAR-coeff-variation"]
    # ,VCG-VAR-min,VCG-VAR-max,VCG-VAR-entropy,POSNEG-RATIO-VAR-mean,POSNEG-RATIO-VAR-stdev,POSNEG-RATIO-VAR-min,POSNEG-RATIO-VAR-max,POSNEG-RATIO-VAR-entropy,HORNY-VAR-mean,HORNY-VAR-coeff-variation,HORNY-VAR-min,HORNY-VAR-max,HORNY-VAR-entropy,horn-clauses-fraction,VG-mean,VG-coeff-variation,VG-min,VG-max,KLB-featuretime,CG-mean,CG-coeff-variation,CG-min,CG-max,CG-entropy,cluster-coeff-mean,cluster-coeff-coeff-variation,cluster-coeff-min,cluster-coeff-max,cluster-coeff-entropy,CG-featuretime]
    test_vals = [20.000000000,45.000000000,15.000000000,40.000000000,0.333333333,0.125000000,0.000000000,0.375000000,1.000000000,0.000000000,1.000000000,1.000000000,-0.000000000,0.200000000,0.577350269,0.133333333,0.400000000,0.562335145,0.000000000,0.750000000,0.750000000,0.000000000,0.200000000,0.000000000,0.200000000,0.200000000,-0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,-0.000000000,0.100000000,0.000000000,0.100000000,0.100000000,-0.000000000,0.750000000,0.350000000,0.000000000,0.350000000,0.350000000,0.000000000,0.262500000,0.577350269,0.175000000,0.525000000,0.562335145,0.210227273,0.327685288,0.090909091,0.250000000,0.562335145,0.000000000]

    for i, x in enumerate(test_labels):
        if "VCG-VAR-coeff" in x:

            index = i

    print(test_vals[index])
