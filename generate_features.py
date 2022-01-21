import sys
from feature_computation.base_features import Features
from sat_instance.sat_instance import SATInstance
from feature_computation.dpll import DPLLProbing

if __name__ == "__main__":
    # Ideal usage - call features, with filename to calculate from, and then options on preprocessing,
    # and what features to calculate
    # cnf_path = sys.argv[1]
    # preprocess_option = sys.argv[2]

    # cnf_path = "cnf_examples/basic.cnf"
    # preprocessed_path = cnf_path[0:-4] + "_preprocessed.cnf"

    # n.b. satelite only works on linux, mac no longer supports 32 bit binaries...
    # satelite_preprocess(cnf_path)
    # preprocessed_path = "cnf_examples/out.cnf"
    # features_dict = compute_features_from_file(preprocessed_path)

    # print(features_dict)
    print(sys.path)

    cnf_path = "cnf_examples/out.cnf"
    satinstance = SATInstance(cnf_path, preprocess=False)

    satinstance.parse_active_features()

    # dpll_prober = DPLLProbing(satinstance)

    # shouldnt do anything at this point
    # print("unit prop")
    # dpll_prober.unit_prop(0, 0)

    satinstance.gen_basic_features()

    print(satinstance.features_dict)

    # test dpll probing
    print("probing")
    # dpll_prober.unit_prop_probe(haltOnAssignment=False, doComp=True)
    satinstance.gen_dpll_probing_features()

    print(satinstance.features_dict)

    # static test values for local testing
    # test_labels = ["nvarsOrig", "nclausesOrig", "nvars", "nclauses", "reducedVars", "reducedClauses", "Pre-featuretime",
    #                "vars-clauses-ratio", "POSNEG-RATIO-CLAUSE-mean",
    #                "POSNEG-RATIO-CLAUSE-coeff-variation", "POSNEG-RATIO-CLAUSE-min", "POSNEG-RATIO-CLAUSE-max",
    #                "POSNEG-RATIO-CLAUSE-entropy", "VCG-CLAUSE-mean",
    #                "VCG-CLAUSE-coeff-variation", "VCG-CLAUSE-min", "VCG-CLAUSE-max", "VCG-CLAUSE-entropy", "UNARY",
    #                "BINARY+", "TRINARY+", "Basic-featuretime", "VCG-VAR-mean", "VCG-VAR-coeff-variation",
    #                "VCG-VAR-min", "VCG-VAR-max", "VCG-VAR-entropy", "POSNEG-RATIO-VAR-mean", "POSNEG-RATIO-VAR-stdev",
    #                "POSNEG-RATIO-VAR-min", "POSNEG-RATIO-VAR-max", "POSNEG-RATIO-VAR-entropy",
    #                "HORNY-VAR-mean", "HORNY-VAR-coeff-variation", "HORNY-VAR-min", "HORNY-VAR-max", "HORNY-VAR-entropy",
    #                "horn-clauses-fraction", "VG-mean", "VG-coeff-variation", "VG-min", "VG-max",
    #                "KLB-featuretime", "CG-mean", "CG-coeff-variation", "CG-min", "CG-max", "CG-entropy",
    #                "cluster-coeff-mean", "cluster-coeff-coeff-variation", "cluster-coeff-min", "cluster-coeff-max",
    #                "cluster-coeff-entropy", "CG-featuretime"]
    # test_vals = [20.000000000, 45.000000000, 15.000000000, 40.000000000, 0.333333333, 0.125000000, 0.000000000,
    #              0.375000000, 1.000000000, 0.000000000, 1.000000000, 1.000000000, -0.000000000, 0.200000000,
    #              0.577350269, 0.133333333, 0.400000000, 0.562335145, 0.000000000, 0.750000000, 0.750000000, 0.000000000,
    #              0.200000000, 0.000000000, 0.200000000, 0.200000000, -0.000000000, 0.000000000, 0.000000000,
    #              0.000000000, 0.000000000, -0.000000000, 0.100000000, 0.000000000, 0.100000000, 0.100000000,
    #              -0.000000000, 0.750000000, 0.350000000, 0.000000000, 0.350000000, 0.350000000, 0.000000000,
    #              0.262500000, 0.577350269, 0.175000000, 0.525000000, 0.562335145, 0.210227273, 0.327685288, 0.090909091,
    #              0.250000000, 0.562335145, 0.000000000]
    #
    # satzilla_features = dict(zip(test_labels, test_vals))
    #
    # print("WE ARE CHECKING")
    # print("v, c")
    # print(features_dict["v"], features_dict["c"])
    # print(satzilla_features["nvars"], satzilla_features["nclauses"])
    # print("vars clauses ratio")
    # print(features_dict["vars_clauses_ratio"])
    # print(satzilla_features["vars-clauses-ratio"])
    #
    # print("vcg clause stats")
    # print(features_dict["vcg_clause_mean"], features_dict["vcg_clause_coeff"], features_dict["vcg_clause_min"], features_dict["vcg_clause_max"], features_dict["vcg_clause_entropy"])
    # print(satzilla_features["VCG-CLAUSE-mean"], satzilla_features["VCG-CLAUSE-coeff-variation"],
    #       satzilla_features["VCG-CLAUSE-min"], satzilla_features["VCG-CLAUSE-max"], satzilla_features["VCG-CLAUSE-entropy"])
    #
    # print("vcg variable stats")
    # print(features_dict["vcg_var_mean"], features_dict["vcg_var_coeff"], features_dict["vcg_var_min"],
    #       features_dict["vcg_var_max"], features_dict["vcg_var_entropy"])
    # print(satzilla_features["VCG-VAR-mean"], satzilla_features["VCG-VAR-coeff-variation"],
    #       satzilla_features["VCG-VAR-min"], satzilla_features["VCG-VAR-max"], satzilla_features["VCG-VAR-entropy"])
    #
    # print("vg stats")
    # print(features_dict["vg_mean"], features_dict["vg_coeff"], features_dict["vg_min"],
    #       features_dict["vg_max"])
    # print(satzilla_features["VG-mean"], satzilla_features["VG-coeff-variation"],
    #       satzilla_features["VG-min"], satzilla_features["VG-max"])
    #
    # print("pos neg clauses features")
    # print(features_dict["pnc_ratio_mean"], features_dict["pnc_ratio_coeff"], features_dict["pnc_ratio_min"],
    #       features_dict["pnc_ratio_max"], features_dict["pnc_ratio_entropy"])
    # print(satzilla_features["POSNEG-RATIO-CLAUSE-mean"], satzilla_features["POSNEG-RATIO-CLAUSE-coeff-variation"],
    #       satzilla_features["POSNEG-RATIO-CLAUSE-min"], satzilla_features["POSNEG-RATIO-CLAUSE-max"], satzilla_features["POSNEG-RATIO-CLAUSE-entropy"])
    #
    # print("pos neg variable features")
    # print(features_dict["pnv_ratio_mean"], features_dict["pnv_ratio_stdev"], features_dict["pnv_ratio_min"],
    #       features_dict["pnv_ratio_max"])
    # print(satzilla_features["POSNEG-RATIO-VAR-mean"], satzilla_features["POSNEG-RATIO-VAR-stdev"],
    #       satzilla_features["POSNEG-RATIO-VAR-min"], satzilla_features["POSNEG-RATIO-VAR-max"])
    #
    # print("binary, ternary, horn_clauses")
    # print(features_dict["binary_ratio"], features_dict["ternary+"], features_dict["hc_fraction"])
    # print(satzilla_features["BINARY+"], satzilla_features["TRINARY+"], satzilla_features["horn-clauses-fraction"])
    #
    # print("horn clause variables count")
    # print(features_dict["hc_var_mean"], features_dict["hc_var_coeff"], features_dict["hc_var_min"], features_dict["hc_var_max"])
    # print(satzilla_features["HORNY-VAR-mean"], satzilla_features["HORNY-VAR-coeff-variation"], satzilla_features["HORNY-VAR-min"], satzilla_features["HORNY-VAR-max"])
