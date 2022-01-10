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


def write_stats(l, name, features_dict):
    l_mean, l_coeff, l_min, l_max = array_stats.get_stats(l)

    features_dict[name + "_mean"] = l_mean
    features_dict[name + "_coeff"] = l_coeff
    features_dict[name + "_min"] = l_min
    features_dict[name + "_max"] = l_max


def write_entropy(l, name, features_dict, c, v):
    entropy = array_stats.entropy_int_array(l, c, v+1)
    features_dict[name + "_entropy"] = entropy


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
    features_dict["clauses_vars_ratio"] = c / v
    features_dict["vars_clauses_ratio"] = v / c

    # print("Active clauses: ", num_active_clauses)
    # print("Active variables: ", num_active_vars)
    # print("Active ration v/c: ", num_active_vars/num_active_clauses)

    # Variable Clause Graph features
    # 4-8
    vcg_v_node_degrees, vcg_c_node_degrees = graph_features.create_vcg(clauses, c, v)

    # variable node degrees divided by number of active clauses
    vcg_v_node_degrees_norm = [x/c for x in vcg_v_node_degrees]

    # clause node degrees divided by number of active variables
    vcg_c_node_degrees_norm = [x / v for x in vcg_c_node_degrees]

    write_stats(vcg_v_node_degrees_norm, "vcg_var", features_dict)
    write_entropy(vcg_v_node_degrees, "vcg_var", features_dict, c, v)

    # entropy needed
    # 9-13
    write_stats(vcg_c_node_degrees_norm, "vcg_clause", features_dict)
    write_entropy(vcg_c_node_degrees, "vcg_clause", features_dict, c, v)

    # entropy here aswell

    # 14-17
    vg_node_degrees = graph_features.create_vg(clauses)

    print("Variable graph degrees", vg_node_degrees)
    # variable node degrees divided by number of active clauses
    vg_node_degrees_norm = [x / c for x in vg_node_degrees]
    print("norm", vg_node_degrees_norm)

    write_stats(vg_node_degrees_norm, "vg", features_dict)

    pos_neg_clause_ratios, pos_neg_clause_balance, pos_neg_variable_ratios, pos_neg_variable_balance,\
        num_binary_clauses, num_ternary_clauses, num_horn_clauses, horn_clause_variable_count = \
        balance_features.compute_balance_features(clauses, c, v)

    write_stats(pos_neg_clause_balance, "pnc_ratio", features_dict)

    write_stats(pos_neg_variable_balance, "pnv_ratio", features_dict)

    features_dict["pnv_ratio_stdev"] = array_stats.get_stdev(pos_neg_variable_balance)

    features_dict["binary_ratio"] = num_binary_clauses / c
    features_dict["ternary_ratio"] = num_ternary_clauses / c
    features_dict["ternary+"] = (num_binary_clauses + num_ternary_clauses) / c

    features_dict["horn_clauses_fraction"] = num_horn_clauses / c

    horn_clause_variable_count_norm = [x/c for x in horn_clause_variable_count]

    hc_var_mean, hc_var_coeff, hc_var_min, hc_var_max = array_stats.get_stats(horn_clause_variable_count_norm)

    features_dict["hc_var_mean"] = hc_var_mean
    features_dict["hc_var_coeff"] = hc_var_coeff
    features_dict["hc_var_min"] = hc_var_min
    features_dict["hc_var_max"] = hc_var_max

    return features_dict


