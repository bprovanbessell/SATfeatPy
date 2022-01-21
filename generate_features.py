import sys
from sat_instance.sat_instance import SATInstance

if __name__ == "__main__":

    # linux test setup
    cnf_path = sys.argv[1]

    if cnf_path == "":
        print("no cnf path specified, using basic example")
        cnf_path = "cnf_examples/basic.cnf"
    satinstance = SATInstance(cnf_path, preprocess=True)

    # Ideal usage - call features, with filename to calculate from, and then options on preprocessing,
    # and what features to calculate
    # cnf_path = sys.argv[1]
    # preprocess_option = sys.argv[2]

    # basic setup with already preprocessed files
    # print(sys.path)
    #
    # cnf_path = "cnf_examples/out.cnf"
    # satinstance = SATInstance(cnf_path, preprocess=False)

    # this is a necessary step
    satinstance.gen_basic_features()

    # print(satinstance.features_dict)

    # test dpll probing
    print("probing")
    # dpll_prober.unit_prop_probe(haltOnAssignment=False, doComp=True)
    satinstance.gen_dpll_probing_features()

    print(satinstance.features_dict)
