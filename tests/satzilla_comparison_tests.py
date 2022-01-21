import os
import sys
from shutil import copyfile
sys.path.append("/Users/bprovan/Insight/SAT-features")
sys.path.append("/home/bprovan/SAT-features")
# print(sys.path)
import unittest
from feature_computation import preprocessing, base_features as main_features
from sat_instance.sat_instance import SATInstance


def gen_base_satzilla_and_features_results(test_file):
    """
    Generate satzilla features, and then generate features with this python script from the test file
    :param test_file:
    :return:
    """
    cnf_example_dir = "cnf_examples/"
    satzilla_dir = "../SAT-features-competition2012/"

    print(os.getcwd())

    if not os.path.isfile(satzilla_dir + test_file):
        copyfile(cnf_example_dir + test_file, satzilla_dir + test_file)

    # gen satzilla features
    os.chdir(satzilla_dir)

    satzilla_results_file = "results/" + test_file[0:-4] + "satzill_res"
    # run satzilla feature generation
    os.system("./features -base " + test_file + " " + satzilla_results_file)

    satzilla_features_dict = {}
    # read output file
    with open(satzilla_results_file) as f:
        feature_names = []
        feature_vals = []
        for i, line in enumerate(f):
            if (i == 0):
                # first line contains the feature names
                feature_names = [str(x) for x in line.split(",")]
            if i == 1:
                # second line contains all of the features
                feature_vals = map(float, line.split(","))

        satzilla_features_dict = dict(zip(feature_names, feature_vals))

        # print("feature names: ", features_names)
        # print("features: ", features)
        # print(features_dict)

    f.close()

    os.chdir("../SAT-features")
    # compute the features with our code
    # preprocess the file with satelite
    cnf_path = "cnf_examples/" + test_file
    preprocessed_path = cnf_path[0:-4] + "_preprocessed.cnf"

    sat_inst = SATInstance(cnf_path, preprocess=True)
    # n.b. satelite only works on linux, mac no longer supports 32 bit binaries...
    # preprocessing.satelite_preprocess(cnf_path)
    # features_dict = main_features.compute_features_from_file(preprocessed_path)
    sat_inst.parse_active_features()
    sat_inst.gen_basic_features()

    return satzilla_features_dict, sat_inst.features_dict


def gen_dpll_satzilla_and_features_results(test_file):
    """
    Generate satzilla features, and then generate features with this python script from the test file
    :param test_file:
    :return:
    """
    cnf_example_dir = "cnf_examples/"
    satzilla_dir = "../SAT-features-competition2012/"

    if not os.path.isfile(satzilla_dir + test_file):
        copyfile(cnf_example_dir + test_file, satzilla_dir + test_file)

    # gen satzilla features
    os.chdir(satzilla_dir)

    satzilla_results_file = "results/" + test_file[0:-4] + "satzill_dpll_res"
    # run satzilla feature generation
    os.system("./features -unit " + test_file + " " + satzilla_results_file)

    satzilla_features_dict = {}
    # read output file
    with open(satzilla_results_file) as f:
        feature_names = []
        feature_vals = []
        for i, line in enumerate(f):
            if (i == 0):
                # first line contains the feature names
                feature_names = [str(x) for x in line.split(",")]
            if i == 1:
                # second line contains all of the features
                feature_vals = map(float, line.split(","))

        satzilla_features_dict = dict(zip(feature_names, feature_vals))

    f.close()

    os.chdir("../SAT-features")
    # compute the features with our code
    # preprocess the file with satelite
    cnf_path = "cnf_examples/" + test_file
    # preprocessed_path = cnf_path[0:-4] + "_preprocessed.cnf"

    sat_inst = SATInstance(cnf_path, preprocess=True)
    sat_inst.parse_active_features()
    sat_inst.gen_dpll_probing_features()

    return satzilla_features_dict, sat_inst.features_dict


