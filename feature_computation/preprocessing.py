import os


def satelite_preprocess(cnf_path="cnf_examples/basic.cnf"):
    # pre process using SatELite binary files
    preprocessed_path = cnf_path[0:-4] + "_preprocessed.cnf"
    satelite_command = "./SatELite/SatELite_v1.0_linux " + cnf_path + " " + preprocessed_path
    os.system(satelite_command)
    return preprocessed_path