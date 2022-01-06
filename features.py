import os
from feature_computation import parse_cnf, balance_features, graph_features, array_stats, active_features

'''
Main file to control extraction of features

'''

def satelite_preprocess(cnf_path="cnf_examples/basic.cnf"):
    # pre process using SatELite binary files
    preprocessed_path = cnf_path[0:-4] + "_preprocessed.cnf"
    satelite_command = "./SatELite/SatELite_v1.0_linux " + cnf_path + " " + preprocessed_path
    os.system(satelite_command)


def compute_features_from_file(cnf_path="cnf_examples/basic.cnf"):
    # parse cnf, and get problem size features

    features_dict = {}

    clauses, c, v = parse_cnf.parse_cnf(cnf_path)

    num_active_vars, num_active_clauses, clause_states, clauses = active_features.get_active_features(clauses, c, v)

    # 1-3.
    # print("c: ", c)
    # print("v: ", v)
    # print("ratio: ", c/v)
    features_dict["c"] = c
    features_dict["v"] = v
    features_dict["clauses_vars_ratio"] = c/v
    features_dict["vars_clauses_ratio"] = v/c

    # print("Active clauses: ", num_active_clauses)
    # print("Active variables: ", num_active_vars)
    # print("Active ration v/c: ", num_active_vars/num_active_clauses)

    # Variable Clause Graph features
    # 4-8
    vcg_v_node_degrees, vcg_c_node_degrees = graph_features.create_vcg(clauses, c, v)

    vcg_v_mean, vcg_v_coeff, vcg_v_min, vcg_v_max = array_stats.get_stats(vcg_v_node_degrees)

    # print("Variable-Clause Graph features")
    # print("Variable nodes degree statistics")
    # print("mean: ", vcg_v_mean)
    # print("coefficient of variation: ", vcg_v_coeff)
    # print("min: ", vcg_v_min)
    # print("max: ", vcg_v_max)

    vg_node_degrees = graph_features.create_vg(clauses)

    pos_neg_clause_ratios, pos_neg_clause_balance, pos_neg_variable_ratios = balance_features.compute_balance_features(clauses, c, v)

    pnc_ratios_mean, pnc_ratios_coeff, pnc_ratios_min, pnc_ratios_max = array_stats.get_stats(pos_neg_clause_balance)

    features_dict["pnc_ratio_mean"] = pnc_ratios_mean
    features_dict["pnc_ratio_coeff"] = pnc_ratios_coeff
    features_dict["pnc_ratio_min"] = pnc_ratios_min
    features_dict["pnc_ratio_max"] = pnc_ratios_max

    pnv_ratios_mean, pnv_ratios_coeff, pnv_ratios_min, pnv_ratios_max = array_stats.get_stats(pos_neg_variable_ratios)

    features_dict["pnv_ratio_mean"] = pnv_ratios_mean
    features_dict["pnv_ratio_coeff"] = pnv_ratios_coeff
    features_dict["pnv_ratio_min"] = pnv_ratios_min
    features_dict["pnv_ratio_max"] = pnv_ratios_max

    return features_dict


if __name__ == "__main__":
    cnf_path = "cnf_examples/basic.cnf"
    preprocessed_path = cnf_path[0:-4] + "_preprocessed.cnf"
    satelite_preprocess(cnf_path)
    features_dict = compute_features_from_file(preprocessed_path)

    test_labels = ["nvarsOrig","nclausesOrig","nvars","nclauses","reducedVars","reducedClauses","Pre-featuretime","vars-clauses-ratio","POSNEG-RATIO-CLAUSE-mean",
                   "POSNEG-RATIO-CLAUSE-coeff-variation","POSNEG-RATIO-CLAUSE-min","POSNEG-RATIO-CLAUSE-max","POSNEG-RATIO-CLAUSE-entropy","VCG-CLAUSE-mean",
                   "VCG-CLAUSE-coeff-variation","VCG-CLAUSE-min","VCG-CLAUSE-max","VCG-CLAUSE-entropy","UNARY","BINARY+","TRINARY+","Basic-featuretime","VCG-VAR-mean","VCG-VAR-coeff-variation",
                   "VCG-VAR-min","VCG-VAR-max","VCG-VAR-entropy","POSNEG-RATIO-VAR-mean","POSNEG-RATIO-VAR-stdev","POSNEG-RATIO-VAR-min","POSNEG-RATIO-VAR-max","POSNEG-RATIO-VAR-entropy",
                   "HORNY-VAR-mean","HORNY-VAR-coeff-variation","HORNY-VAR-min","HORNY-VAR-max","HORNY-VAR-entropy","horn-clauses-fraction","VG-mean","VG-coeff-variation","VG-min","VG-max",
                   "KLB-featuretime","CG-mean","CG-coeff-variation","CG-min","CG-max","CG-entropy","cluster-coeff-mean","cluster-coeff-coeff-variation","cluster-coeff-min","cluster-coeff-max","cluster-coeff-entropy","CG-featuretime"]
    test_vals = [20.000000000,45.000000000,15.000000000,40.000000000,0.333333333,0.125000000,0.000000000,0.375000000,1.000000000,0.000000000,1.000000000,1.000000000,-0.000000000,0.200000000,0.577350269,0.133333333,0.400000000,0.562335145,0.000000000,0.750000000,0.750000000,0.000000000,0.200000000,0.000000000,0.200000000,0.200000000,-0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,-0.000000000,0.100000000,0.000000000,0.100000000,0.100000000,-0.000000000,0.750000000,0.350000000,0.000000000,0.350000000,0.350000000,0.000000000,0.262500000,0.577350269,0.175000000,0.525000000,0.562335145,0.210227273,0.327685288,0.090909091,0.250000000,0.562335145,0.000000000]

    satzilla_features = dict(zip(test_labels, test_vals))


    print("WE ARE CHECKING")
    print("v, c")
    print(features_dict["v"], features_dict["c"])
    print(satzilla_features["nvars"], satzilla_features["nclauses"])
    print("vars clauses ratio")
    print(features_dict["vars_clauses_ratio"])
    print(satzilla_features["vars-clauses-ratio"])


    print("pos neg clauses features")
    print(features_dict["pnc_ratio_mean"], features_dict["pnc_ratio_coeff"], features_dict["pnc_ratio_min"], features_dict["pnc_ratio_max"])
    print(satzilla_features["POSNEG-RATIO-CLAUSE-mean"], satzilla_features["POSNEG-RATIO-CLAUSE-coeff-variation"], satzilla_features["POSNEG-RATIO-CLAUSE-min"],satzilla_features["POSNEG-RATIO-CLAUSE-max"])

    print("pos neg variable features")
    print(features_dict["pnv_ratio_mean"], features_dict["pnv_ratio_coeff"], features_dict["pnv_ratio_min"], features_dict["pnv_ratio_max"])
    print(satzilla_features["POSNEG-RATIO-VAR-mean"], satzilla_features["POSNEG-RATIO-VAR-coeff-variation"], satzilla_features["POSNEG-RATIO-VAR-min"],satzilla_features["POSNEG-RATIO-VAR-max"])



