import sys
from sat_instance.sat_instance import SATInstance

if __name__ == "__main__":
    # Ideal usage - call features, with filename to calculate from, and then options on preprocessing,
    # linux test setup
    try:
        cnf_path = sys.argv[1]

    except IndexError as E:
        print("no cnf path specified, using basic example")
        cnf_path = "cnf_examples/basic.cnf"

    if sys.platform == "darwin":
        # osx
        cnf_path = "cnf_examples/out.cnf"
        satinstance = SATInstance(cnf_path, preprocess=False)

    else:
        satinstance = SATInstance(cnf_path, preprocess=True)

    # basic setup with already preprocessed files
    # print(sys.path)
    #
    # cnf_path = "cnf_examples/out.cnf"
    # satinstance = SATInstance(cnf_path, preprocess=False)

    # this is a necessary step
    satinstance.gen_basic_features()

    # test dpll probing
    print("probing")
    # dpll_prober.unit_prop_probe(haltOnAssignment=False, doComp=True)
    satinstance.gen_dpll_probing_features()

    print(satinstance.features_dict)
