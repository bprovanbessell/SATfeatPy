import os
import sys
from shutil import copyfile
import glob
sys.path.append("/Users/bprovan/Insight/SAT-features")
sys.path.append("/home/bprovan/SAT-features")
# print(sys.path)
import unittest
from feature_computation import preprocessing, base_features as main_features
from sat_instance.sat_instance import SATInstance


def satzilla_results_to_dict(satzilla_results_file):

    satzilla_features_dict = {}
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
    return satzilla_features_dict


def gen_base_features(test_file, file_directory):
    """
    Generate satzilla features, and then generate features with this python script from the test file
    :param test_file:
    :return:
    """
    satzilla_dir = "../SAT-features-competition2012/"

    print(os.getcwd())

    if not os.path.isfile(satzilla_dir + test_file):
        copyfile(file_directory + test_file, satzilla_dir + test_file)

    # gen satzilla features
    os.chdir(satzilla_dir)

    satzilla_results_file = "results/" + test_file[0:-4] + "satzill_res"
    # see if it has been generated already (based on previous test runs)
    if not os.path.isfile(satzilla_results_file):
        # run satzilla feature generation
        os.system("./features -base " + test_file + " " + satzilla_results_file)

    satzilla_dict = satzilla_results_to_dict(satzilla_results_file)

    os.chdir("../SAT-features")
    # compute the features with our code
    cnf_path = file_directory + test_file

    sat_inst = SATInstance(cnf_path, preprocess=True)
    # n.b. satelite only works on linux, mac no longer supports 32 bit binaries...
    # preprocessing.satelite_preprocess(cnf_path)
    # features_dict = main_features.compute_features_from_file(preprocessed_path)
    sat_inst.parse_active_features()
    sat_inst.gen_basic_features()

    return satzilla_dict, sat_inst.features_dict


def gen_unit_props_features(test_file, file_directory):
    """
    Generate satzilla features, and then generate features with this python script from the test file
    :param test_file:
    :return:
    """
    satzilla_dir = "../SAT-features-competition2012/"

    if not os.path.isfile(satzilla_dir + test_file):
        copyfile(file_directory + test_file, satzilla_dir + test_file)

    # gen satzilla features
    os.chdir(satzilla_dir)

    satzilla_results_file = "results/" + test_file[0:-4] + "unit_props_res"
    # see if it has been generated already (based on previous test runs)
    if not os.path.isfile(satzilla_results_file):
        # run satzilla feature generation
        os.system("./features -unit " + test_file + " " + satzilla_results_file)

    satzilla_features_dict = satzilla_results_to_dict(satzilla_results_file)

    os.chdir("../SAT-features")
    # compute the features with our code
    cnf_path = file_directory + test_file

    sat_inst = SATInstance(cnf_path, preprocess=True)
    sat_inst.parse_active_features()
    sat_inst.gen_dpll_probing_features()

    return satzilla_features_dict, sat_inst.features_dict


