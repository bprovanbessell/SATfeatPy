import os
import statistics
import sys
from feature_computation import parse_cnf, balance_features, graph_features, array_stats, active_features, preprocessing
from feature_computation.dpll import DPLLProbing

'''
Main file to control extraction of features

'''

def write_stats(l, name, features_dict):
    l_mean, l_coeff, l_min, l_max = array_stats.get_stats(l)

    features_dict[name + "_mean"] = l_mean
    features_dict[name + "_coeff"] = l_coeff
    features_dict[name + "_min"] = l_min
    features_dict[name + "_max"] = l_max


def write_entropy(l, name, features_dict, c, number_of_outcomes):
    entropy = array_stats.entropy_int_array(l, number_of_outcomes+1)
    features_dict[name + "_entropy"] = entropy


def write_entropy_float(l, name, features_dict, num, buckets=100, maxval=1):
    # scipy has an implementation for shannon entropy (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.entropy.html),
    # could be something to look into changing to
    entropy = array_stats.entropy_float_array(l, num, buckets, maxval)
    features_dict[name + "_entropy"] = entropy


def compute_base_features(clauses, c, v, num_active_vars, num_active_clauses):
    features_dict = {}

    # 1-3
    features_dict["c"] = num_active_clauses
    features_dict["v"] = num_active_vars
    features_dict["clauses_vars_ratio"] = num_active_clauses / num_active_vars
    features_dict["vars_clauses_ratio"] = num_active_vars / num_active_clauses

    # Variable Clause Graph features
    vcg_v_node_degrees, vcg_c_node_degrees = graph_features.create_vcg(clauses, c, v)
    # variable node degrees divided by number of active clauses
    vcg_v_node_degrees_norm = [x / c for x in vcg_v_node_degrees]
    # 4-8
    write_stats(vcg_v_node_degrees_norm, "vcg_var", features_dict)
    write_entropy(vcg_v_node_degrees, "vcg_var", features_dict, v, c)

    # clause node degrees divided by number of active variables
    vcg_c_node_degrees_norm = [x / v for x in vcg_c_node_degrees]
    # 9-13
    write_stats(vcg_c_node_degrees_norm, "vcg_clause", features_dict)
    write_entropy(vcg_c_node_degrees, "vcg_clause", features_dict, c, v)

    # Variable graph features
    vg_node_degrees = graph_features.create_vg(clauses)
    # 14-17
    # variable node degrees divided by number of active clauses
    vg_node_degrees_norm = [x / c for x in vg_node_degrees]

    write_stats(vg_node_degrees_norm, "vg", features_dict)

    # Balance features
    pos_neg_clause_ratios, pos_neg_clause_balance, pos_neg_variable_ratios, pos_neg_variable_balance, \
        num_binary_clauses, num_ternary_clauses, num_horn_clauses, horn_clause_variable_count = \
        balance_features.compute_balance_features(clauses, c, v)
    # 18-20
    write_stats(pos_neg_clause_balance, "pnc_ratio", features_dict)
    write_entropy_float(pos_neg_clause_balance, "pnc_ratio", features_dict, c)
    # 21-25
    write_stats(pos_neg_variable_balance, "pnv_ratio", features_dict)
    write_entropy_float(pos_neg_variable_balance, "pnv_ratio", features_dict, num_active_vars)

    features_dict["pnv_ratio_stdev"] = array_stats.get_stdev(pos_neg_variable_balance)
    # 26-27
    features_dict["binary_ratio"] = num_binary_clauses / c
    features_dict["ternary_ratio"] = num_ternary_clauses / c
    features_dict["ternary+"] = (num_binary_clauses + num_ternary_clauses) / c
    # 28
    features_dict["hc_fraction"] = num_horn_clauses / c
    # 29-33
    horn_clause_variable_count_norm = [x / c for x in horn_clause_variable_count]
    write_stats(horn_clause_variable_count_norm, "hc_var", features_dict)
    write_entropy(horn_clause_variable_count, "hc_var", features_dict, v, c)

    return features_dict


def compute_features_from_file(cnf_path="cnf_examples/basic.cnf"):
    # parse cnf, and get the features
    # store them in a dictionary
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

    write_entropy(vcg_v_node_degrees, "vcg_var", features_dict, v, c)

    # entropy needed
    # 9-13
    write_stats(vcg_c_node_degrees_norm, "vcg_clause", features_dict)
    write_entropy(vcg_c_node_degrees, "vcg_clause", features_dict, c, v)

    # 14-17
    vg_node_degrees = graph_features.create_vg(clauses)

    # variable node degrees divided by number of active clauses
    vg_node_degrees_norm = [x / c for x in vg_node_degrees]

    write_stats(vg_node_degrees_norm, "vg", features_dict)

    pos_neg_clause_ratios, pos_neg_clause_balance, pos_neg_variable_ratios, pos_neg_variable_balance,\
        num_binary_clauses, num_ternary_clauses, num_horn_clauses, horn_clause_variable_count = \
        balance_features.compute_balance_features(clauses, c, v)

    write_stats(pos_neg_clause_balance, "pnc_ratio", features_dict)
    write_entropy_float(pos_neg_clause_balance, "pnc_ratio", features_dict, c)

    write_stats(pos_neg_variable_balance, "pnv_ratio", features_dict)
    write_entropy_float(pos_neg_variable_balance, "pnv_ratio", features_dict, v)

    features_dict["pnv_ratio_stdev"] = array_stats.get_stdev(pos_neg_variable_balance)

    features_dict["binary_ratio"] = num_binary_clauses / c
    features_dict["ternary_ratio"] = num_ternary_clauses / c
    features_dict["ternary+"] = (num_binary_clauses + num_ternary_clauses) / c

    features_dict["hc_fraction"] = num_horn_clauses / c

    horn_clause_variable_count_norm = [x/c for x in horn_clause_variable_count]

    hc_var_mean, hc_var_coeff, hc_var_min, hc_var_max = array_stats.get_stats(horn_clause_variable_count_norm)
    write_entropy(horn_clause_variable_count, "hc_var", features_dict, v, c)

    features_dict["hc_var_mean"] = hc_var_mean
    features_dict["hc_var_coeff"] = hc_var_coeff
    features_dict["hc_var_min"] = hc_var_min
    features_dict["hc_var_max"] = hc_var_max

    return features_dict