class SatzillaComparisonTest(unittest.TestCase):
    """
    Satzilla and satelite only run on linux unfortunately
    Run from test root directory of project(SAT-features/tests)
    Based on the assumption that Satzilla feature extraction code is in the same directory that contains SAT-features
    """

    def test_base_features(self):

        satzilla_names_map = {
            "nvars": "v",
            "nclauses": "c",
            "vars-clauses-ratio": "vars_clauses_ratio",
            "POSNEG-RATIO-CLAUSE-mean": "pnc_ratio_mean",
            "POSNEG-RATIO-CLAUSE-coeff-variation": "pnc_ratio_coeff",
            "POSNEG-RATIO-CLAUSE-min": "pnc_ratio_min",
            "POSNEG-RATIO-CLAUSE-max": "pnc_ratio_max",
            "POSNEG-RATIO-CLAUSE-entropy": "pnc_ratio_entropy",
            "VCG-CLAUSE-mean": "vcg_clause_mean",
            "VCG-CLAUSE-coeff-variation": "vcg_clause_coeff",
            "VCG-CLAUSE-min": "vcg_clause_min",
            "VCG-CLAUSE-max": "vcg_clause_max",
            "VCG-CLAUSE-entropy": "vcg_clause_entropy",
            # "UNARY": ,
            "BINARY+": "binary_ratio",
            "TRINARY+": "ternary+",
            "VCG-VAR-mean": "vcg_var_mean",
            "VCG-VAR-coeff-variation": "vcg_var_coeff",
            "VCG-VAR-min": "vcg_var_min",
            "VCG-VAR-max": "vcg_var_max",
            "VCG-VAR-entropy": "vcg_var_entropy",
            "POSNEG-RATIO-VAR-mean": "pnv_ratio_mean",
            "POSNEG-RATIO-VAR-stdev": "pnv_ratio_stdev",
            "POSNEG-RATIO-VAR-min": "pnv_ratio_min",
            "POSNEG-RATIO-VAR-max": "pnv_ratio_max",
            "POSNEG-RATIO-VAR-entropy": "pnv_ratio_entropy",
            "HORNY-VAR-mean": "hc_var_mean",
            "HORNY-VAR-coeff-variation": "hc_var_coeff",
            "HORNY-VAR-min": "hc_var_min",
            "HORNY-VAR-max": "hc_var_max",
            "HORNY-VAR-entropy": "hc_var_entropy",
            "horn-clauses-fraction": "hc_fraction",
            "VG-mean": "vg_mean",
            "VG-coeff-variation": "vg_coeff",
            "VG-min": "vg_min",
            "VG-max": "vg_max"
        }

        test_files = ["basic.cnf", "php10_7.cnf", "parity_5.cnf", "parity_6.cnf", "subsetcard_5.cnf", "tseitin_10_4.cnf"]

        for test_file in test_files:

            satzilla_features_dict, features_dict = gen_base_satzilla_and_features_results(test_file)
            print("now testing: " + test_file)

            for sat_feat_name, feat_name in satzilla_names_map.items():
                print(sat_feat_name, feat_name)
                self.assertAlmostEqual(satzilla_features_dict[sat_feat_name], features_dict[feat_name])

    def test_unit_propagation_features(self):

        satzilla_names_map = {
            "vars-reduced-depth-1": "unit_props_at_depth_1",
            "vars-reduced-depth-4": "unit_props_at_depth_4",
            "vars-reduced-depth-16": "unit_props_at_depth_16",
            "vars-reduced-depth-64": "unit_props_at_depth_64",
            "vars-reduced-depth-256": "unit_props_at_depth_256",
        }

        test_files = ["basic.cnf", "php10_7.cnf", "parity_5.cnf", "parity_6.cnf", "subsetcard_5.cnf", "tseitin_10_4.cnf"]

        for test_file in test_files:

            satzilla_features_dict, features_dict = gen_dpll_satzilla_and_features_results(test_file)
            print("now testing: " + test_file)

            for sat_feat_name, feat_name in satzilla_names_map.items():
                print(sat_feat_name, feat_name)
                self.assertAlmostEqual(satzilla_features_dict[sat_feat_name], features_dict[feat_name])


if __name__ == '__main__':
    os.chdir("..")
    unittest.main()
