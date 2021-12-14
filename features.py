from feature_computation import parse_cnf, balance_features, graph_features

'''
Main file to control extraction of features

'''


def compute_features_from_file(cnf_path="cnf_examples/basic.cnf"):
    clauses, c, v = parse_cnf.parse_cnf(cnf_path)
    balance_features.compute_balance_features(clauses, c, v)
    v_node_degrees, c_node_degrees = graph_features.create_vcg(clauses, c, v)
    print("VCG variable node degrees")
    print(v_node_degrees[0:10])
    print("VCG clause node degrees")
    print(c_node_degrees[0:10])
    print("VG node degrees")
    print(graph_features.create_vg(clauses))


if __name__ == "__main__":
    cnf_path = "cnf_examples/basic.cnf"
    compute_features_from_file(cnf_path)