if __name__ == "__main__":
    cnf_path = "cnf_examples/basic.cnf"
    preprocessed_path = cnf_path[0:-4] + "_preprocessed.cnf"
    satelite_preprocess(cnf_path)
    features_dict = compute_features_from_file(preprocessed_path)

    test_labels = ["nvarsOrig", "nclausesOrig", "nvars", "nclauses", "reducedVars", "reducedClauses", "Pre-featuretime",
                   "vars-clauses-ratio", "POSNEG-RATIO-CLAUSE-mean",
                   "POSNEG-RATIO-CLAUSE-coeff-variation", "POSNEG-RATIO-CLAUSE-min", "POSNEG-RATIO-CLAUSE-max",
                   "POSNEG-RATIO-CLAUSE-entropy", "VCG-CLAUSE-mean",
                   "VCG-CLAUSE-coeff-variation", "VCG-CLAUSE-min", "VCG-CLAUSE-max", "VCG-CLAUSE-entropy", "UNARY",
                   "BINARY+", "TRINARY+", "Basic-featuretime", "VCG-VAR-mean", "VCG-VAR-coeff-variation",
                   "VCG-VAR-min", "VCG-VAR-max", "VCG-VAR-entropy", "POSNEG-RATIO-VAR-mean", "POSNEG-RATIO-VAR-stdev",
                   "POSNEG-RATIO-VAR-min", "POSNEG-RATIO-VAR-max", "POSNEG-RATIO-VAR-entropy",
                   "HORNY-VAR-mean", "HORNY-VAR-coeff-variation", "HORNY-VAR-min", "HORNY-VAR-max", "HORNY-VAR-entropy",
                   "horn-clauses-fraction", "VG-mean", "VG-coeff-variation", "VG-min", "VG-max",
                   "KLB-featuretime", "CG-mean", "CG-coeff-variation", "CG-min", "CG-max", "CG-entropy",
                   "cluster-coeff-mean", "cluster-coeff-coeff-variation", "cluster-coeff-min", "cluster-coeff-max",
                   "cluster-coeff-entropy", "CG-featuretime"]
    test_vals = [20.000000000, 45.000000000, 15.000000000, 40.000000000, 0.333333333, 0.125000000, 0.000000000,
                 0.375000000, 1.000000000, 0.000000000, 1.000000000, 1.000000000, -0.000000000, 0.200000000,
                 0.577350269, 0.133333333, 0.400000000, 0.562335145, 0.000000000, 0.750000000, 0.750000000, 0.000000000,
                 0.200000000, 0.000000000, 0.200000000, 0.200000000, -0.000000000, 0.000000000, 0.000000000,
                 0.000000000, 0.000000000, -0.000000000, 0.100000000, 0.000000000, 0.100000000, 0.100000000,
                 -0.000000000, 0.750000000, 0.350000000, 0.000000000, 0.350000000, 0.350000000, 0.000000000,
                 0.262500000, 0.577350269, 0.175000000, 0.525000000, 0.562335145, 0.210227273, 0.327685288, 0.090909091,
                 0.250000000, 0.562335145, 0.000000000]

    satzilla_features = dict(zip(test_labels, test_vals))

    print("WE ARE CHECKING")
    print("v, c")
    print(features_dict["v"], features_dict["c"])
    print(satzilla_features["nvars"], satzilla_features["nclauses"])
    print("vars clauses ratio")
    print(features_dict["vars_clauses_ratio"])
    print(satzilla_features["vars-clauses-ratio"])

    print("vcg clause stats")
    print(features_dict["vcg_clause_mean"], features_dict["vcg_clause_coeff"], features_dict["vcg_clause_min"], features_dict["vcg_clause_max"], features_dict["vcg_clause_entropy"])
    print(satzilla_features["VCG-CLAUSE-mean"], satzilla_features["VCG-CLAUSE-coeff-variation"],
          satzilla_features["VCG-CLAUSE-min"], satzilla_features["VCG-CLAUSE-max"], satzilla_features["VCG-CLAUSE-entropy"])

    print("vcg variable stats")
    print(features_dict["vcg_var_mean"], features_dict["vcg_var_coeff"], features_dict["vcg_var_min"],
          features_dict["vcg_var_max"], features_dict["vcg_var_entropy"])
    print(satzilla_features["VCG-VAR-mean"], satzilla_features["VCG-VAR-coeff-variation"],
          satzilla_features["VCG-VAR-min"], satzilla_features["VCG-VAR-max"], satzilla_features["VCG-VAR-entropy"])

    print("vg stats")
    print(features_dict["vg_mean"], features_dict["vg_coeff"], features_dict["vg_min"],
          features_dict["vg_max"])
    print(satzilla_features["VG-mean"], satzilla_features["VG-coeff-variation"],
          satzilla_features["VG-min"], satzilla_features["VG-max"])

    print("pos neg clauses features")
    print(features_dict["pnc_ratio_mean"], features_dict["pnc_ratio_coeff"], features_dict["pnc_ratio_min"],
          features_dict["pnc_ratio_max"])
    print(satzilla_features["POSNEG-RATIO-CLAUSE-mean"], satzilla_features["POSNEG-RATIO-CLAUSE-coeff-variation"],
          satzilla_features["POSNEG-RATIO-CLAUSE-min"], satzilla_features["POSNEG-RATIO-CLAUSE-max"])

    print("pos neg variable features")
    print(features_dict["pnv_ratio_mean"], features_dict["pnv_ratio_stdev"], features_dict["pnv_ratio_min"],
          features_dict["pnv_ratio_max"])
    print(satzilla_features["POSNEG-RATIO-VAR-mean"], satzilla_features["POSNEG-RATIO-VAR-stdev"],
          satzilla_features["POSNEG-RATIO-VAR-min"], satzilla_features["POSNEG-RATIO-VAR-max"])

    print("binary, ternary, horn_clauses")
    print(features_dict["binary_ratio"], features_dict["ternary+"], features_dict["horn_clauses_fraction"])
    print(satzilla_features["BINARY+"], satzilla_features["TRINARY+"], satzilla_features["horn-clauses-fraction"])

    print("horn clause variables count")
    print(features_dict["hc_var_mean"], features_dict["hc_var_coeff"], features_dict["hc_var_min"], features_dict["hc_var_max"])
    print(satzilla_features["HORNY-VAR-mean"], satzilla_features["HORNY-VAR-coeff-variation"], satzilla_features["HORNY-VAR-min"], satzilla_features["HORNY-VAR-max"])