def gen_search_space_est_features(test_file, file_directory):
    """
    Generate satzilla features, and then generate features with this python script from the test file
    :param test_file:
    :return:
    """
    satzilla_dir = "../SAT-features-competition2012/"

    if not os.path.isfile(satzilla_dir + test_file):
        copyfile(file_directory + test_file, satzilla_dir + test_file)

    # gen satzilla features
    os.chdir(satzilla_dir)

    satzilla_results_file = "results/" + test_file[0:-4] + "search_space_res"
    # see if it has been generated already (based on previous test runs)
    if not os.path.isfile(satzilla_results_file):
        # run satzilla feature generation
        os.system("./features -lobjois " + test_file + " " + satzilla_results_file)

    satzilla_features_dict = satzilla_results_to_dict(satzilla_results_file)

    os.chdir("../SAT-features")
    # compute the features with our code
    cnf_path = file_directory + test_file

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

    def setUp(self) -> None:
        self.unit_probing_names_map = {
            "vars-reduced-depth-1": "unit_props_at_depth_1",
            "vars-reduced-depth-4": "unit_props_at_depth_4",
            "vars-reduced-depth-16": "unit_props_at_depth_16",
            "vars-reduced-depth-64": "unit_props_at_depth_64",
            "vars-reduced-depth-256": "unit_props_at_depth_256"
        }

        self.base_names_map = {
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
            "HORNY-VAR-mean": "hc_var_mean",
            "HORNY-VAR-coeff-variation": "hc_var_coeff",
            "HORNY-VAR-min": "hc_var_min",
            "HORNY-VAR-max": "hc_var_max",
            "HORNY-VAR-entropy": "hc_var_entropy",
            "horn-clauses-fraction": "hc_fraction",
            "VG-mean": "vg_mean",
            "VG-coeff-variation": "vg_coeff",
            "VG-min": "vg_min",
            "VG-max": "vg_max",
            "POSNEG-RATIO-VAR-entropy": "pnv_ratio_entropy",
        }

        self.search_space_names_map = {
            "lobjois-mean-depth-over-vars": "mean_depth_to_contradiction_over_vars",
            "lobjois-log-num-nodes-over-vars": "estimate_log_number_nodes_over_vars"
        }

    # @unittest.skip("Not an issue atm")
    def test_base_features(self):

        test_files = ["basic.cnf", "php10_7.cnf", "parity_5.cnf", "parity_6.cnf", "subsetcard_5.cnf", "tseitin_10_4.cnf"]
        # directory relative to the project root
        file_directory = "cnf_examples/"

        for test_file in test_files:

            satzilla_features_dict, features_dict = gen_base_features(test_file, file_directory)
            print("now testing: " + test_file)

            for sat_feat_name, feat_name in self.base_names_map.items():
                print(sat_feat_name, feat_name)
                self.assertAlmostEqual(satzilla_features_dict[sat_feat_name], features_dict[feat_name])

    # @unittest.skip("not and issue atm")
    def test_unit_propagation_features(self):

        test_files = ["basic.cnf", "php10_7.cnf", "parity_5.cnf", "parity_6.cnf", "subsetcard_5.cnf", "tseitin_10_4.cnf"]
        file_directory = "cnf_examples/"

        for test_file in test_files:

            satzilla_features_dict, features_dict = gen_unit_props_features(test_file, file_directory)
            print("now testing: " + test_file)

            for sat_feat_name, feat_name in self.unit_probing_names_map.items():
                print(sat_feat_name, feat_name)
                self.assertAlmostEqual(satzilla_features_dict[sat_feat_name], features_dict[feat_name])

    # @unittest.skip("not an issue atm")
    def test_search_space_features(self):

        test_files = ["basic.cnf", "php10_7.cnf", "parity_5.cnf", "parity_6.cnf", "subsetcard_5.cnf", "tseitin_10_4.cnf"]
        file_directory = "cnf_examples/"

        for test_file in test_files:

            satzilla_features_dict, features_dict = gen_search_space_est_features(test_file, file_directory)
            print("now testing: " + test_file)

            # these features are stochastic in nature, and can vary, so we need a certain level of freedom with the testing
            # Not entirely sure how much is needed. As there is also a significant speed difference between python and c++
            # This further changes the results, as these features are based on approximations over a large number of runs
            for sat_feat_name, feat_name in self.search_space_names_map.items():
                print(sat_feat_name, feat_name)
                self.assertAlmostEqual(satzilla_features_dict[sat_feat_name], features_dict[feat_name], places=2)

    # @unittest.skip("Bug with satzilla???")
    def test_more_complex_cnfs(self):

        file_directory = "cnf_examples/more_complex_cnfs/"
        test_files = glob.glob(file_directory + "*.cnf")
        test_file_names = [x.split("/")[-1] for x in test_files]
        test_file_names = ["sat_4color_200_1126_10020.cnf", "sat_subsetcard_100_8400_64659.cnf",
                           "sat_tseitin_24_312_777.cnf", "unsat_4color_200_1126_33694.cnf"]

        for test_file in test_file_names:
            satzilla_features_dict, features_dict = gen_base_features(test_file, file_directory)
            print("now testing: " + test_file)

            # satzilla_features_dict, features_dict = gen_unit_props_features(test_file, file_directory)
            # print("now testing: " + test_file)

            for sat_feat_name, feat_name in self.base_names_map.items():
                print(sat_feat_name, satzilla_features_dict[sat_feat_name], feat_name, features_dict[feat_name])
                self.assertAlmostEqual(satzilla_features_dict[sat_feat_name], features_dict[feat_name])


if __name__ == '__main__':
    os.chdir("..")
    unittest.main()
